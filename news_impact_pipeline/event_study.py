#!/usr/bin/env python3
"""
event_study.py

Calcolo deterministico di event study per la Fase 4 del News Impact Pipeline.

Dato un asset (o una lista di asset) e una lista di date di eventi storici
analoghi, calcola il rendimento cumulato in finestre di trading days
(default T+1, T+3, T+5, T+10) e produce statistiche aggregate
(media, mediana, dev std, percentili 25/75, N).

Approccio "Opzione A" (vedi memory [[feedback-event-study-design]]):
l'analista fornisce manualmente le date degli episodi analoghi; il sistema
si limita al calcolo statistico. La comparabilita' degli eventi e' un atto
di giudizio analitico, non automatizzato.

Convenzioni metodologiche:
  - T=0 (anchor)   = primo giorno con dati di mercato on or after event_date
                     (gestisce eventi in weekend/festivi/after-hours)
  - T+N            = N-esimo giorno con dati strettamente dopo T=0
  - Rendimento     = simple cumulative return = (P_{T+N} / P_0 - 1) * 100 (in %)
  - Prezzo         = adj_close se disponibile (reinvesti dividendi), fallback su close
  - Per ticker con dati radi (es. BTP_BUND_SPREAD mensile), l'event study
    a finestre giornaliere e' sconsigliato; il sistema emette un warning.

Sample size: se N < 10, l'output e' flaggato come "⚠ INDICATIVE ONLY".
Questo e' coerente con CLAUDE.md e con il Design Document §7 (caveat).

Uso CLI:
    venv/bin/python event_study.py \\
        --ticker '^STOXX50E' \\
        --events 2014-06-05,2014-09-04,2019-09-12,2024-06-06 \\
        --windows 1,3,5,10

    # Multi-asset (ripeti --ticker o usa CSV):
    venv/bin/python event_study.py \\
        --ticker '^STOXX50E,EURUSD=X,^TNX' \\
        --events 2014-06-05,2014-09-04 \\
        --markdown

Uso programmatico:
    from event_study import run_event_study
    result = run_event_study(['^STOXX50E'], ['2014-06-05', '2014-09-04'])
"""

import argparse
import sqlite3
import sys
from datetime import date, datetime
from statistics import mean, median, pstdev
from pathlib import Path

import pandas as pd

from bootstrap_market_data import DB_PATH


DEFAULT_WINDOWS = [1, 3, 5, 10]
SAMPLE_SIZE_WARNING_THRESHOLD = 10


# --- DB lookup -------------------------------------------------------------

def load_price_series(conn, ticker: str, use_adj: bool = True) -> pd.Series:
    """
    Restituisce una Series di prezzi indicizzata per data (sorted),
    valori NaN inclusi solo se ne mancano nel DB.

    Se use_adj=True, prova adj_close; fallback automatico a close se adj_close
    e' NULL per quella riga (succede per BTP_BUND_SPREAD o ticker recenti).
    """
    col_pref = "COALESCE(adj_close, close)" if use_adj else "close"
    rows = conn.execute(
        f"SELECT date, {col_pref} FROM prices WHERE ticker = ? ORDER BY date",
        (ticker,)
    ).fetchall()

    if not rows:
        raise ValueError(
            f"Ticker '{ticker}' non ha prezzi nel DB. "
            f"Verifica che sia registrato in 'assets' e che il bootstrap sia stato fatto."
        )

    dates  = [date.fromisoformat(r[0]) for r in rows]
    prices = [r[1] for r in rows]
    s = pd.Series(prices, index=pd.DatetimeIndex(dates), dtype=float, name=ticker)
    return s.sort_index()


def detect_monthly_data(s: pd.Series) -> bool:
    """
    Euristica: se il numero medio di giorni fra osservazioni consecutive e'
    >= 20, e' una serie mensile (tipo FRED BTP_BUND_SPREAD).
    """
    if len(s) < 3:
        return False
    diffs = s.index.to_series().diff().dt.days.dropna()
    return diffs.mean() >= 20


# --- Anchor + targets ------------------------------------------------------

