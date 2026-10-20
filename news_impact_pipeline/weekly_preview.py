#!/usr/bin/env python3
"""weekly_preview.py — anteprima settimanale dal calendario.

Per ogni evento macro o di banca centrale della settimana successiva mostra i due scenari
storici condizionali (verso pos e neg sull'asset di riferimento), con N, e le research
collegate. Statistica descrittiva, non previsione. Commento e bozze LinkedIn li scrive
`claude -p` in run_weekly_preview.sh; qui solo la parte deterministica.

Spec: docs/superpowers/specs/2026-10-17-anteprima-settimanale-design.md
"""
from datetime import date, datetime, time, timedelta
import json
import re
import sys
from pathlib import Path
import urllib.request
from zoneinfo import ZoneInfo

import yaml

from stile import BASE

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EVENTS_MAP = HERE / "anteprima_eventi.yaml"
CB_CALENDAR = HERE / "calendario_banche_centrali.yaml"
PREVIEW_DIR = ROOT / "weekly_preview"
LOGDIR = HERE / "logs"
ENV = Path.home() / "Claude" / ".env"
ROME = ZoneInfo("Europe/Rome")
NY = ZoneInfo("America/New_York")
FRED_TIME = time(8, 30)          # ora ufficiale dei rilasci USA del perimetro


def load_events_map(path: Path = EVENTS_MAP) -> dict[str, dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_cb_calendar(path: Path = CB_CALENDAR) -> list[dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))["meetings"]


def env(key: str) -> str:
    for line in ENV.read_text().splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(f"{key} mancante in {ENV}")


def fred_dates(release_id: int, start: date, end: date) -> list[date]:
    url = ("https://api.stlouisfed.org/fred/release/dates?file_type=json"
           f"&release_id={release_id}&api_key={env('FRED_API_KEY')}"
           "&include_release_dates_with_no_data=true"
           f"&realtime_start={start}&realtime_end=9999-12-31")
    with urllib.request.urlopen(url, timeout=60) as r:
        rows = json.load(r)["release_dates"]
    return [d for d in (date.fromisoformat(x["date"]) for x in rows) if start <= d <= end]


def target_week(now: datetime) -> date | None:
    """Il lunedì della settimana da preparare: domenica dalle 18:00 la prossima; lunedì e
    martedì quella in corso (ripresa a Mac spento); negli altri momenti nessuna."""
    now = now.astimezone(ROME)
    today = now.date()
    if today.weekday() == 6 and now.hour >= 18:
        return today + timedelta(days=1)
    if today.weekday() in (0, 1):
        return today - timedelta(days=today.weekday())
    return None


def _rome_hhmm(day: date, local: time, tz: ZoneInfo) -> str:
    return datetime.combine(day, local, tz).astimezone(ROME).strftime("%H:%M")


def week_events(monday: date, as_of: date, fred=fred_dates, cb: list[dict] | None = None,
                events_map: dict | None = None) -> list[dict]:
    events_map = load_events_map() if events_map is None else events_map
    cb = load_cb_calendar() if cb is None else cb
    friday = monday + timedelta(days=4)
    by_bank = {spec["bank"]: name for name, spec in events_map.items() if "bank" in spec}
    out = []

    def add(event_type, label, day, hhmm, mapped):
        if day >= as_of:
            out.append({"id": f"{day}:{event_type}", "event_type": event_type, "label": label,
                        "reaction_session": day, "time_rome": hhmm, "mapped": mapped})

    for name, spec in events_map.items():
        if "fred_release_id" in spec:
            for d in fred(spec["fred_release_id"], monday, friday):
                add(name, spec["label"], d, _rome_hhmm(d, FRED_TIME, NY), True)
    for row in cb:
        d = row["reaction_session"]
        if not monday <= d <= friday:
            continue
        hhmm, tz = row["time_local"].split()
        hhmm = _rome_hhmm(row["decision"], time.fromisoformat(hhmm), ZoneInfo(tz))
        name = by_bank.get(row["bank"])
        if name:
            add(name, events_map[name]["label"], d, hhmm, True)
        else:
            add(row["bank"], row["bank"].upper(), d, hhmm, False)
    return sorted(out, key=lambda e: (e["reaction_session"], e["time_rome"], e["event_type"]))


# --- Scenari e tabelle ------------------------------------------------------

WINDOWS = [1, 3, 5, 10]
# Quotano un rendimento in percentuale (5,098 = 5,098%): la variazione si legge in punti base,
# non in % del livello («+2% di ^TNX» sono circa 10 bp, non 2 punti).
YIELDS = {"^TNX", "^FVX", "^TYX"}


