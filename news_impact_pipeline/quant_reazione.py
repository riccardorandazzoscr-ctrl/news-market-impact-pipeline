#!/usr/bin/env python3
"""Replay esplorativo del Run 11 — Quantitativo «reazione, non seguito» (sola lettura).

Riproduce le misure 1–4 di «Il problema, misurato» (PIANO_REVISIONE_PIPELINE.md, Run 11) su
ledger, libreria episodi e DB prezzi. ESPLORATIVO: sono dati già visti, non conta come prova.
Le definizioni (σ60, baseline normale, z, cancello, orizzonte primario) si leggono dal protocollo
experiments/quant_reazione/protocol-1.0.0.json; la prova vera è prospettica (Run 11e).

    venv/bin/python quant_reazione.py replay
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sqlite3
import sys
from datetime import date
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from analogues import LIB_PATH
from bootstrap_market_data import DB_PATH
from event_study import detect_monthly_data, load_price_series
from forecast_tracking import FLAT_THRESHOLD, LEDGER_PATH

PROTOCOL_PATH = Path(__file__).resolve().parents[1] / "experiments/quant_reazione/protocol-1.0.0.json"
HORIZONS = [1, 3, 5, 10]
EXPLORATIVE_N_MIN = 5         # soglia della fotografia del 2026-10-07 (il protocollo usa gate.n_min)
SPLIT_DAY = "2026-08-15"      # stabilità prima/dopo, come nella fotografia
ANY_DAY_ABS_Z = 0.674         # mediana di |N(0,1)|: «un giorno qualsiasi» in teoria


def load_protocol() -> dict:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


# --- definizioni del protocollo (pure) --------------------------------------------------------

def sigma(p: np.ndarray, a: int, window: int) -> float | None:
    """σ campionaria dei log-rendimenti delle `window` sedute che finiscono in a−1; mai prezzi ≥ a."""
    if a - window - 1 < 0:
        return None
    seg = p[a - window - 1:a]
    if (seg <= 0).any():
        return None
    s = float(np.std(np.diff(np.log(seg)), ddof=1))
    return s if s > 0 else None


def reaction(p: np.ndarray, a: int, window: int) -> tuple[float, float] | None:
    """(R0 in %, z0) della seduta a contro a−1; None se σ non è calcolabile."""
    s = sigma(p, a, window)
    if s is None or p[a] <= 0:
        return None
    return (p[a] / p[a - 1] - 1) * 100, math.log(p[a] / p[a - 1]) / s


def baseline(p: np.ndarray, a: int, h: int, window: int) -> np.ndarray | None:
    """Rendimenti a h sedute (%) delle `window` finestre che terminano in a−window … a−1."""
    if a - window - h < 0:
        return None
    seg = p[a - window - h:a]
    if (seg <= 0).any():
        return None
    return (seg[h:] / seg[:-h] - 1) * 100


def abs_z_all_sessions(s: pd.Series, window: int) -> pd.Series:
    """|z0| di ogni seduta della serie, con la stessa σ di `sigma` (controllo «giorno qualsiasi»)."""
    lr = np.log(s.where(s > 0)).diff()
    return (lr / lr.rolling(window).std().shift(1)).abs().dropna()


def deviation_z(med: float, p25: float, p75: float, n: int, normal_median: float) -> float | None:
    iqr = abs(p75 - p25)
    if iqr == 0 or n < 1:
        return None
    return (med - normal_median) / (iqr / 1.349 / math.sqrt(n))


def passes_gate(z: float | None, n: int, gate: dict) -> bool:
    return z is not None and abs(z) >= gate["z_min"] and n >= gate["n_min"]


def deviation_hit(med: float, normal_median: float, realized: float) -> int | None:
    """1 se il realizzato si scosta dal normale nel verso della mediana del pool; None se uno scarto è zero."""
    d_pool, d_real = med - normal_median, realized - normal_median
    if d_pool == 0 or d_real == 0:
        return None
    return int((d_pool > 0) == (d_real > 0))


def daily_votes(cells: list[dict]) -> pd.Series:
    """Quota giornaliera di celle con hit = 1 (hit None escluse), in ordine di giorno."""
    df = pd.DataFrame([c for c in cells if c["hit"] is not None], columns=["day", "hit"])
    return df.groupby("day")["hit"].mean().sort_index()


def binom_one_sided(k: int, n: int) -> float:
    """P(X ≥ k) con X ~ Binomiale(n, 0,5)."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def vote_test(votes: pd.Series) -> dict:
    above, below = int((votes > 0.5).sum()), int((votes < 0.5).sum())
    return {"above": above, "below": below, "ties": len(votes) - above - below,
            "p": binom_one_sided(above, above + below) if above + below else float("nan")}


