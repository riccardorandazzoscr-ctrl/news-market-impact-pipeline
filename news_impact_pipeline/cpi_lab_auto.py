#!/usr/bin/env python3
"""Laboratorio CPI in automatico (job launchd com.riccardo.newsimpact.cpilab).

Gira ogni ora e all'accensione, dopo aver aspettato la rete: un rilascio perso a Mac spento
si recupera al primo giro utile. Ogni esecuzione, idempotente:
1. nel giorno del CPI, prima delle 08:25 ET, chiede alla Wayback Machine una copia del
   calendario MarketWatch (il sito risponde 401 alle richieste dirette);
2. per ogni rilascio uscito e non ancora in archivio scrive il record in events.jsonl:
   valore dal BLS (API pubblica), consenso dall'ultima copia Wayback precedente le 08:30 ET,
   variazioni Fed da FRED con comunicato verificato. Se un pezzo manca il record è
   `excluded` col motivo: la data serve comunque al campione B del protocollo 3.0.0;
3. a 30 rilasci maturi da ottobre 2026 esegue una sola volta il campione B;
4. a meno di 90 giorni dalla fine estende il calendario XNYS di un anno.
Ogni scrittura e ogni anomalia arrivano su Telegram.

    venv/bin/python news_impact_pipeline/cpi_lab_auto.py run [--now ISO]
"""
from __future__ import annotations

import argparse
import calendar as cal_mod
import gzip
import html
import json
import os
import re
import sqlite3
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import cpi_lab