def find_anchor_and_targets(prices: pd.Series,
                            event_date: date,
                            windows: list[int]) -> dict | None:
    """
    Identifica T=0 (anchor) come primo giorno con dati >= event_date.
    Per ciascuna finestra N, T+N = N-esimo giorno con dati strettamente
    successivo all'anchor.

    Restituisce None se:
      - event_date e' prima del primo dato disponibile
      - event_date e' dopo l'ultimo dato disponibile
      - NESSUNA delle window richieste e' coperta dai dati
    Altrimenti restituisce un dict:
      {
        "event_date":    date,
        "anchor_date":   date,
        "anchor_price":  float,
        "windows": {N: {"target_date": date, "target_price": float}, ...},
      }
    Le window non coperte sono escluse dalla chiave "windows".
    """
    if event_date < prices.index.min().date():
        return None
    if event_date > prices.index.max().date():
        return None

    # Indice posizionale del primo prezzo >= event_date
    pos_anchor = prices.index.searchsorted(pd.Timestamp(event_date), side="left")
    if pos_anchor >= len(prices):
        return None

    anchor_date  = prices.index[pos_anchor].date()
    anchor_price = float(prices.iloc[pos_anchor])
    if pd.isna(anchor_price) or anchor_price == 0:
        return None

    targets = {}
    for n in windows:
        pos_target = pos_anchor + n
        if pos_target >= len(prices):
            continue  # finestra fuori dai dati disponibili
        tprice = prices.iloc[pos_target]
        if pd.isna(tprice):
            continue
        targets[n] = {
            "target_date":  prices.index[pos_target].date(),
            "target_price": float(tprice),
        }

    if not targets:
        return None

    return {
        "event_date":    event_date,
        "anchor_date":   anchor_date,
        "anchor_price":  anchor_price,
        "windows":       targets,
    }


# --- Calcolo rendimenti + stats -------------------------------------------

def compute_returns(conn, ticker: str, event_dates: list[date],
                    windows: list[int], use_adj: bool = True) -> dict:
    """
    Per un singolo asset, calcola rendimenti cumulati per ogni evento.

    Restituisce dict:
      {
        "ticker":       str,
        "warnings":     list[str],
        "is_monthly":   bool,
        "per_event":    [ {event_date, anchor_date, anchor_price,
                            returns: {N: pct, ...}, skipped_windows: [N, ...]},
                           ...],
        "skipped_events": [ {event_date, reason}, ... ],
      }
    """
    prices = load_price_series(conn, ticker, use_adj=use_adj)
    is_monthly = detect_monthly_data(prices)
    warnings = []
    if is_monthly:
        warnings.append(
            f"⚠ '{ticker}' sembra avere dati mensili (FRED?). "
            f"L'event study a finestre giornaliere e' poco significativo."
        )

    per_event   = []
    skipped     = []
    # Dedup per GIORNO-ANCORA: date-evento diverse possono risolvere sullo stesso primo
    # giorno di borsa (weekend → lunedì, festivi, eventi a 1 giorno di distanza). Senza
    # dedup lo STESSO movimento entra 2-3 volte: N gonfiato e dispersione compressa —
    # cioè bande più strette del vero, il difetto che stiamo combattendo. Al 2026-07-29
    # il 9,6% degli episodi in libreria cadeva di sabato/domenica. Vince la data più
    # antica (ordine deterministico, indipendente da come arriva la lista).
    seen_anchors: dict = {}

    for ed in sorted(event_dates):
        info = find_anchor_and_targets(prices, ed, windows)
        if info is None:
            skipped.append({
                "event_date": ed,
                "reason": "event_date fuori dal range dati o nessuna finestra coperta",
            })
            continue

        anchor = info["anchor_date"]
        if anchor in seen_anchors:
            skipped.append({
                "event_date": ed,
                "reason": f"stesso giorno-ancora ({anchor}) di {seen_anchors[anchor]} "
                          f"→ duplicato scartato (non conta due volte lo stesso movimento)",
            })
            continue
        seen_anchors[anchor] = info["event_date"]

        returns = {}
        for n, t in info["windows"].items():
            returns[n] = (t["target_price"] / info["anchor_price"] - 1.0) * 100.0

        skipped_windows = [w for w in windows if w not in info["windows"]]
        per_event.append({
            "event_date":     info["event_date"],
            "anchor_date":    info["anchor_date"],
            "anchor_price":   info["anchor_price"],
            "returns":        returns,
            "skipped_windows": skipped_windows,
        })

    return {
        "ticker":         ticker,
        "warnings":       warnings,
        "is_monthly":     is_monthly,
        "per_event":      per_event,
        "skipped_events": skipped,
    }