def status_for(n: int) -> str:
    return "insufficiente" if n < 5 else "indicativo" if n < 10 else "ok"


def scenario_pool(spec: dict, direction: str, before: date) -> tuple[list[str], str]:
    """Pool di `analogues.py find` per un verso: date-locali strette, nessun fallback,
    solo episodi anteriori a `before` (no look-ahead)."""
    import contextlib
    import io
    import analogues
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        analogues.cmd_find(spec["theme"], direction, before.isoformat(), spec["subthemes"], 12, 0,
                           match_all=spec.get("match_all", False),
                           direction_reference=spec["reference"], strict=True)
    return [d for d in out.getvalue().strip().split(",") if d], err.getvalue().strip()


def scenario_stats(dates: list[str], assets: list[str], as_of: date) -> dict[str, dict[str, dict]]:
    import event_study
    study = event_study.run_event_study(assets, [date.fromisoformat(d) for d in dates],
                                        WINDOWS, as_of=as_of)
    import statistics
    out = {}
    for ticker, res in study.items():
        out[ticker] = {}
        for n in WINDOWS:
            if ticker in YIELDS:
                vals = [(pe["targets"][n]["target_price"] - pe["anchor_price"]) * 100
                        for pe in res["per_event"] if n in pe.get("targets", {})]
                med, unit = (statistics.median(vals) if vals else None), "bp"
            else:
                vals = [pe["returns"][n] for pe in res["per_event"] if n in pe["returns"]]
                med, unit = res["stats"].get(n, {}).get("median"), "%"
            out[ticker][str(n)] = {"median": None if med is None else float(med),
                                   "pos_share": sum(v > 0 for v in vals) / len(vals) if vals else None,
                                   "N": len(vals), "unit": unit}
    return out


def pool_composition(theme: str, dates: list[str]) -> list[list]:
    """Etichette date-locali più frequenti fra gli episodi del pool: dice cosa c'è davvero
    dentro (il pool «PCE» è fatto in gran parte di CPI). Si calcola, non si scrive a mano."""
    import collections
    import analogues
    wanted = set(dates)
    c = collections.Counter(lbl for e in analogues._load()
                            if e["theme"] == theme and e["date"] in wanted
                            for lbl in e.get("subthemes_local") or [])
    return [[lbl, n] for lbl, n in c.most_common(5)]


def related_research(spec: dict) -> list[dict]:
    import pipeline_tools
    hits = pipeline_tools.match_research(theme=spec["theme"], sub_themes=spec["subthemes"],
                                         assets=spec["assets"], text=spec["match_query"])
    hits = sorted(hits, key=lambda h: -h["score"])[:2]
    return [{"title": h["title"], "source_file": h["source_file"], "score": h["score"]} for h in hits]


def _cell(s: dict, n_pool: int) -> str:
    if not s or s["median"] is None:
        return "—"
    n = "" if s["N"] == n_pool else f", N={s['N']}"   # date senza prezzi per quell'asset
    value = f"{s['median']:.1f} bp" if s.get("unit") == "bp" else f"{s['median']:.2f}%"
    return f"{value} ({round(100 * s['pos_share'])}%{n})"