def lag1_autocorr(votes: pd.Series) -> float:
    x = (votes[votes != 0.5] > 0.5).to_numpy(dtype=float)
    if len(x) < 3 or x[:-1].std() == 0 or x[1:].std() == 0:
        return float("nan")
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def spearman(a, b) -> float:
    return pd.Series(list(a)).rank().corr(pd.Series(list(b)).rank())


# --- dati (sola lettura) ----------------------------------------------------------------------

def price_loader(conn):
    """prices(asset) → serie delle sedute con prezzo valido; None se assente o mensile."""
    @lru_cache(maxsize=None)
    def prices(asset: str) -> pd.Series | None:
        try:
            s = load_price_series(conn, asset).dropna()
        except ValueError:
            return None
        return None if detect_monthly_data(s) else s
    return prices


def _num(x: str) -> float | None:
    return float(x) if x not in ("", None) else None


def ledger_cells(rows: list[dict], prices, proto: dict) -> list[dict]:
    """Celle del ledger: scenario base, registrazione originale, realizzato congelato e prezzi validi."""
    sw, bw = proto["sigma_window_sessions"], proto["baseline_window_sessions"]
    out = []
    for r in rows:
        if (r["scenario"] != "base" or r["registration"] == "recovered" or r["uso"] == "ritirata"
                or r["ingestion_status"] == "quarantine" or not r["expected_median"]
                or not r["realized_return"] or not r["anchor_date"]):
            continue
        s = prices(r["asset"])
        if s is None:
            continue
        anchor = pd.Timestamp(r["anchor_date"])
        a = int(s.index.searchsorted(anchor))
        if a >= len(s) or s.index[a] != anchor:
            continue                                   # ancora congelata assente dalla serie di oggi
        p, h = s.to_numpy(), int(r["horizon"])
        base = baseline(p, a, h, bw)
        prev = reaction(p, a - 1, sw)
        c = {"day": r["made_date"], "card": r["card_path"], "asset": r["asset"], "h": h,
             "med": float(r["expected_median"]), "n": int(r["n_analogues"] or 0),
             "p25": _num(r["hist_p25"]), "p75": _num(r["hist_p75"]), "uso": r["uso"],
             "realized": float(r["realized_return"]),
             "realized_prev": (p[a - 1 + h] / p[a - 1] - 1) * 100 if 1 <= a <= len(p) - h and p[a - 1] > 0 else None,
             "z_prev": prev[1] if prev else None,
             "normal_median": float(np.median(base)) if base is not None else None,
             "normal_p25": float(np.percentile(base, 25)) if base is not None else None,
             "normal_p75": float(np.percentile(base, 75)) if base is not None else None}
        ok = None not in (c["p25"], c["p75"], c["normal_median"])
        c["z"] = deviation_z(c["med"], c["p25"], c["p75"], c["n"], c["normal_median"]) if ok else None
        c["hit"] = deviation_hit(c["med"], c["normal_median"], c["realized"]) if c["normal_median"] is not None else None
        out.append(c)
    return out


def library_pairs(episodes: list[dict], prices, proto: dict) -> list[dict]:
    """Coppie (data, asset) con verso univoco pos/neg: reazione del giorno-ancora e seguito T+h."""
    sw = proto["sigma_window_sessions"]
    out = []
    for e in episodes:
        for asset, dirs in (e.get("directions_by_reference") or {}).items():
            if len(set(dirs)) != 1 or dirs[0] not in ("pos", "neg"):
                continue
            s = prices(asset)
            if s is None:
                continue
            d = pd.Timestamp(e["date"])
            a = int(s.index.searchsorted(d))
            if a + max(HORIZONS) >= len(s) or s.index[a] - d > pd.Timedelta(days=4):
                continue                               # seguito non osservabile o ancora troppo lontana
            p = s.to_numpy()
            rz = reaction(p, a, sw)
            if rz is None:
                continue
            srcs = (e.get("direction_sources") or {}).get(asset, [])
            out.append({"date": e["date"], "theme": e["theme"], "asset": asset,
                        "verso": 1 if dirs[0] == "pos" else -1, "r0": rz[0], "z0": rz[1],
                        "src": "kb" if any(str(x).startswith("kb:") for x in srcs) else "card",
                        **{f"r{h}": (p[a + h] / p[a] - 1) * 100 for h in HORIZONS}})
    return out


# --- misure ----------------------------------------------------------------------------------

def sign_hit(pred: pd.Series, real: pd.Series) -> tuple[float, int]:
    """Quota di segno indovinato, escluse le chiamate piatte (|pred| < FLAT) e i realizzati nulli."""
    m = (pred.abs() >= FLAT_THRESHOLD) & real.notna() & (real != 0)
    return float((np.sign(pred[m]) == np.sign(real[m])).mean()), int(m.sum())