def aggregate_stats(per_event: list[dict], windows: list[int]) -> dict:
    """
    Per ogni finestra, aggrega gli eventi per cui la finestra esiste:
    mean, median, stdev (campionaria), p25, p75, N.
    Restituisce dict {N: {stat: value or None}}.
    """
    out = {}
    for n in windows:
        values = [pe["returns"][n] for pe in per_event if n in pe["returns"]]
        N = len(values)
        if N == 0:
            out[n] = {"mean": None, "median": None, "stdev": None,
                      "p25": None, "p75": None, "N": 0}
            continue
        series = pd.Series(values)
        out[n] = {
            "mean":   series.mean(),
            "median": series.median(),
            "stdev":  series.std(ddof=1) if N >= 2 else 0.0,
            "p25":    series.quantile(0.25),
            "p75":    series.quantile(0.75),
            "N":      N,
        }
    return out


def run_event_study(tickers: list[str], event_dates: list[date],
                    windows: list[int] = None,
                    use_adj: bool = True) -> dict:
    """
    Esegue lo studio per multipli ticker. Restituisce dict per-ticker.
    """
    if windows is None:
        windows = DEFAULT_WINDOWS

    conn = sqlite3.connect(DB_PATH)
    out = {}
    try:
        for t in tickers:
            computed = compute_returns(conn, t, event_dates, windows, use_adj=use_adj)
            computed["stats"] = aggregate_stats(computed["per_event"], windows)
            out[t] = computed
    finally:
        conn.close()
    return out


# --- Output formatting -----------------------------------------------------

def _fmt(v, dec=2):
    return f"{v:+.{dec}f}" if v is not None else "  n/a"


def format_console(study: dict, windows: list[int]) -> str:
    """Tabelle leggibili per la console."""
    lines = []
    for ticker, data in study.items():
        lines.append(f"\n=== {ticker} ===")
        for w in data["warnings"]:
            lines.append(f"  {w}")

        if not data["per_event"]:
            lines.append("  Nessun evento valido nel campione.")
            for sk in data["skipped_events"]:
                lines.append(f"    skipped: {sk['event_date']} ({sk['reason']})")
            continue

        # Tabella per-event
        header = "  Event date  | Anchor      | " + " | ".join(
            f"T+{w:<3}" for w in windows
        )
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        for pe in data["per_event"]:
            row = f"  {pe['event_date']}  | {pe['anchor_date']}  | " + " | ".join(
                _fmt(pe["returns"].get(w)) + "%" if w in pe["returns"] else "  n/a "
                for w in windows
            )
            lines.append(row)

        # Skipped events
        for sk in data["skipped_events"]:
            lines.append(f"  [skip]  {sk['event_date']}: {sk['reason']}")

        # Stats
        stats = data["stats"]
        lines.append("\n  Aggregate stats (in % di rendimento cumulato):")
        head = "  Stat    | " + " | ".join(f"T+{w:<3}" for w in windows)
        lines.append(head)
        lines.append("  " + "-" * (len(head) - 2))
        for stat_name in ("mean", "median", "stdev", "p25", "p75"):
            row = f"  {stat_name:<7} | " + " | ".join(
                _fmt(stats[w][stat_name]) + "%" for w in windows
            )
            lines.append(row)
        lines.append(
            "  N       | " + " | ".join(f" {stats[w]['N']:>4}  " for w in windows)
        )

        # Sample size warning
        min_N = min((stats[w]["N"] for w in windows if stats[w]["N"] > 0), default=0)
        if 0 < min_N < SAMPLE_SIZE_WARNING_THRESHOLD:
            lines.append(
                f"\n  ⚠ INDICATIVE ONLY: campione N={min_N} < {SAMPLE_SIZE_WARNING_THRESHOLD}. "
                f"Non trattare come evidenza robusta."
            )

    return "\n".join(lines)