def _by_start(data_start: dict[str, str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for tk, d in data_start.items():
        out.setdefault(d, []).append(tk)
    return out


def data_start(tickers: set[str]) -> dict[str, str]:
    import sqlite3
    conn = sqlite3.connect(ROOT / "market_data" / "market_data.db")
    try:
        return {tk: conn.execute("SELECT MIN(date) FROM prices WHERE ticker=?", (tk,)).fetchone()[0][:10]
                for tk in sorted(tickers)}
    finally:
        conn.close()


def _markdown(t: dict, events_map: dict) -> str:
    lines = [f"# Anteprima {t['week']} (dati al {t['as_of']})", "",
             "Celle: mediana del rendimento cumulato (quota di casi positivi). Statistica "
             "descrittiva sugli analoghi storici, non una previsione.",
             "Rendimenti dalla chiusura del giorno dell'evento (T=0) alla chiusura di T+n sedute: "
             "la reazione del giorno stesso non è inclusa. Gli episodi sono quelli della nostra "
             "libreria (research e schede), non tutti i rilasci storici. Per " + ", ".join(sorted(YIELDS)) +
             ", che sono rendimenti, la variazione è in punti base (bp).",
             "Prezzi giornalieri disponibili: " + ", ".join(
                 f"{', '.join(tk)} dal {d}" for d, tk in sorted(_by_start(t.get("data_start", {})).items())) + ".", ""]
    for e in t["events"]:
        lines += [f"## {e['id']} — {e['label']}", "",
                  f"{e['reaction_session']} ore {e['time_rome']} (Roma) · riferimento "
                  f"{e.get('reference') or '—'} · stato: {e['status']}", ""]
        if e.get("pool"):
            lines += [f"Pool: {e['pool']}.", ""]
        for d, sc in e.get("scenarios", {}).items():
            n_min = sc.get("N_min", sc["N"])
            n_min = "" if n_min == sc["N"] else f", celle con N fino a {n_min}"
            period = f", campione dal {sc['dates'][0]} al {sc['dates'][-1]}" if sc["dates"] else ""
            lines += [f"### Scenario {d}: {sc['label']} (N={sc['N']}{n_min}, {sc['status']}{period})", ""]
            if sc.get("composition"):
                lines += ["Etichette più frequenti nel pool, composizione: " +
                          ", ".join(f"{lbl} {n}" for lbl, n in sc["composition"]), ""]
            if sc["stats"]:
                lines += ["| asset | " + " | ".join(f"T+{n}" for n in WINDOWS) + " |",
                          "|---|" + "---|" * len(WINDOWS)]
                for ticker, row in sc["stats"].items():
                    lines.append(f"| {ticker} | " + " | ".join(_cell(row.get(str(n)), sc["N"]) for n in WINDOWS) + " |")
                lines.append("")
        if e.get("research"):
            lines += ["Research collegate: " + "; ".join(r["title"] for r in e["research"]), ""]
    lines += ["## Lacune", ""]
    lines += [f"- {l['event']}: tema `{l['theme']}`, verso `{l['direction']}` su `{l['reference']}`, "
              f"N={l['N']}" for l in t["lacune"]] or ["- nessuna"]
    return "\n".join(lines) + "\n"


def build(week_of: date, as_of: date, out_root: Path = PREVIEW_DIR, fred=fred_dates) -> Path:
    monday = week_of + timedelta(days=7 - week_of.weekday())
    year, wk, _ = monday.isocalendar()
    out = out_root / f"{year}-W{wk:02d}"
    events_map = load_events_map()
    tables = {"week": out.name, "monday": monday.isoformat(), "as_of": as_of.isoformat(),
              "events": [], "lacune": []}
    for ev in week_events(monday, as_of, fred=fred, events_map=events_map):
        row = dict(ev, reaction_session=ev["reaction_session"].isoformat())
        if not ev["mapped"]:
            row["status"] = "non_mappato"
            tables["events"].append(row)
            continue
        spec = events_map[ev["event_type"]]
        row.update(reference=spec["reference"], pool=spec["pool"], scenarios={},
                   research=related_research(spec))
        for d in ("pos", "neg"):
            dates, note = scenario_pool(spec, d, as_of)
            stats, n_min = {}, len(dates)
            if status_for(n_min) != "insufficiente":
                stats = scenario_stats(dates, spec["assets"], as_of)
                # Lo stato segue la cella più povera: una data senza prezzi abbassa N.
                n_min = min((c["N"] for r in stats.values() for c in r.values()), default=0)
            st = status_for(n_min)
            row["scenarios"][d] = {"label": spec["scenarios"][d], "dates": dates, "N": len(dates),
                                   "N_min": n_min, "status": st, "note": note,
                                   "composition": pool_composition(spec["theme"], dates) if dates else [],
                                   "stats": {} if st == "insufficiente" else stats}
            if st == "insufficiente":
                tables["lacune"].append({"event": row["id"], "theme": spec["theme"],
                                         "reference": spec["reference"], "direction": d, "N": n_min})
        both_out = all(s["status"] == "insufficiente" for s in row["scenarios"].values())
        row["status"] = "insufficiente" if both_out else "ok"
        tables["events"].append(row)
    tables["data_start"] = data_start({tk for e in tables["events"]
                                       for sc in e.get("scenarios", {}).values() for tk in sc["stats"]})
    out.mkdir(parents=True, exist_ok=True)
    (out / "tabelle.json").write_text(json.dumps(tables, ensure_ascii=False, indent=1))
    (out / "tabelle.md").write_text(_markdown(tables, events_map))
    return out


# --- Validatore del testo del modello ---------------------------------------

CLOSING = "descriptive statistics, not a forecast"   # la bozza LinkedIn è in inglese
_NUM = re.compile(r"([-−+]?)(\d+(?:[.,]\d+)?)")


def parse_text(text: str) -> dict[str, dict[str, str]]:
    """`testo.md`: `## <event_id>`, poi `### Commento` e `### Bozza LinkedIn`."""
    out = {}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        parts = re.split(r"^### (Commento|Bozza LinkedIn)\s*$", body, flags=re.M)
        sec = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}
        out[head.strip()] = {"commento": sec.get("Commento", ""), "bozza": sec.get("Bozza LinkedIn", "")}
    return out


def _allowed_numbers(tables: dict) -> tuple[set[str], dict[str, set[str]]]:
    """Cifre ammesse senza segno, e per le mediane i segni ammessi («-», «+»)."""
    ok = {str(n) for n in WINDOWS} | {tables["as_of"][:4]}
    ok |= {d[:4] for d in tables.get("data_start", {}).values()}
    signs: dict[str, set[str]] = {}
    for e in tables["events"]:
        for r in e.get("research", []):
            ok |= {m[1] for m in _NUM.findall(r.get("title", ""))}
        for sc in e.get("scenarios", {}).values():
            ok.add(str(sc.get("N_min", sc["N"])))
            ok |= {str(n) for _, n in sc.get("composition", [])}
            ok.add(str(sc["N"]))
            ok |= {d[:4] for d in sc["dates"]}
            for row in sc["stats"].values():
                for s in row.values():
                    ok.add(str(s["N"]))
                    if s["median"] is not None:
                        for fmt in ("{:.2f}", "{:.1f}") + (("{:.0f}",) if s.get("unit") == "bp" else ()):
                            v = fmt.format(abs(s["median"]))
                            sign = "-" if s["median"] < 0 else "+"
                            for w in (v, v.replace(".", ",")):
                                ok.add(w)
                                signs.setdefault(w, set()).add(sign)
                    if s["pos_share"] is not None:
                        ok.add(str(round(100 * s["pos_share"])))
    return ok, signs


def validate(text: str, tables: dict) -> list[str]:
    problems = []
    sections = parse_text(text)
    wanted = {e["id"] for e in tables["events"] if e.get("status") == "ok"}
    for eid in sorted(wanted - set(sections)):
        problems.append(f"manca la sezione di {eid}")
    for eid in sorted(set(sections) - wanted):
        problems.append(f"sezione per un evento non in tabella: {eid}")
    for eid, sec in sections.items():
        if not sec["commento"] or not sec["bozza"]:
            problems.append(f"{eid}: commento o bozza vuoti")
        if CLOSING not in sec["bozza"].lower() or "N=" not in sec["bozza"]:
            problems.append(f"{eid}: la bozza non chiude con N e «{CLOSING}»")
        if len(re.findall(r"(?<!\w)#\w+", sec["bozza"])) < 3:
            problems.append(f"{eid}: la bozza ha meno di 3 hashtag")
        ev = next((e for e in tables["events"] if e["id"] == eid), None)
        starts = {sc["dates"][0][:4] for sc in (ev or {}).get("scenarios", {}).values()
                  if sc["stats"] and sc["dates"]}
        if starts and not any(y in sec["bozza"] for y in starts):
            problems.append(f"{eid}: la bozza non dice da quando parte il campione ({', '.join(sorted(starts))})")
    ok, signs = _allowed_numbers(tables)
    # Orari e ticker delle tabelle non sono cifre: si tolgono prima del controllo. Un orario
    # che non sta in tabella resta e viene rifiutato come cifra.
    names = {tk for e in tables["events"] for sc in e.get("scenarios", {}).values() for tk in sc["stats"]}
    names |= {e["time_rome"] for e in tables["events"] if e.get("time_rome")}
    clean = re.sub(r"(?<!\w)#\w+", " ", text)
    for name in sorted(names, key=len, reverse=True):
        clean = clean.replace(name, " ")
    clean = re.sub(r"\d{4}-\d{2}-\d{2}(:\w+)?|T\+\d+", " ", clean)
    for sign, num in sorted(set(_NUM.findall(clean))):
        if num not in ok:
            problems.append(f"cifra non presente nelle tabelle: {num}")
        elif sign and num in signs and ("-" if sign in "-−" else "+") not in signs[num]:
            problems.append(f"segno sbagliato: {sign}{num}")
    return problems


# --- Report HTML e avviso del calendario ------------------------------------

ALERTS = LOGDIR / "weeklypreview_avvisi.txt"
CSS = BASE + """
main{max-width:760px;margin:auto;padding:28px 16px 60px}
h1,h2,h3,.meta,.badge,table,.cal,summary,.legend{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif}
h1{font-size:30px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--soft);margin:0 0 24px;font-size:15px}
h2{font-size:23px;margin:0 0 4px}
h3{font-size:16px;margin:26px 0 6px}
.legend{font-size:14px;color:var(--soft);background:var(--quote);border-radius:10px;padding:12px 16px;margin:0 0 28px}
.cal{list-style:none;padding:0;margin:0 0 32px}
.cal li{display:flex;gap:14px;padding:10px 0;border-bottom:1px solid var(--line);font-size:15px}
.cal .when{color:var(--soft);min-width:150px}.cal a{color:var(--accent);text-decoration:none;font-weight:600}
.cal .muted{color:var(--soft)}
.event{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 22px;margin:0 0 28px}
.meta{color:var(--soft);font-size:14px;margin:0 0 18px}
.brief{border-left:3px solid var(--accent);padding:2px 0 2px 16px;margin:0 0 8px}
.brief p{margin:0 0 10px}
.scen-sub{color:var(--soft);font-size:14px;font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;margin:0 0 8px}
.badge{display:inline-block;font-size:12px;font-weight:600;padding:2px 9px;border-radius:999px;
background:var(--quote);color:var(--soft);margin-left:8px;vertical-align:2px}
.badge.warn{background:var(--warn-bg);color:var(--warn)}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;margin:4px 0 6px}
th{font-weight:600;color:var(--soft);font-size:12px;text-transform:uppercase;letter-spacing:.04em;
text-align:right;padding:6px 8px;border-bottom:1px solid var(--line)}
td{text-align:right;padding:8px;border-bottom:1px solid var(--line);white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal}
td .tk{display:block;color:var(--soft);font-size:11px}
td b{font-weight:600}.up{color:var(--up)}.down{color:var(--down)}
td small{display:block;color:var(--soft);font-size:11px}
img{margin:18px 0 4px}
details{margin:18px 0 0;font-size:15px}
summary{cursor:pointer;color:var(--accent);font-size:14px;font-weight:600}
details .inner{padding:8px 0 0;color:var(--soft)}
.nota{background:var(--warn-bg);color:var(--warn);border-radius:10px;padding:12px 16px;font-size:15px}
.bozza{background:var(--quote);border-radius:10px;padding:14px 18px;margin:12px 0;font-size:15px}
.bozza .t{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;font-size:13px;color:var(--soft)}
footer{color:var(--soft);font-size:13px;margin-top:36px}
@media (max-width:520px){body{font-size:16px}.event{padding:18px 14px}td,th{padding:6px 4px}table{font-size:13px}.cal li{flex-direction:column;gap:2px}}
"""
# Nome in italiano per la pagina; un ticker che manca qui ricade sul nome del DB.
NOMI_IT = {"CNY=X": "Dollaro/yuan", "HG=F": "Rame", "EEM": "Azioni emergenti",
           "^TNX": "Rendimento Treasury 10 anni", "^FVX": "Rendimento Treasury 5 anni",
           "IEF": "Treasury 7-10 anni (prezzo)", "DX-Y.NYB": "Indice del dollaro",
           "^GSPC": "S&P 500", "GC=F": "Oro", "EURUSD=X": "Euro/dollaro", "JPY=X": "Dollaro/yen",
           "GBPUSD=X": "Sterlina/dollaro", "^N225": "Nikkei 225", "1482.T": "Titoli di Stato USA in yen",
           "^STOXX50E": "Euro Stoxx 50", "BTP_BUND_SPREAD": "Spread BTP-Bund",
           "IEAG.AS": "Obbligazioni area euro", "IGLT.L": "Gilt britannici", "XLY": "Consumi USA (azioni)"}
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]


