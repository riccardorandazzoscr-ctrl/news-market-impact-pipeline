#!/usr/bin/env python3
"""Offline, reproducible CPI release experiment. No production pipeline hooks."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
import tempfile
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "experiments" / "cpi_lab"
DEFAULT_PROTOCOL_PATH = LAB / "protocol.json"
DEFAULT_EVENTS_PATH = LAB / "events.jsonl"
DEFAULT_CALENDAR_PATH = LAB / "calendar.json"
DEFAULT_RUNS_PATH = LAB / "runs"
DEFAULT_EPISODES_PATH = ROOT / "knowledge_base" / "_episodes.yaml"
DEFAULT_PROTOCOL = {
    "protocol_version": "1.0.0",
    "experiment": "US monthly headline CPI, first release vs same-metric consensus",
    "run_type": "historical_replay",
    "asset": "^GSPC",
    "price_column": "adj_close",
    "horizon_sessions": 5,
    "initial_period_start": "2011-01-01",
    "initial_period_end": "2018-12-31",
    "evaluation_start": "2019-01-01",
    "minimum_pool": 10,
    "inline_tolerance_percentage_points": "0.05",
    "current_analogue_subtheme": "inflation_print",
    "current_analogue_theme": "macro_data",
    "current_analogue_max_pool": 30,
    "current_analogue_filter": "strict date-local source evidence; no fallback",
    "condition_fields": ["surprise_band", "fed_regime"],
    "fed_regime_definition": "sign of latest non-zero Fed target change; proxy for decision direction, not policy restrictiveness",
    "price_question": "continuation from release-day close through the fifth following NYSE session; not immediate announcement reaction",
    "calendar_file": "experiments/cpi_lab/calendar.json",
    "calendar_requirement": "complete, explicit XNYS sessions with cited source",
    "vintages": "current adjusted prices are frozen in each replay; historical provider vintages are unavailable unless separately cited",
}


class DataUnavailable(ValueError):
    pass


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _timestamp(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: timestamp ISO-8601 obbligatorio")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field}: timestamp ISO-8601 non valido") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field}: serve un fuso orario")
    return parsed


def _decimal(value, field):
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{field}: valore numerico obbligatorio")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field}: valore numerico non valido") from None
    if not result.is_finite():
        raise ValueError(f"{field}: valore non finito")
    return result


def _source(value, field):
    if not isinstance(value, dict):
        raise ValueError(f"{field}: provenienza obbligatoria")
    for key in ("publisher", "document_ref"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"{field}.{key}: obbligatorio")
    available = _timestamp(value.get("available_at"), f"{field}.available_at")
    retrieved = _timestamp(value.get("retrieved_at"), f"{field}.retrieved_at")
    if retrieved < available:
        raise ValueError(f"{field}: retrieved_at precede available_at")
    return available


def _validate_verified_event(record):
    errors = []
    required = ("actual_initial", "consensus", "previous_as_reported", "fed_moves",
                "fed_history_complete_through")
    for key in required:
        if key not in record:
            errors.append(f"{key} mancante")
    if errors:
        return errors
    try:
        release = _timestamp(record["release_at"], "release_at")
        if record.get("metric") != "headline_cpi_mom_sa":
            raise ValueError("metric deve essere headline_cpi_mom_sa")
        if record.get("unit") != "percentage_points":
            raise ValueError("unit deve essere percentage_points")
        actual = record["actual_initial"]
        if not isinstance(actual, dict) or actual.get("unit", record["unit"]) != "percentage_points":
            raise ValueError("actual_initial deve usare percentage_points")
        actual_at = _source(actual.get("source"), "actual_initial.source")
        if _decimal(actual.get("value"), "actual_initial.value") is None:
            raise ValueError("actual_initial.value mancante")
        if actual_at != release:
            raise ValueError("actual_initial.source.available_at deve coincidere con il primo rilascio")

        consensus = record["consensus"]
        if not isinstance(consensus, dict):
            raise ValueError("consensus deve essere un oggetto verificato")
        if consensus.get("metric") != record["metric"] or consensus.get("unit", record["unit"]) != record["unit"]:
            raise ValueError("consensus metric/unit diversi dalla headline CPI mensile SA")
        if not isinstance(consensus.get("provider"), str) or not consensus["provider"].strip():
            raise ValueError("consensus.provider obbligatorio")
        observed = _timestamp(consensus.get("observed_at"), "consensus.observed_at")
        if observed >= release:
            raise ValueError("consensus osservato dopo o al rilascio")
        consensus_at = _source(consensus.get("source"), "consensus.source")
        if consensus_at > observed:
            raise ValueError("la fonte del consensus risulta disponibile dopo observed_at")
        _decimal(consensus.get("value"), "consensus.value")

        previous = record["previous_as_reported"]
        if previous is not None:
            if not isinstance(previous, dict) or previous.get("unit", record["unit"]) != record["unit"]:
                raise ValueError("previous_as_reported deve usare percentage_points o null")
            _decimal(previous.get("value"), "previous_as_reported.value")
            previous_at = _source(previous.get("source"), "previous_as_reported.source")
            if previous_at > release:
                raise ValueError("previous_as_reported non era disponibile al rilascio")

        moves = record["fed_moves"]
        if not isinstance(moves, list) or (len(moves) != 2 and not (not moves and record.get("fed_history_status") == "unknown")):
            raise ValueError("fed_moves deve contenere le ultime due variazioni, oppure [] con storia Fed verificata come unknown")
        if not moves:
            history_at = _source(record.get("fed_history_source"), "fed_history_source")
            if history_at > release:
                raise ValueError("verifica della storia Fed non disponibile al rilascio")
        last_decisions = []
        for i, move in enumerate(moves):
            decision = _timestamp(move.get("decision_at"), f"fed_moves[{i}].decision_at")
            known = _source(move.get("source"), f"fed_moves[{i}].source")
            change = _decimal(move.get("change_percentage_points"), f"fed_moves[{i}].change_percentage_points")
            if change == 0:
                raise ValueError("fed_moves contiene una variazione nulla")
            if decision >= release or known > release or known < decision:
                raise ValueError("fonte della variazione Fed non disponibile fra decisione e CPI")
            last_decisions.append(decision)
        if last_decisions != sorted(last_decisions):
            raise ValueError("fed_moves deve essere ordinato dal più vecchio al più recente")
        complete = _timestamp(record["fed_history_complete_through"], "fed_history_complete_through")
        if complete > release or (moves and complete < max(last_decisions[-1], _timestamp(moves[-1]["source"]["available_at"], "ultima fonte Fed"))):
            raise ValueError("fed_history_complete_through incoerente con il rilascio")
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(str(exc))
    return errors


def validate_events(records):
    if not isinstance(records, list):
        return ["l'archivio deve contenere una lista di record"]
    errors, seen = [], {}
    for index, record in enumerate(records, 1):
        prefix = f"riga {index}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: record non è un oggetto JSON")
            continue
        try:
            if record.get("schema_version") != 1:
                raise ValueError("schema_version deve essere 1")
            month = record.get("reference_month")
            if not isinstance(month, str) or len(month) != 7 or date.fromisoformat(month + "-01").strftime("%Y-%m") != month:
                raise ValueError("reference_month deve essere YYYY-MM")
            if record.get("event_id") != f"us_cpi:{month}":
                raise ValueError("event_id deve essere us_cpi:<reference_month>")
            _timestamp(record.get("release_at"), "release_at")
            status = record.get("verification_status")
            if status not in ("verified", "excluded"):
                raise ValueError("verification_status deve essere verified o excluded")
            if status == "excluded":
                if not isinstance(record.get("exclusion_reason"), str) or not record["exclusion_reason"].strip():
                    raise ValueError("un record excluded richiede exclusion_reason")
            else:
                problems = _validate_verified_event(record)
                if problems:
                    raise ValueError("; ".join(problems))
            canonical = json.dumps(_json_safe(record), sort_keys=True, ensure_ascii=False)
            eid = record["event_id"]
            if eid in seen:
                kind = "conflitto" if seen[eid] != canonical else "duplicato identico"
                raise ValueError(f"duplicate {kind}: {eid}")
            seen[eid] = canonical
        except (ValueError, TypeError, OverflowError) as exc:
            errors.append(f"{prefix}: {exc}")
    return errors


def verified_events(records):
    return [r for r in records if r.get("verification_status") == "verified"]


def load_events(path):
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: JSON non valido: {exc.msg}") from exc
    errors = validate_events(rows)
    if errors:
        raise ValueError("\n".join(errors))
    return rows


def validate_calendar(cal):
    if not isinstance(cal, dict) or cal.get("schema_version") != 1:
        raise ValueError("calendar: schema_version deve essere 1")
    sessions = cal.get("sessions")
    if not isinstance(sessions, list):
        raise ValueError("calendar.sessions deve essere una lista esplicita di date")
    for d in sessions:
        try:
            if not isinstance(d, str) or date.fromisoformat(d).isoformat() != d:
                raise ValueError(f"data seduta non ISO: {d}")
        except ValueError:
            raise ValueError(f"data seduta non valida: {d}") from None
    if sessions != sorted(set(sessions)):
        raise ValueError("calendar.sessions deve essere ordinato e senza duplicati")
    if sessions:
        if not cal.get("complete"):
            raise ValueError("calendar non dichiarato completo: replay non sicuro")
        if cal.get("exchange") != "XNYS":
            raise ValueError("calendar.exchange deve essere XNYS")
        if cal.get("coverage_start") != sessions[0] or cal.get("coverage_end") != sessions[-1]:
            raise ValueError("coverage_start/end devono coincidere con gli estremi delle sedute")
        _source(cal.get("source"), "calendar.source")
        closes = cal.get("session_closes")
        if not isinstance(closes, dict) or set(closes) != set(sessions):
            raise ValueError("calendar.session_closes deve contenere la chiusura di ogni seduta")
        for day, close_at in closes.items():
            if _timestamp(close_at, f"session_closes.{day}").date().isoformat() != day:
                raise ValueError(f"chiusura XNYS non valida per {day}")
    return []


def market_window(cal, release_at, horizon):
    validate_calendar(cal)
    if not cal["sessions"]:
        raise DataUnavailable("calendario esplicito assente")
    release = _timestamp(release_at, "release_at")
    release_day = release.date().isoformat()
    if release_day < cal["coverage_start"] or release_day > cal["coverage_end"]:
        raise DataUnavailable("data fuori dalla copertura del calendario XNYS")
    sessions = cal["sessions"]
    try:
        index = sessions.index(release_day)
    except ValueError:
        raise DataUnavailable("data rilascio non presente nel calendario XNYS") from None
    if release.astimezone(timezone.utc) >= _timestamp(cal["session_closes"][release_day], f"session_closes.{release_day}").astimezone(timezone.utc):
        raise DataUnavailable("rilascio non precedente alla chiusura XNYS: close dello stesso giorno non è un'ancora valida")
    end = index + horizon + 1
    if end > len(sessions):
        raise DataUnavailable("calendario senza le sedute complete dell'orizzonte")
    return sessions[index:end]


def window_return(prices, window, horizon):
    if len(window) != horizon + 1:
        raise DataUnavailable("numero sedute diverso da ancora + orizzonte")
    values = []
    for day in window:
        value = prices.get(day)
        if value is None:
            raise DataUnavailable(f"prezzo adj_close mancante nella seduta {day}")
        values.append(_decimal(value, f"prezzo {day}"))
    if values[0] <= 0 or values[-1] <= 0:
        raise DataUnavailable("prezzo non positivo")
    return (values[-1] / values[0] - Decimal(1)) * Decimal(100)


def surprise_band(record, protocol=None):
    protocol = protocol or DEFAULT_PROTOCOL
    delta = _decimal(record["actual_initial"]["value"], "actual_initial") - _decimal(record["consensus"]["value"], "consensus")
    tolerance = _decimal(protocol["inline_tolerance_percentage_points"], "inline tolerance")
    return "above" if delta > tolerance else "below" if delta < -tolerance else "inline"


def fed_regime(record):
    moves = record.get("fed_moves") or []
    if not moves:
        return "unknown"
    last = _decimal(moves[-1].get("change_percentage_points"), "Fed move")
    return "last_move_up" if last > 0 else "last_move_down" if last < 0 else "unknown"


def _date_of(record):
    return _timestamp(record["release_at"], "release_at").date().isoformat()


def _event_labels(episode):
    labels = set()
    for ev in episode.get("events") or []:
        witnesses = ev.get("evidence")
        if witnesses is None:
            continue
        for witness in witnesses:
            labels.update(str(x).strip().lower() for x in witness.get("subthemes_local") or [])
    return labels


def _quantile(values, q):
    ordered = sorted(values)
    if not ordered:
        return None
    pos = Decimal(len(ordered) - 1) * Decimal(str(q))
    low = int(pos)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (pos - low)


def _median(values):
    return _quantile(values, Decimal("0.5"))


def _json_safe(value):
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    return value


def _canonical_bytes(value):
    return json.dumps(_json_safe(value), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def _sha(data):
    if isinstance(data, Path):
        data = data.read_bytes()
    elif not isinstance(data, bytes):
        data = _canonical_bytes(data)
    return hashlib.sha256(data).hexdigest()


def _load_prices(conn, ticker, days):
    wanted = sorted(set(days))
    out = {d: None for d in wanted}
    if not wanted:
        return out
    # SQLite's bind-variable limit is lower on older system builds.
    for start in range(0, len(wanted), 800):
        batch = wanted[start:start + 800]
        marks = ",".join("?" for _ in batch)
        try:
            rows = conn.execute(f"SELECT date, adj_close FROM prices WHERE ticker=? AND date IN ({marks})", [ticker, *batch]).fetchall()
        except sqlite3.Error as exc:
            raise ValueError(f"schema prezzi incompatibile: {exc}") from exc
        for d, price in rows:
            out[d] = None if price is None else str(price)
    return out


def _return_if_ready(event_id, windows, prices, horizon):
    window = windows.get(event_id)
    if not window:
        return None
    try:
        return window_return(prices, window, horizon)
    except DataUnavailable:
        return None


def _distribution(pool_ids, return_by_id):
    values = [return_by_id[i] for i in pool_ids if i in return_by_id]
    if not values:
        return None
    return {"median": _median(values), "p25": _quantile(values, Decimal("0.25")),
            "p75": _quantile(values, Decimal("0.75")), "count": len(values)}


def _episode_snapshots(episodes, record_dates, protocol):
    wanted = set(record_dates)
    out = []
    for episode in episodes:
        if episode.get("theme") != protocol["current_analogue_theme"] or episode.get("date") not in wanted:
            continue
        if protocol["current_analogue_subtheme"] not in _event_labels(episode):
            continue
        out.append(episode)
    return sorted(out, key=lambda x: x["date"])


def _methods_for(record, events, returns, windows, current_dates, protocol):
    cutoff = _date_of(record)
    eligible = []
    for prior in events:
        prior_id = prior["event_id"]
        if (prior_id == record["event_id"] or _date_of(prior) >= cutoff
                or _date_of(prior) < protocol["initial_period_start"]):
            continue
        window = windows.get(prior_id)
        if not window or window[-1] >= cutoff or prior_id not in returns:
            continue
        eligible.append(prior)
    surprise = surprise_band(record, protocol)
    regime = fed_regime(record)
    current = [e for e in eligible if _date_of(e) in current_dates]
    current = sorted(current, key=lambda e: _date_of(e))[-int(protocol["current_analogue_max_pool"]):]
    conditioned = [e for e in eligible if surprise_band(e, protocol) == surprise and fed_regime(e) == regime and regime != "unknown"]
    return {
        "reference": eligible,
        "current_analogues": current,
        "conditioned": conditioned,
    }


def _source_text_sha(path):
    return _sha(Path(path)) if path and Path(path).is_file() else None


def create_replay(runs_dir, conn, protocol, records, cal, episodes,
                  code_sha=None, input_sha=None, calendar_sha=None, episodes_sha=None):
    errors = validate_events(records)
    if errors:
        raise ValueError("\n".join(errors))
    validate_calendar(cal)
    active = verified_events(records)
    if active and not cal.get("complete"):
        raise DataUnavailable("record CPI verificati presenti ma manca un calendario XNYS completo e citato")
    asset = protocol["asset"]
    horizon = int(protocol["horizon_sessions"])
    windows, readiness, release_days = {}, {}, {}
    needed_days = []
    for rec in active:
        event_id = rec["event_id"]
        release = _date_of(rec)
        release_days[event_id] = release
        try:
            win = market_window(cal, rec["release_at"], horizon)
            windows[event_id] = win
            needed_days.extend(win)
            readiness[event_id] = "ready"
        except DataUnavailable as exc:
            readiness[event_id] = str(exc)
    prices = _load_prices(conn, asset, needed_days)
    returns = {}
    for rec in active:
        eid = rec["event_id"]
        if readiness[eid] != "ready":
            continue
        try:
            returns[eid] = window_return(prices, windows[eid], horizon)
        except DataUnavailable as exc:
            readiness[eid] = str(exc)

    eval_start = date.fromisoformat(protocol["evaluation_start"] + "-01") if len(protocol["evaluation_start"]) == 7 else date.fromisoformat(protocol["evaluation_start"])
    snapshots = _episode_snapshots(episodes, release_days.values(), protocol)
    current_dates = {x["date"] for x in snapshots}
    decisions = []
    for rec in active:
        eid = rec["event_id"]
        day = release_days[eid]
        if date.fromisoformat(day) < eval_start:
            continue
        if readiness[eid] != "ready":
            decisions.append({"event_id": eid, "cutoff": rec["release_at"], "status": "excluded", "reason": readiness[eid], "methods": {}})
            continue
        pools = _methods_for(rec, active, returns, windows, current_dates, protocol)
        methods = {}
        for name, pool in pools.items():
            ids = [e["event_id"] for e in pool]
            if len(ids) < int(protocol["minimum_pool"]):
                methods[name] = {"status": "abstention", "reason": f"pool {len(ids)} < minimum_pool {protocol['minimum_pool']}", "selected_event_ids": ids}
            else:
                methods[name] = {"status": "selected", "reason": None, "selected_event_ids": ids}
        decisions.append({"event_id": eid, "cutoff": rec["release_at"], "status": "evaluated", "realized_available": True,
                          "surprise_band": surprise_band(rec, protocol), "fed_regime": fed_regime(rec), "methods": methods})
    # All prices and facts used by this run are copied into one immutable input file.
    input_data = {"protocol": protocol, "events": records, "calendar": cal, "price_ticker": asset,
                  "price_column": "adj_close", "price_observations": prices, "windows": windows,
                  "current_analogue_evidence": snapshots,
                  "limitations": ["historical adjusted prices are frozen now; historical provider vintages are not available",
                                  "current_analogues labels are retrospective and cannot establish historical availability"]}
    rid = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    target_root = Path(runs_dir)
    target_root.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".tmp-", dir=target_root))
    final = target_root / rid
    try:
        input_bytes = _canonical_bytes(input_data)
        decision_bytes = b"".join(_canonical_bytes(row) + b"\n" for row in decisions)
        (tmp / "input.json").write_bytes(input_bytes)
        (tmp / "decisions.jsonl").write_bytes(decision_bytes)
        meta = {"run_id": rid, "run_type": "historical_replay", "code_sha256": code_sha or _sha(Path(__file__)),
                "protocol_sha256": _sha(protocol), "events_sha256": input_sha or _sha(records),
                "calendar_sha256": calendar_sha or _sha(cal), "episodes_sha256": episodes_sha or _sha(snapshots),
                "price_snapshot_sha256": _sha(prices), "input_sha256": _sha(input_bytes),
                "decisions_sha256": _sha(decision_bytes), "created_at": datetime.now(timezone.utc).isoformat()}
        (tmp / "meta.json").write_bytes(_canonical_bytes(meta) + b"\n")
        os.replace(tmp, final)
    except Exception:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return final


def _load_run(run_dir):
    path = Path(run_dir)
    meta = _json(path / "meta.json")
    input_bytes = (path / "input.json").read_bytes()
    decision_bytes = (path / "decisions.jsonl").read_bytes()
    if _sha(input_bytes) != meta.get("input_sha256") or _sha(decision_bytes) != meta.get("decisions_sha256"):
        raise ValueError("ricevuta alterata: hash input/decisioni non coincide")
    inp = json.loads(input_bytes)
    decisions = [json.loads(line) for line in decision_bytes.decode().splitlines() if line.strip()]
    return meta, inp, decisions


def _fmt(value, places=2):
    return "n/a" if value is None else f"{float(value):.{places}f}"


def render_report(run_dir):
    meta, inp, decisions = _load_run(run_dir)
    protocol = inp["protocol"]
    records = {r["event_id"]: r for r in inp["events"] if r.get("verification_status") == "verified"}
    returns = {}
    for eid, window in inp["windows"].items():
        try:
            returns[eid] = window_return(inp["price_observations"], window, int(protocol["horizon_sessions"]))
        except DataUnavailable:
            pass
    eval_start = protocol["evaluation_start"]
    eval_records = [r for r in records.values() if _date_of(r) >= eval_start]
    evaluations = [d for d in decisions if d.get("status") == "evaluated" and d["event_id"] in returns]
    excluded = [d for d in decisions if d.get("status") == "excluded"]
    source_excluded = [r for r in inp["events"] if r.get("verification_status") == "excluded" and _date_of(r) >= eval_start]
    rows = {name: [] for name in ("reference", "current_analogues", "conditioned")}
    matured_count = len(evaluations)
    for decision in evaluations:
        actual = returns[decision["event_id"]]
        for name, detail in decision["methods"].items():
            if detail["status"] != "selected":
                continue
            dist = _distribution(detail["selected_event_ids"], returns)
            if dist is not None:
                rows[name].append((actual, dist))
    names = {"reference": "Riferimento CPI", "current_analogues": "Analoghi correnti (retrospettivi)", "conditioned": "Condizionato: sorpresa + ultima variazione Fed"}
    lines = [f"CPI lab · historical_replay · run {meta['run_id']}",
             f"Asset/orizzonte: {protocol['asset']} · chiusura release → T+{protocol['horizon_sessions']} sedute XNYS · prezzo {protocol['price_column']}.",
             "Non misura la reazione intraday. L'archivio prezzi disponibile oggi è congelato; non certifica vintage storiche.",
             "Metodo analoghi correnti: confronto retrospettivo non valido per inferire capacità predittiva, poiché l'ora storica delle etichette/fonti non è provata.",
             f"Eventi verificati nell'input: {len(records)} · release nel periodo: {len(eval_records)} · "
             f"finestra prezzi matura: {matured_count} · esclusi per finestra/calendario: {len(excluded)} · "
             f"esclusi dall'archivio: {len(source_excluded)}.", ""]
    reasons = {}
    for decision in excluded:
        reason = decision.get("reason", "motivo non specificato")
        reasons[reason] = reasons.get(reason, 0) + 1
    for record in source_excluded:
        reason = record.get("exclusion_reason", "motivo non specificato")
        reasons[reason] = reasons.get(reason, 0) + 1
    for reason, count in sorted(reasons.items()):
        lines.append(f"Esclusioni ({count}): {reason}.")
    for name in rows:
        paired = []
        for d in evaluations:
            ref = d["methods"].get("reference", {})
            other = d["methods"].get(name, {})
            if ref.get("status") == "selected" and other.get("status") == "selected":
                paired.append(d["event_id"])
        vals = rows[name]
        if vals:
            errors = [abs(actual - dist["median"]) for actual, dist in vals]
            directional = [(actual, dist["median"]) for actual, dist in vals if actual != 0 and dist["median"] != 0]
            hits = sum((actual > 0) == (med > 0) for actual, med in directional)
            bands = [(actual, dist) for actual, dist in vals if dist["p25"] is not None and dist["p75"] is not None]
            covered = sum(lo <= actual <= hi for actual, dist in bands for lo, hi in [(dist["p25"], dist["p75"])])
            width = sum(dist["p75"] - dist["p25"] for _, dist in bands) / len(bands) if bands else None
            paired_mae = []
            if name != "reference":
                for d in evaluations:
                    if d["event_id"] not in paired:
                        continue
                    actual = returns[d["event_id"]]
                    for method_name in ("reference", name):
                        ids = d["methods"][method_name]["selected_event_ids"]
                        med = _distribution(ids, returns)["median"]
                        paired_mae.append((method_name, abs(actual - med)))
            p_ref = [x[1] for x in paired_mae if x[0] == "reference"]
            p_other = [x[1] for x in paired_mae if x[0] == name]
            pair_txt = (f"paired MAE ref/metodo {_fmt(sum(p_ref)/len(p_ref))}/{_fmt(sum(p_other)/len(p_other))} (N={len(paired)})"
                        if name != "reference" and paired else "nessuna coppia selezionata" if name != "reference" else "baseline")
            abstentions = sum(d["methods"].get(name, {}).get("status") == "abstention" for d in evaluations)
            lines.append(f"{names[name]}: selezioni {len(vals)}/{len(eval_records)} release nel periodo; "
                         f"previsioni mature {len(vals)}/{matured_count}; astensioni pool {abstentions}; MAE mediana {_fmt(sum(errors)/len(errors))} pp; segno {hits}/{len(directional)}; copertura IQR {covered}/{len(bands)}; ampiezza media IQR {_fmt(width)} pp; {pair_txt}.")
        else:
            abstentions = sum(d["methods"].get(name, {}).get("status") == "abstention" for d in evaluations)
            lines.append(f"{names[name]}: dati insufficienti, 0 previsioni mature su {matured_count}; "
                         f"astensioni pool {abstentions}, release nel periodo {len(eval_records)}.")
    if not records:
        lines.append("Dati insufficienti: nessun record CPI verificato con consenso e fonti complete.")
    lines.extend(["", "Metriche descrittive; finestre e eventi sono dipendenti. Quartili empirici, non intervalli di confidenza. La copertura è riportata con il tasso di selezione per rendere visibili le astensioni."])
    return "\n".join(lines) + "\n"


def _load_protocol(path):
    protocol = _json(path)
    missing = set(DEFAULT_PROTOCOL) - set(protocol)
    if missing:
        raise ValueError(f"protocol mancante: {', '.join(sorted(missing))}")
    if protocol["run_type"] != "historical_replay":
        raise ValueError("questa versione esegue solo historical_replay")
    if protocol["asset"] != "^GSPC" or protocol["price_column"] != "adj_close" or int(protocol["horizon_sessions"]) != 5:
        raise ValueError("protocol incompatibile con il perimetro CPI lab v1 (^GSPC, adj_close, T+5)")
    if int(protocol["minimum_pool"]) < 1 or int(protocol["current_analogue_max_pool"]) < 1:
        raise ValueError("minimum_pool e current_analogue_max_pool devono essere positivi")
    date.fromisoformat(protocol["evaluation_start"] + "-01" if len(protocol["evaluation_start"]) == 7 else protocol["evaluation_start"])
    date.fromisoformat(protocol["initial_period_start"])
    date.fromisoformat(protocol["initial_period_end"])
    if protocol["initial_period_start"] > protocol["initial_period_end"] or protocol["initial_period_end"] >= protocol["evaluation_start"]:
        raise ValueError("initial_period deve precedere evaluation_start")
    return protocol


def _read_episodes(path):
    if not path.exists():
        return []
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict) or not isinstance(payload.get("episodes", []), list):
        raise ValueError("libreria analoghi YAML non ha una lista episodes")
    return payload.get("episodes", [])


def _readonly_db(path):
    uri = Path(path).resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.execute("PRAGMA query_only=ON")
    return conn


def _safe_runs(path):
    resolved = Path(path).resolve()
    allowed = DEFAULT_RUNS_PATH.resolve()
    if not resolved.is_relative_to(allowed):
        raise ValueError(f"replay scrive solo dentro {allowed}")
    return resolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="valida l'archivio JSONL")
    validate.add_argument("--events", type=Path, default=DEFAULT_EVENTS_PATH)
    replay = sub.add_parser("replay", help="esegue un replay congelato in sola lettura")
    replay.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    replay.add_argument("--events", type=Path, default=DEFAULT_EVENTS_PATH)
    replay.add_argument("--calendar", type=Path, default=DEFAULT_CALENDAR_PATH)
    replay.add_argument("--episodes", type=Path, default=DEFAULT_EPISODES_PATH)
    replay.add_argument("--db", type=Path, required=True)
    replay.add_argument("--runs", type=Path, default=DEFAULT_RUNS_PATH)
    report = sub.add_parser("report", help="ricalcola e stampa report dalla ricevuta congelata")
    report.add_argument("--run", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            records = load_events(args.events)
            print(f"OK: {len(records)} record, {len(verified_events(records))} verificati, {len(records)-len(verified_events(records))} esclusi")
            return 0
        if args.command == "report":
            print(render_report(args.run), end="")
            return 0
        protocol = _load_protocol(args.protocol)
        records = load_events(args.events)
        cal = _json(args.calendar)
        validate_calendar(cal)
        episodes = _read_episodes(args.episodes)
        if verified_events(records) and not cal.get("complete"):
            raise DataUnavailable("completare calendar.json con una fonte XNYS citata prima del replay")
        with _readonly_db(args.db) as conn:
            run_dir = create_replay(_safe_runs(args.runs), conn, protocol, records, cal, episodes,
                                    input_sha=_source_text_sha(args.events), calendar_sha=_source_text_sha(args.calendar),
                                    episodes_sha=_source_text_sha(args.episodes))
        print(run_dir)
        return 0
    except (OSError, sqlite3.Error, ValueError, KeyError, TypeError) as exc:
        print(f"Errore CPI lab: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