def format_markdown(study: dict, windows: list[int], detail: bool = True) -> str:
    """Tabella markdown da incollare in una scheda news.

    Con detail=False omette il blocco <details> per-event: è l'85% dei byte
    dell'output e nelle schede non viene mai incollato. Chiedilo solo quando
    serve davvero ispezionare i singoli episodi (potatura del pool, outlier).
    """
    blocks = []
    for ticker, data in study.items():
        block = [f"### Event study — `{ticker}`\n"]
        for w in data["warnings"]:
            block.append(f"> {w}\n")

        if not data["per_event"]:
            block.append("_Nessun evento valido nel campione._\n")
            blocks.append("\n".join(block))
            continue

        stats = data["stats"]
        min_N = min((stats[w]["N"] for w in windows if stats[w]["N"] > 0), default=0)

        # Tabella stats (compatta)
        cols = ["Stat"] + [f"T+{w}" for w in windows]
        block.append("| " + " | ".join(cols) + " |")
        block.append("|" + "|".join(["---"] * len(cols)) + "|")
        for stat_name, label in [("mean", "media"), ("median", "mediana"),
                                 ("stdev", "dev std"), ("p25", "p25"),
                                 ("p75", "p75")]:
            row = [label] + [
                f"{_fmt(stats[w][stat_name])}%" for w in windows
            ]
            block.append("| " + " | ".join(row) + " |")
        block.append("| **N** | " + " | ".join(f"**{stats[w]['N']}**" for w in windows) + " |")
        block.append("")

        # Sample size flag
        if 0 < min_N < SAMPLE_SIZE_WARNING_THRESHOLD:
            block.append(
                f"> ⚠ **INDICATIVE ONLY** — campione N={min_N} < "
                f"{SAMPLE_SIZE_WARNING_THRESHOLD}. Non trattare come evidenza robusta."
            )

        # Dettaglio per-event (collassabile mentale)
        if not detail:
            if data["skipped_events"]:
                block.append(
                    f"\n> {len(data['skipped_events'])} evento/i scartato/i "
                    f"(fuori serie o dati mancanti). Rilancia con --detail per l'elenco."
                )
            blocks.append("\n".join(block))
            continue

        block.append("\n<details><summary>Dettaglio per-event</summary>\n")
        block.append("| Event date | Anchor | " +
                     " | ".join(f"T+{w}" for w in windows) + " |")
        block.append("|" + "|".join(["---"] * (2 + len(windows))) + "|")
        for pe in data["per_event"]:
            row = [str(pe["event_date"]), str(pe["anchor_date"])] + [
                f"{_fmt(pe['returns'].get(w))}%" if w in pe["returns"] else "n/a"
                for w in windows
            ]
            block.append("| " + " | ".join(row) + " |")
        for sk in data["skipped_events"]:
            block.append(f"| {sk['event_date']} | _skipped_ | " +
                         " | ".join(["n/a"] * len(windows)) + " |")
        block.append("\n</details>")

        blocks.append("\n".join(block))

    return "\n\n".join(blocks)


# --- CLI -------------------------------------------------------------------

def _parse_dates(s: str) -> list[date]:
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if not tok:
            continue
        out.append(date.fromisoformat(tok))
    return out


def _parse_tickers(values: list[str]) -> list[str]:
    """Flatten lista di --ticker, supportando CSV in un singolo valore."""
    out = []
    for v in values:
        for t in v.split(","):
            t = t.strip()
            if t and t not in out:
                out.append(t)
    return out


def _parse_windows(s: str) -> list[int]:
    return sorted({int(x) for x in s.split(",") if x.strip()})


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--ticker", action="append", required=True,
                   help="Ticker (ripetibile o CSV: es. '^GSPC,EURUSD=X')")
    p.add_argument("--events", required=True,
                   help="Date evento separate da virgola (AAAA-MM-GG,AAAA-MM-GG,...)")
    p.add_argument("--windows", default=",".join(str(w) for w in DEFAULT_WINDOWS),
                   help=f"Finestre in trading days, CSV (default: {DEFAULT_WINDOWS})")
    p.add_argument("--no-adj", action="store_true",
                   help="Usa 'close' invece di 'adj_close' (default: usa adj_close)")
    p.add_argument("--markdown", action="store_true",
                   help="Output in formato markdown (incollabile in schede news)")
    p.add_argument("--detail", action="store_true",
                   help="Con --markdown: aggiunge il blocco <details> per-event "
                        "(una riga per episodio). Di default è OMESSO: pesa l'85%% "
                        "dell'output e nelle schede non si incolla mai. Chiedilo "
                        "solo per ispezionare i singoli episodi (potatura, outlier).")

    args = p.parse_args()

    tickers     = _parse_tickers(args.ticker)
    event_dates = _parse_dates(args.events)
    windows     = _parse_windows(args.windows)

    if not tickers:
        sys.exit("Errore: nessun ticker fornito.")
    if not event_dates:
        sys.exit("Errore: nessuna data evento fornita.")
    if not windows:
        sys.exit("Errore: nessuna finestra valida.")

    study = run_event_study(tickers, event_dates, windows, use_adj=not args.no_adj)

    if args.markdown:
        print(format_markdown(study, windows, detail=args.detail))
    else:
        print(format_console(study, windows))


if __name__ == "__main__":
    main()