def ic_within(df: pd.DataFrame, x: str, y: str, min_n: int = 15) -> tuple[float, int]:
    """Correlazione di rango dentro asset×orizzonte, media pesata per numerosità."""
    g = [(len(v), spearman(v[x], v[y])) for _, v in df.groupby(["asset", "h"]) if len(v) >= min_n]
    g = [(n, r) for n, r in g if not math.isnan(r)]
    if not g:
        return float("nan"), 0
    return float(np.average([r for _, r in g], weights=[n for n, _ in g])), len(g)


def misura_1(cells: list[dict]) -> list[str]:
    df = pd.DataFrame(cells)
    out = ["## 1. Il segno del seguito: mediana del pool contro realizzato",
           f"celle {len(df)} · schede {df.card.nunique()} · giorni {df.day.nunique()} · asset {df.asset.nunique()}",
           "", "| Orizzonte | N | segno indovinato | realizzato su | ancora a−1 |", "|---|---|---|---|---|"]
    for h, g in df.groupby("h"):
        hit, n = sign_hit(g.med, g.realized)
        prev, _ = sign_hit(g.med, g.realized_prev.astype(float))
        up = (g.realized[(g.med.abs() >= FLAT_THRESHOLD) & (g.realized != 0)] > 0).mean()
        out.append(f"| T+{h} | {n} | {hit:.1%} | {up:.0%} | {prev:.1%} |")
    ic, k = ic_within(df, "med", "realized")
    out += ["", f"IC dentro asset×orizzonte (gruppi ≥ 15 celle: {k}): {ic:+.3f}", "",
            "Per numerosità del pool:"]
    df["nb"] = pd.cut(df.n, [0, 9, 19, 29, 10_000], labels=["<10", "10-19", "20-29", "30+"])
    for nb, g in df.groupby("nb", observed=True):
        hit, n = sign_hit(g.med, g.realized)
        out.append(f"- N {nb}: {hit:.1%} (celle {n}, giorni {g.day.nunique()})")
    big = df[df.z_prev.astype(float).abs() >= 1.5]
    cont = (np.sign(big.z_prev.astype(float)) == np.sign(big.realized))[big.realized != 0].mean()
    out += ["", f"Mossa già avvenuta (ultima seduta chiusa, |z| ≥ 1,5): il seguito continua nel {cont:.1%} "
                f"dei casi (celle {len(big)}, giorni {big.day.nunique()})"]
    return out


def misura_2(cells: list[dict]) -> list[str]:
    b = pd.DataFrame([c for c in cells if c["p25"] is not None and c["normal_median"] is not None])
    lo, hi = b[["p25", "p75"]].min(axis=1), b[["p25", "p75"]].max(axis=1)
    b["in_pool"] = (b.realized >= lo) & (b.realized <= hi)
    b["in_norm"] = (b.realized >= b.normal_p25) & (b.realized <= b.normal_p75)
    b["w_pool"], b["w_norm"] = hi - lo, b.normal_p75 - b.normal_p25
    out = ["## 2. Il pool contro il comportamento normale dell'asset (250 sedute prima)",
           f"celle {len(b)} · giorni {b.day.nunique()} (atteso per una banda p25–p75 tarata: 50%)", "",
           "| Orizzonte | N | copertura pool | copertura normale | ampiezza pool | ampiezza normale |",
           "|---|---|---|---|---|---|"]
    for h, g in b.groupby("h"):
        out.append(f"| T+{h} | {len(g)} | {g.in_pool.mean():.0%} | {g.in_norm.mean():.0%} | "
                   f"{g.w_pool.median():.2f} pp | {g.w_norm.median():.2f} pp |")
    out += ["", "Errore assoluto medio del realizzato contro:"]
    for lab, ref in (("mediana del pool", b.med), ("mediana normale", b.normal_median), ("zero", 0.0)):
        out.append(f"- {lab}: {(b.realized - ref).abs().mean():.3f} pp")
    return out


def misura_3(pairs: list[dict], any_day: float) -> list[str]:
    d = pd.DataFrame(pairs)
    out = ["## 3. Il giorno della notizia: libreria episodi con verso univoco",
           f"coppie (data, asset) {len(d)} · date {d.date.nunique()} · asset {d.asset.nunique()}",
           f"|z0| mediano del giorno-ancora: {d.z0.abs().median():.2f} — giorno qualsiasi: "
           f"{ANY_DAY_ABS_Z} in teoria, {any_day:.2f} misurato sugli stessi asset", "",
           "| Fonte del verso | N | giorno-ancora | T+1 | T+3 | T+5 | T+10 |", "|---|---|---|---|---|---|---|"]
    for lab, g in (("tutte", d), ("research KB", d[d.src == "kb"]), ("schede", d[d.src == "card"])):
        cols = ["r0"] + [f"r{h}" for h in HORIZONS]
        rates = [(np.sign(g[c]) == g.verso)[g[c] != 0].mean() for c in cols]
        out.append(f"| {lab} | {len(g)} | " + " | ".join(f"{x:.0%}" for x in rates) + " |")
    return out