def _giorno(iso: str, weekday: bool = True) -> str:
    d = date.fromisoformat(iso)
    return (f"{GIORNI[d.weekday()]} " if weekday else "") + f"{d.day} {MESI[d.month - 1]}"


def _html_cell(s: dict | None, n_pool: int) -> str:
    if not s or s["median"] is None:
        return "<td>—</td>"
    m = s["median"]
    value = f"{m:+.1f} bp" if s.get("unit") == "bp" else f"{m:+.2f}%"
    n = "" if s["N"] == n_pool else f", su {s['N']}"
    cls = "up" if m > 0 else "down" if m < 0 else ""
    return (f"<td><b class='{cls}'>{value.replace('-', '−')}</b>"
            f"<small>{round(100 * s['pos_share'])}% positivi{n}</small></td>")


def _scenario_html(sc: dict, names: dict) -> str:
    import html
    head, _, sub = sc["label"].partition(" (")
    badge = (f"<span class='badge'>{sc['N']} casi</span>" if sc["status"] == "ok" else
             f"<span class='badge warn'>{sc['N']} casi · solo indicativo</span>" if sc["status"] == "indicativo"
             else f"<span class='badge warn'>{sc['N']} casi · troppo pochi</span>")
    out = f"<h3>{html.escape(head[:1].upper() + head[1:])}{badge}</h3>"
    if sub:
        out += f"<p class='scen-sub'>{html.escape(sub.rstrip(')'))}</p>"
    if not sc["stats"]:
        return out + "<p class='scen-sub'>Troppo pochi casi nella libreria per una tabella.</p>"
    rows = "".join(f"<tr><td>{html.escape(names.get(tk, tk))}<span class='tk'>{html.escape(tk)}</span></td>"
                   + "".join(_html_cell(row.get(str(n)), sc["N"]) for n in WINDOWS) + "</tr>"
                   for tk, row in sc["stats"].items())
    heads = "".join(f"<th>{n} {'seduta' if n == 1 else 'sedute'}</th>" for n in WINDOWS)
    return out + f"<div class='tw'><table><tr><th>Asset</th>{heads}</tr>{rows}</table></div>"