NY = ZoneInfo("America/New_York")
ENV = Path.home() / "Claude" / ".env"
DB = cpi_lab.ROOT / "market_data" / "market_data.db"
PROTOCOL_B = cpi_lab.LAB / "protocols" / "3.0.0-ief-inversione.json"
SAMPLE_B = cpi_lab.LAB / "inversione_campione_B.json"
RESULT_B = cpi_lab.LAB / "inversione_campione_B_esito.json"
B_START, B_SIZE = "2026-10-01", 30
MW_URL = "https://www.marketwatch.com/economy-politics/calendar"
PROVIDER = "MarketWatch (dati Onclusive/Dow Jones), colonna Forecast del calendario economico USA"
BLS_SERIES = "CUSR0000SA0"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) newsimpact-cpilab"
ALERTS = Path(__file__).resolve().parent / "logs" / "cpilab_avvisi.txt"
SNAPSHOT_MAX_AGE = timedelta(days=7)   # la pagina mostra la settimana: oltre, il consenso può essere vecchio


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def env(key):
    if key in os.environ:
        return os.environ[key]
    for line in ENV.read_text().splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip('"')
    raise KeyError(f"{key} mancante in {ENV}")


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def telegram(text):
    try:
        data = urllib.parse.urlencode({"chat_id": env("TELEGRAM_CHAT_ID"), "text": text}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{env('TELEGRAM_BOT_TOKEN')}/sendMessage", data, timeout=30)
    except Exception as exc:   # l'avviso non deve far perdere il record già scritto
        log(f"WARN Telegram: {exc}")


def alert(text, now):
    """Avviso di problema: il job gira ogni ora, quindi lo stesso avviso parte una volta al giorno."""
    key = f"{now.date()} {text}"
    seen = ALERTS.read_text(encoding="utf-8").splitlines() if ALERTS.exists() else []
    if key in seen:
        return
    ALERTS.write_text("\n".join(seen[-50:] + [key]) + "\n", encoding="utf-8")
    telegram(text)


def iso(dt):
    return dt.isoformat(timespec="seconds")


def release_at(d):
    return datetime.combine(d, time(8, 30), NY)


def next_month(ym):
    y, m = map(int, ym.split("-"))
    return f"{y + m // 12}-{m % 12 + 1:02d}"


def next_month_back(ym):
    y, m = map(int, ym.split("-"))
    return f"{y - (m == 1)}-{(m - 2) % 12 + 1:02d}"


# --- fonti -----------------------------------------------------------------

def fred_release_dates():
    url = ("https://api.stlouisfed.org/fred/release/dates?release_id=10&file_type=json"
           f"&include_release_dates_with_no_data=true&sort_order=asc&api_key={env('FRED_API_KEY')}")
    return [date.fromisoformat(r["date"]) for r in json.loads(http_get(url))["release_dates"]]


def bls_indexes():
    """{'2026-09': Decimal('336.298'), ...} e l'ultimo periodo pubblicato."""
    payload = json.loads(http_get(f"https://api.bls.gov/publicAPI/v1/timeseries/data/{BLS_SERIES}"))
    if payload.get("status") != "REQUEST_SUCCEEDED":
        raise ValueError(f"BLS: {payload.get('status')} {payload.get('message')}")
    rows = payload["Results"]["series"][0]["data"]
    idx = {f"{r['year']}-{r['period'][1:]}": Decimal(r["value"]) for r in rows
           if r["period"].startswith("M") and r["value"] != "-"}   # "-": mese senza dati (shutdown ottobre 2025)
    return idx, max(idx)


def mom_change(idx, month):
    """Variazione mensile come la pubblica il BLS: dagli indici a tre decimali, arrotondata a un decimale."""
    pct = (idx[month] / idx[next_month_back(month)] - 1) * 100
    return str(pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def fed_moves(release):
    """Ultime due variazioni del tasso obiettivo prima del rilascio. FRED (DFEDTARU) le registra dal
    giorno in cui hanno effetto, il giorno dopo la decisione: la data si conferma col comunicato Fed."""
    url = ("https://api.stlouisfed.org/fred/series/observations?series_id=DFEDTARU&file_type=json"
           f"&observation_start=2008-12-16&api_key={env('FRED_API_KEY')}")
    obs = [(date.fromisoformat(o["date"]), Decimal(o["value"])) for o in json.loads(http_get(url))["observations"]
           if o["value"] != "."]
    changes = [(d, v - pv) for (pd, pv), (d, v) in zip(obs, obs[1:]) if v != pv]
    moves = []
    for effective, delta in changes:
        decided = effective - timedelta(days=1)
        decision_at = datetime.combine(decided, time(14, 0), NY)
        if decision_at >= release:
            continue
        moves.append((decided, decision_at, delta))
    out = []
    for decided, decision_at, delta in moves[-2:]:
        ref = f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{decided:%Y%m%d}a.htm"
        try:
            http_get(ref, timeout=30)
        except Exception as exc:
            raise ValueError(f"comunicato Fed non trovato per la variazione del {decided} ({exc})") from None
        out.append({"decision_at": iso(decision_at), "change_percentage_points": str(delta.normalize()),
                    "source": {"publisher": "Federal Reserve", "document_ref": ref,
                               "available_at": iso(decision_at), "retrieved_at": None}})
    return out


def parse_calendar(page, release_day, month):
    """Forecast della riga «CPI» del giorno del rilascio, o None. Rifiuta una colonna che non si
    chiami esattamente Forecast: un altro fornitore non si mescola (regola del 2026-10-04)."""
    weekday = release_day.strftime("%A")
    abbr = cal_mod.month_abbr[int(month[5:])].lower()
    in_day, col = False, None
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if "Report" in cells:
            col = cells.index("Forecast") if "Forecast" in cells else None
            continue
        head = re.fullmatch(r"(\w+day), \w+\.? (\d+)", cells[1]) if len(cells) == 2 else None
        if head:
            in_day = head.group(1) == weekday and int(head.group(2)) == release_day.day
            continue
        if in_day and col is not None and len(cells) > col and cells[2] == "CPI" and cells[3].lower().startswith(abbr):
            value = cells[col].rstrip("%")
            return value if re.fullmatch(r"-?\d+(\.\d+)?", value) else None
    return None


def wayback_consensus(release, month):
    """Ultima copia Wayback (HTTP 200) leggibile, non più vecchia di 7 giorni e precedente al rilascio."""
    start = (release - SNAPSHOT_MAX_AGE).astimezone(timezone.utc)
    end = release.astimezone(timezone.utc) - timedelta(seconds=1)
    url = ("https://web.archive.org/cdx/search/cdx?url=marketwatch.com/economy-politics/calendar"
           f"&matchType=prefix&from={start:%Y%m%d%H%M%S}&to={end:%Y%m%d%H%M%S}"
           "&filter=statuscode:200&fl=timestamp,original")
    snaps = sorted((line.split(" ", 1) for line in http_get(url).decode().splitlines() if line.strip()), reverse=True)
    for ts, original in snaps:
        page = http_get(f"https://web.archive.org/web/{ts}id_/{original}").decode("utf-8", "replace")
        value = parse_calendar(page, release.date(), month)
        if value is not None:
            observed = datetime.strptime(ts, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            return value, observed, f"https://web.archive.org/web/{ts}/{original} — riga «CPI», mese {month}"
    return None


def request_snapshot():
    try:
        http_get(f"https://web.archive.org/save/{MW_URL}", timeout=180)
        log("Wayback: copia del calendario richiesta.")
    except Exception as exc:
        log(f"WARN Wayback save: {exc}")


# --- record ----------------------------------------------------------------

def build_record(d, prev, now):
    """Record del rilascio del giorno d, o None se il BLS non ha ancora aggiornato i dati."""
    release = release_at(d)
    month = next_month(prev["reference_month"])
    idx, latest = bls_indexes()
    if latest < month:
        return None
    stamp = iso(now)
    rec = {"schema_version": 1, "event_id": f"us_cpi:{month}", "reference_month": month,
           "release_at": iso(release), "metric": "headline_cpi_mom_sa", "unit": "percentage_points"}
    reasons = []
    if latest > month:
        reasons.append(f"il BLS pubblica già {latest}: valore iniziale di {month} non più leggibile dall'API "
                       "(possibili revisioni) o rilascio di due mesi")
    elif next_month_back(month) not in idx:
        reasons.append(f"il BLS non ha l'indice del mese precedente {next_month_back(month)}: variazione non calcolabile")
    else:
        bulletin = f"https://www.bls.gov/news.release/archives/cpi_{d:%m%d%Y}.htm"
        rec["actual_initial"] = {"value": mom_change(idx, month), "unit": "percentage_points", "source": {
            "publisher": "BLS",
            "document_ref": f"https://api.bls.gov/publicAPI/v1/timeseries/data/{BLS_SERIES} — indici CPI-U SA, "
                            f"variazione {month} su mese precedente arrotondata a un decimale; comunicato {bulletin}",
            "available_at": iso(release), "retrieved_at": stamp}}
    try:
        found = wayback_consensus(release, month)
    except Exception as exc:
        found, reasons = None, reasons + [f"Wayback non raggiungibile: {exc}"]
    if found:
        value, observed, ref = found
        rec["consensus"] = {"value": value, "unit": "percentage_points", "metric": "headline_cpi_mom_sa",
                            "provider": PROVIDER, "observed_at": iso(observed),
                            "source": {"publisher": "Internet Archive (Wayback Machine)", "document_ref": ref,
                                       "available_at": iso(observed), "retrieved_at": stamp}}
    elif not any(r.startswith("Wayback") for r in reasons):
        reasons.append("nessuna copia Wayback del calendario MarketWatch con il consenso, nei 7 giorni prima delle 08:30 ET")
    rec["previous_as_reported"] = None
    rec["fed_history_complete_through"] = iso(release - timedelta(minutes=1))
    try:
        rec["fed_moves"] = fed_moves(release)
        for move in rec["fed_moves"]:
            move["source"]["retrieved_at"] = stamp
    except Exception as exc:
        reasons.append(f"storia Fed: {exc}")
    rec["verification_status"] = "excluded" if reasons else "verified"
    rec["exclusion_reason"] = "; ".join(reasons) or None
    if not reasons:
        problems = cpi_lab._validate_verified_event(rec)
        if problems:
            rec["verification_status"], rec["exclusion_reason"] = "excluded", "; ".join(problems)
    return rec


def write_atomic(path, text):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def append_event(rec, path=cpi_lab.DEFAULT_EVENTS_PATH):
    rows = cpi_lab.load_events(path)
    errors = cpi_lab.validate_events(rows + [rec])
    if errors:
        raise ValueError("record rifiutato dalla validazione: " + "; ".join(errors))
    text = path.read_text(encoding="utf-8")
    write_atomic(path, text.rstrip("\n") + "\n" + json.dumps(rec, ensure_ascii=False) + "\n")


def describe(rec):
    if rec["verification_status"] == "verified":
        return (f"CPI {rec['reference_month']}: {rec['actual_initial']['value']}% contro consenso "
                f"{rec['consensus']['value']}% ({cpi_lab.surprise_band(rec)}), registrato nell'archivio.")
    return f"CPI {rec['reference_month']}: registrato come ESCLUSO. Motivo: {rec['exclusion_reason']}"


# --- campione B e calendario ---------------------------------------------------

def mature_releases(cal, conn, releases):
    last = conn.execute("SELECT MAX(date) FROM prices WHERE ticker='IEF'").fetchone()[0] or ""
    out = []
    for rel in releases:
        try:
            if cpi_lab.market_window(cal, rel, 5, 0)[-1] <= last:
                out.append(rel)
        except cpi_lab.DataUnavailable:
            pass
    return out


def run_sample_b(events, cal, conn, now):
    if RESULT_B.exists():
        return None
    releases = sorted(r["release_at"] for r in events if r["release_at"][:10] >= B_START)
    mature = mature_releases(cal, conn, releases)
    if len(mature) < B_SIZE:
        return None
    chosen = mature[:B_SIZE]
    sample = {"protocol": "3.0.0-ief-inversione", "sample": "B_prospettico",
              "source": {"publisher": "FRED (release 10) e archivio events.jsonl",
                         "document_ref": "date dei rilasci CPI registrate da cpi_lab_auto.py", "retrieved_at": iso(now)},
              "note": f"Primi {B_SIZE} rilasci maturi dal {B_START}; eseguito una sola volta (regola del protocollo).",
              "releases": [{"release_at": r} for r in chosen]}
    res = cpi_lab.reversal_test(cpi_lab._json(PROTOCOL_B), chosen, cal, conn)
    write_atomic(SAMPLE_B, json.dumps(sample, ensure_ascii=False, indent=1) + "\n")
    verdict = "SOSTENUTA" if res["p_one_sided"] is not None and res["p_one_sided"] < 0.05 else "NON sostenuta"
    result = {"executed_at": iso(now), "n": res["n"], "opposite": res["opposite"], "zeros": res["zeros"],
              "p_one_sided": res["p_one_sided"], "excluded": res["excluded"], "verdict_alpha_0_05": verdict}
    write_atomic(RESULT_B, json.dumps(result, ensure_ascii=False, indent=1) + "\n")
    return (f"Protocollo 3.0.0, campione B eseguito: {res['opposite']}/{res['n']} continuazioni opposte, "
            f"p unilaterale {res['p_one_sided']:.3f}, ipotesi {verdict} (alfa 0,05). Il campione A era 27/48, "
            "non sostenuta: per la regola di decisione servono entrambi. Dettagli in experiments/cpi_lab/.")


def extend_calendar(cal, today, now):
    end = date.fromisoformat(cal["coverage_end"])
    if (end - today).days >= 90:
        return None
    import exchange_calendars as xc
    new_end = date(end.year + 1, 12, 31)
    check_start = cal["sessions"][-60]
    x = xc.get_calendar("XNYS", start=(date.fromisoformat(check_start) - timedelta(days=10)).isoformat(),
                        end=new_end.isoformat())
    def closes(a, b):
        return {s.date().isoformat(): x.session_close(s).tz_convert(NY).isoformat()
                for s in x.sessions_in_range(a, b)}
    check = closes(check_start, cal["coverage_end"])
    if list(check) != cal["sessions"][-60:] or any(cal["session_closes"][d] != c for d, c in check.items()):
        raise ValueError("exchange_calendars non riproduce le ultime 60 sedute già in archivio: calendario non esteso")
    added = closes((end + timedelta(days=1)).isoformat(), new_end.isoformat())
    cal["sessions"] += list(added)
    cal["session_closes"].update(added)
    cal["coverage_end"] = cal["sessions"][-1]
    cal["source"]["document_ref"] += f"; esteso al {new_end.year} il {today} (exchange_calendars {xc.__version__})"
    cal["source"]["retrieved_at"] = iso(now)
    cpi_lab.validate_calendar(cal)
    write_atomic(cpi_lab.DEFAULT_CALENDAR_PATH, json.dumps(cal, ensure_ascii=False, indent=1) + "\n")
    return f"Calendario XNYS del laboratorio CPI esteso fino al {cal['coverage_end']} ({len(added)} sedute)."


# --- giro quotidiano ----------------------------------------------------------

def run(now):
    events = cpi_lab.load_events(cpi_lab.DEFAULT_EVENTS_PATH)
    et = now.astimezone(NY)
    dates = fred_release_dates()
    if et.date() in dates and time(5, 0) <= et.time() < time(8, 25):
        request_snapshot()
    last = max(r["release_at"][:10] for r in events)
    for d in dates:
        if d.isoformat() <= last or release_at(d) + timedelta(minutes=5) > now:
            continue
        rec = build_record(d, max(events, key=lambda r: r["release_at"]), now)
        if rec is None:
            log(f"BLS non ha ancora i dati del rilascio del {d}: riprovo al prossimo giro.")
            if now - release_at(d) > timedelta(days=2):
                alert(f"Laboratorio CPI: il BLS non mostra ancora i dati del rilascio del {d}. Controlla.", now)
            break
        append_event(rec)
        events.append(rec)
        log(describe(rec))
        telegram("Laboratorio CPI — " + describe(rec))
    cal = cpi_lab._json(cpi_lab.DEFAULT_CALENDAR_PATH)
    msg = extend_calendar(cal, et.date(), now)
    if msg:
        log(msg)
        telegram("Laboratorio CPI — " + msg)
    with cpi_lab._readonly_db(DB) as conn:
        msg = run_sample_b(events, cal, conn, now)
    if msg:
        log(msg)
        telegram("Laboratorio CPI — " + msg)
    nxt = [d for d in dates if d > et.date()]
    log(f"Fatto. Archivio: {len(events)} record; prossimo rilascio {nxt[0] if nxt else 'non in calendario FRED'}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("run", help="giro quotidiano (job launchd)")
    r.add_argument("--now", help="istante ISO con fuso, per prove")
    args = parser.parse_args(argv)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone.utc)
    try:
        run(now)
        return 0
    except Exception as exc:
        log(f"ERRORE: {exc}")
        alert(f"Laboratorio CPI — errore nel giro automatico: {exc}", now)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