def _votes_line(label: str, cells: list[dict]) -> str:
    t = vote_test(daily_votes(cells))
    return (f"- {label}: giorni sopra {t['above']}, sotto {t['below']}, pari {t['ties']} "
            f"(p unilaterale {t['p']:.3f}; celle {sum(c['hit'] is not None for c in cells)})")


def misura_4(cells: list[dict], proto: dict) -> list[str]:
    gate, hp = proto["gate"], proto["primary_horizon_sessions"]
    b = [c for c in cells if c["z"] is not None and c["hit"] is not None]
    exp = [c for c in b if c["n"] >= EXPLORATIVE_N_MIN]
    out = ["## 4. Il cancello: la mediana del pool lontana dal normale",
           f"Definizione esplorativa (N ≥ {EXPLORATIVE_N_MIN}, tutti gli orizzonti) — celle {len(exp)}", "",
           "| abs(z) | celle | giorni | scostamento indovinato | segno della mediana |", "|---|---|---|---|---|"]
    for lo, hi in ((0, 1), (1, 2), (2, 3), (3, math.inf)):
        g = pd.DataFrame([c for c in exp if lo <= abs(c["z"]) < hi])
        if g.empty:
            continue
        sh, _ = sign_hit(g.med, g.realized)
        lab = f"≥ {lo}" if hi == math.inf else f"{lo}–{hi}"
        out.append(f"| {lab} | {len(g)} | {g.day.nunique()} | {g.hit.mean():.1%} | {sh:.1%} |")
    hi2 = [c for c in exp if abs(c["z"]) >= 2]
    out += ["", "Un voto per giorno:", _votes_line("abs(z) ≥ 2", hi2),
            _votes_line("abs(z) < 1", [c for c in exp if abs(c["z"]) < 1])]
    for lab, part in (("prima del " + SPLIT_DAY, [c for c in hi2 if c["day"] < SPLIT_DAY]),
                      ("dal " + SPLIT_DAY, [c for c in hi2 if c["day"] >= SPLIT_DAY])):
        if part:
            out.append(f"  - {lab}: {np.mean([c['hit'] for c in part]):.1%} "
                       f"(celle {len(part)}, giorni {len({c['day'] for c in part})})")
    prim = [c for c in b if c["h"] == hp]
    strict = [c for c in prim if passes_gate(c["z"], c["n"], gate)]
    days_all = len({c["day"] for c in cells if c["h"] == hp})
    v = daily_votes(strict)
    out += ["", f"Regola del protocollo {proto['protocol_version']} (abs(z) ≥ {gate['z_min']}, "
                f"N ≥ {gate['n_min']}, T+{hp}) sui dati già visti:",
            f"- giorni con almeno una cella sopra cancello: {len(v)} su {days_all}",
            _votes_line("sopra cancello", strict),
            f"- autocorrelazione lag-1 dei voti: {lag1_autocorr(v):+.2f}",
            _votes_line("controllo abs(z) < 1, stessa N", [c for c in prim if abs(c["z"]) < 1 and c["n"] >= gate["n_min"]]),
            _votes_line("solo tabelle [previsione]", [c for c in strict if c["uso"] == "previsione"])]
    return out


# --- comando ---------------------------------------------------------------------------------

def replay() -> str:
    proto = load_protocol()
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        prices = price_loader(conn)
        with open(LEDGER_PATH, newline="", encoding="utf-8") as f:
            cells = ledger_cells(list(csv.DictReader(f)), prices, proto)
        episodes = yaml.safe_load(LIB_PATH.read_text(encoding="utf-8"))["episodes"]
        pairs = library_pairs(episodes, prices, proto)
        assets = sorted({p["asset"] for p in pairs})
        any_day = float(pd.concat([abs_z_all_sessions(prices(a), proto["sigma_window_sessions"])
                                   for a in assets]).median())
        lines = [f"# Replay esplorativo — Run 11 «reazione, non seguito» ({date.today()})",
                 f"⚠ ESPLORATIVO: dati già visti, non conta come prova. La prova è prospettica "
                 f"(protocollo {proto['protocol_version']}, Run 11e).", "",
                 *misura_1(cells), "", *misura_2(cells), "", *misura_3(pairs, any_day), "",
                 *misura_4(cells, proto)]
    finally:
        conn.close()
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("replay", help="misure esplorative 1–4 del Run 11 (sola lettura)")
    ap.parse_args(argv)
    print(replay())
    return 0


if __name__ == "__main__":
    sys.exit(main())