def render(week_dir: Path) -> Path:
    import base64
    import html
    import markdown
    tables = json.loads((week_dir / "tabelle.json").read_text())
    text_file = week_dir / "testo.md"
    text, reason = {}, "il testo del modello non c'è"
    if text_file.exists():
        problems = validate(text_file.read_text(), tables)
        if problems:
            reason = "il testo del modello non ha passato la validazione (" + "; ".join(problems[:3]) + ")"
        else:
            text = parse_text(text_file.read_text())
    tickers = sorted({tk for e in tables["events"] for sc in e.get("scenarios", {}).values() for tk in sc["stats"]})
    names = {**_asset_names(tickers), **{tk: NOMI_IT[tk] for tk in tickers if tk in NOMI_IT}}
    monday = date.fromisoformat(tables["monday"])
    sunday = monday + timedelta(days=6)
    parts = [f"<h1>La settimana dal {_giorno(tables['monday'], False)} al {_giorno(sunday.isoformat(), False)}</h1>",
             f"<p class='sub'>Anteprima {tables['week']} · dati di mercato al {_giorno(tables['as_of'], False)}</p>",
             "<p class='legend'>Per ogni appuntamento: cosa hanno fatto i mercati nei casi passati simili, "
             "divisi per esito. Ogni cella è la variazione mediana dalla chiusura del giorno dell'evento "
             "a 1, 3, 5 e 10 sedute dopo (la reazione del giorno stesso non è inclusa); sotto, in quale quota dei casi "
             "è stata positiva. Statistica descrittiva sui casi della nostra libreria, non una previsione.</p>"]
    if not text:
        parts.append(f"<p class='nota'>Commento e bozze non disponibili: {html.escape(reason)}.</p>")
    cal = []
    for i, e in enumerate(tables["events"]):
        when = f"{_giorno(e['reaction_session']).capitalize()}, {e['time_rome']}"
        what = (f"<a href='#ev{i}'>{html.escape(e['label'])}</a>" if e["status"] == "ok" else
                f"{html.escape(e['label'])} <span class='muted'>· pochi casi passati, nessuna tabella</span>")
        cal.append(f"<li><span class='when'>{when}</span><span>{what}</span></li>")
    parts.append("<h3>In calendario</h3><ul class='cal'>" + "".join(cal) + "</ul>")
    for i, e in enumerate(tables["events"]):
        if e["status"] != "ok":
            continue
        ev = [f"<section class='event' id='ev{i}'><h2>{html.escape(e['label'])}</h2>",
              f"<p class='meta'>{_giorno(e['reaction_session']).capitalize()}, ore {e['time_rome']} (Roma)</p>"]
        if e["id"] in text:
            ev.append("<div class='brief'>" + markdown.markdown(text[e["id"]]["commento"]) + "</div>")
        ev += [_scenario_html(sc, names) for sc in e.get("scenarios", {}).values()]
        png = week_dir / f"grafico-{e['event_type']}.png"
        if png.exists():   # incorporato: il report viaggia su Telegram come file unico
            ev.append(f"<img alt='grafico {html.escape(e['label'])}' "
                      f"src='data:image/png;base64,{base64.b64encode(png.read_bytes()).decode()}'>")
        det = [f"<p>Casi considerati: {html.escape(e.get('pool') or '—')}. Asset che decide l'esito: "
               f"{html.escape(names.get(e.get('reference'), e.get('reference') or '—'))}.</p>"]
        for sc in e.get("scenarios", {}).values():
            if sc["dates"]:
                comp = ", ".join(f"{lbl} {n}" for lbl, n in sc.get("composition", []))
                det.append(f"<p>{html.escape(sc['label'].partition(' (')[0].capitalize())}: {sc['N']} casi "
                           f"dal {_giorno(sc['dates'][0], False)} {sc['dates'][0][:4]} al "
                           f"{_giorno(sc['dates'][-1], False)} {sc['dates'][-1][:4]}"
                           + (f" · etichette: {html.escape(comp)}" if comp else "") + ".</p>")
        if e.get("research"):
            det.append("<p>Research collegate: " + "; ".join(html.escape(r["title"]) for r in e["research"]) + ".</p>")
        ev.append("<details><summary>Dettagli sul campione</summary><div class='inner'>" + "".join(det) + "</div></details>")
        parts.append("".join(ev) + "</section>")
    if text:
        bozze = "".join(
            # Testo semplice, non Markdown: «#Hashtag» a inizio riga diventerebbe un titolo.
            f"<div class='bozza'><p class='t'>{html.escape(eid)} · bozza da rivedere</p>"
            f"<p>{html.escape(sec['bozza']).replace(chr(10), '<br>')}</p></div>" for eid, sec in text.items())
        parts.append(f"<details><summary>Bozze LinkedIn ({len(text)})</summary>{bozze}</details>")
    lac = "".join(f"<li>{html.escape(l['event'])}: tema {l['theme']}, verso {l['direction']} su "
                  f"{html.escape(l['reference'])}, {l['N']} casi</li>" for l in tables["lacune"])
    parts.append("<details><summary>Lacune della libreria</summary><div class='inner'>"
                 + (f"<ul>{lac}</ul>" if lac else "<p>Nessuna.</p>") + "</div></details>")
    parts.append("<footer>Generata automaticamente da weekly_preview.py. Non è una raccomandazione.</footer>")
    out = week_dir / "anteprima.html"
    out.write_text("<!doctype html><html lang='it'><head><meta charset='utf-8'><meta name='viewport' "
                   f"content='width=device-width,initial-scale=1'><title>Anteprima {tables['week']}</title>"
                   f"<style>{CSS}</style></head><body><main>{''.join(parts)}</main></body></html>")
    return out


def calendar_warning(today: date, rows: list[dict], alerts: Path = ALERTS) -> str | None:
    """Avviso se l'ultima riunione di una banca è a meno di 60 giorni; al massimo uno al giorno.
    Per banca, non sul file: la PBOC copre solo tre mesi e finirebbe in silenzio."""
    last = {}
    for r in rows:
        last[r["bank"]] = max(last.get(r["bank"], r["decision"]), r["decision"])
    bank, end = min(last.items(), key=lambda kv: kv[1])
    if (end - today).days >= 60:
        return None
    msg = (f"Anteprima settimanale: in calendario_banche_centrali.yaml le riunioni {bank} finiscono "
           f"il {end}. Aggiungi le successive dalle pagine ufficiali.")
    seen = alerts.read_text().splitlines() if alerts.exists() else []
    line = f"{today}\t{msg}"
    if line in seen:
        return None
    alerts.parent.mkdir(parents=True, exist_ok=True)
    with alerts.open("a") as fh:
        fh.write(line + "\n")
    return msg


# --- Grafico per il post -----------------------------------------------------

COLORS = {"pos": "#c0392b", "neg": "#2471a3"}


def _asset_names(tickers: list[str]) -> dict[str, str]:
    import sqlite3
    conn = sqlite3.connect(ROOT / "market_data" / "market_data.db")
    try:
        return {tk: (conn.execute("SELECT name FROM assets WHERE ticker=?", (tk,)).fetchone() or [tk])[0]
                for tk in tickers}
    finally:
        conn.close()


def chart_subtitle(event: dict, spec: dict) -> str:
    parts = []
    for d, sc in event["scenarios"].items():
        lab = spec["chart_labels"][d]
        if sc["status"] == "insufficiente":
            parts.append(f"{lab}: too few episodes (N={sc.get('N_min', sc['N'])})")
        else:
            n_min = sc.get("N_min", sc["N"])
            low = f", at least {n_min} per point" if n_min != sc["N"] else ""
            parts.append(f"{lab}: N={sc['N']}{low} ({sc['dates'][0][:4]}–{sc['dates'][-1][:4]})")
    return " · ".join(parts)


def chart(event: dict, spec: dict, out: Path) -> Path:
    """Un'immagine quadrata 1200×1200 per il post: mediana dei due scenari a T+1…T+10 per
    gli asset fissati in `chart`. Solo cifre già in tabella; testi in inglese come il post."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    live = {d: sc for d, sc in event["scenarios"].items() if sc["status"] != "insufficiente"}
    tickers = [tk for tk in spec["chart"] if any(tk in sc["stats"] for sc in live.values())]
    names = _asset_names(tickers)
    fig, axes = plt.subplots(max(len(tickers), 1), 1, figsize=(12, 12), dpi=100, squeeze=False)
    for ax, tk in zip(axes[:, 0], tickers):
        unit = "%"
        for d, sc in live.items():
            row = sc["stats"].get(tk, {})
            pts = [(n, row[str(n)]["median"]) for n in WINDOWS
                   if str(n) in row and row[str(n)]["median"] is not None]
            if not pts:
                continue
            unit = row[str(pts[0][0])].get("unit", "%")
            xs, ys = zip(*pts)
            ax.plot(xs, ys, marker="o", lw=3, ms=8, color=COLORS[d], label=spec["chart_labels"][d])
            ax.annotate(f"{ys[-1]:+.1f}{' bp' if unit == 'bp' else '%'}", (xs[-1], ys[-1]),
                        xytext=(8, 0), textcoords="offset points", va="center",
                        fontsize=13, color=COLORS[d], weight="bold")
        ax.axhline(0, color="#999", lw=1)
        ax.set_title(f"{names[tk]} ({tk})", fontsize=16, loc="left", weight="bold")
        ax.set_ylabel("median change (bp)" if unit == "bp" else "median change (%)", fontsize=12)
        ax.set_xticks(WINDOWS, [f"T+{n}" for n in WINDOWS], fontsize=12)
        ax.set_xlim(0.5, 11.5)
        ax.grid(axis="y", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
    # Una legenda sola sopra i pannelli: dentro i pannelli copriva le linee.
    handles = [plt.Line2D([], [], color=COLORS[d], lw=3, marker="o", ms=8) for d in live]
    fig.legend(handles, [spec["chart_labels"][d] for d in live], loc="upper left",
               bbox_to_anchor=(0.03, 0.865), ncol=2, fontsize=14, frameon=False)
    fig.text(0.03, 0.985, f"{spec['label_en']}, {event['reaction_session']}", fontsize=24,
             weight="bold", va="top")
    fig.text(0.03, 0.947, "What followed past surprises", fontsize=18, va="top")
    fig.text(0.03, 0.912, chart_subtitle(event, spec) + "\nSessions after the event-day close "
             "(the event-day move is not included). Episodes from our own library,\nnot every past release.",
             fontsize=12.5, color="#444", va="top")
    fig.text(0.03, 0.015, "Descriptive statistics, not a forecast. Daily prices: Yahoo Finance.",
             fontsize=12, color="#666")
    fig.tight_layout(rect=(0, 0.04, 1, 0.82))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)
    return out


def charts(week_dir: Path) -> list[Path]:
    tables = json.loads((week_dir / "tabelle.json").read_text())
    events_map = load_events_map()
    return [chart(e, events_map[e["event_type"]], week_dir / f"grafico-{e['event_type']}.png")
            for e in tables["events"] if e["status"] == "ok"]


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--week-of", type=date.fromisoformat, default=date.today())
    b.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    v = sub.add_parser("validate")
    v.add_argument("week_dir", type=Path)
    r = sub.add_parser("render")
    r.add_argument("week_dir", type=Path)
    c = sub.add_parser("charts")
    c.add_argument("week_dir", type=Path)
    sub.add_parser("check-calendar")
    sub.add_parser("target-week")
    a = p.parse_args(argv)
    if a.cmd == "build":
        print(build(a.week_of, a.as_of))
    elif a.cmd == "validate":
        text = a.week_dir / "testo.md"
        problems = validate(text.read_text() if text.exists() else "",
                            json.loads((a.week_dir / "tabelle.json").read_text()))
        for pr in problems:
            print(pr, file=sys.stderr)
        sys.exit(1 if problems else 0)
    elif a.cmd == "render":
        print(render(a.week_dir))
    elif a.cmd == "charts":
        for path in charts(a.week_dir):
            print(path)
    elif a.cmd == "target-week":
        monday = target_week(datetime.now(ROME))
        if monday:
            print(monday)
    elif a.cmd == "check-calendar":
        msg = calendar_warning(date.today(), load_cb_calendar())
        if msg:
            print(msg)


if __name__ == "__main__":
    main()
