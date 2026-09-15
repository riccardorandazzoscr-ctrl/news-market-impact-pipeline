#!/usr/bin/env python3
"""
stato_giornata.py — a che punto e' arrivata la catena giornaliera, e perche' si e'
fermata li'.

Prima di questo file la catena aveva due soli stati — "_index.md compilato" e "non
compilato" — e li usava sia per decidere se c'era lavoro da fare, sia per decidere
se il lavoro era riuscito. Tutto cio' che sta DOPO l'indice (render, invio) era
invisibile: falliva in WARN e il run usciva 0. Al ritentativo, un indice compilato
faceva uscire subito, senza riparare proprio quelle fasi. (R07 della revisione del
2026-09-15; piano in daily_analysis/_reviews/2026-09-15-r07-stati-completamento.md.)

Le sei fasi, in ordine:

    input_validato      il briefing di quel giorno e' arrivato ed e' completo
    dati_pronti         l'aggiornamento prezzi di oggi ha girato e le serie
                        scaricate sono fresche
    triage_completato   _index.md copre TUTTE le notizie in ingresso, ogni riga
                        e' decisa, la sintesi e' scritta
    schede_validate     ogni riga tenuta ha la sua scheda, e la scheda ha dentro
                        i risultati
    html_prodotto       report.html esiste, e' piu' recente di cio' che rende, e
                        contiene un'ancora per ogni scheda
    consegna_confermata c'e' la ricevuta dell'invio, per QUESTO report.html

REGOLA: la verita' e' il disco. Ogni fase si verifica rileggendo gli artefatti.
`_state.json` e' una RICEVUTA, non la fonte: tiene solo cio' che il disco non sa
(l'impronta del briefing usato, le impronte per notizia, l'esito dell'invio). Se
stato e disco divergono, vince il disco. Un `_state.json` assente non e' un errore:
significa "identita' dell'input non registrata" (niente riuso di schede) e
"consegna sconosciuta" — non "consegna fallita". Le giornate gia' in archivio non
ne hanno e non lo avranno: nessuna migrazione.

Uso:
    stato_giornata.py --date 2026-09-16            # leggibile: fase per fase, col perche'
    stato_giornata.py --date 2026-09-16 --fase     # un solo token, per il wrapper
    stato_giornata.py --date 2026-09-16 --json
    stato_giornata.py --date 2026-09-16 --registra-input
    stato_giornata.py --date 2026-09-16 --registra-consegna ok --parziale

Esce 0 se tutte le fasi sono complete, 1 altrimenti (2 su errore d'uso). Il wrapper
legge lo stdout di --fase, non il codice di uscita.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import namedtuple
from datetime import date, datetime
from pathlib import Path

import diagnosi_serie as ds
from parse_briefing import (parse_briefing, briefing_path, impronte,
                            chiave_item, SEZIONE_BREVE)
from pipeline_tools import DAILY_ANALYSIS_DIR

FASI = ("input_validato", "dati_pronti", "triage_completato",
        "schede_validate", "html_prodotto", "consegna_confermata")

# Soglia minima di notizie perche' un briefing sia "pubblicato e non a meta'".
# Stessa variabile d'ambiente del wrapper, cosi' la suite puo' abbassarla.
MIN_STORIES = int(os.environ.get("MIN_STORIES", "1"))

# Marcatori del template di PHASE5_RUNBOOK.md. ⚠ Se cambiano LI', vanno cambiati QUI.
SEGNAPOSTO_SINTESI = "Da compilare dopo il triage"
INTESTAZIONI_SCHEDA = ("### Risultati", "## Provenance")

Esito = namedtuple("Esito", "ok note")

# La scheda referenziata dalla colonna "Scheda": sia la forma con link
# `[news_01](news_01.md)` (quella corrente) sia il nome nudo `news_01`, che due
# giornate di fine giugno usano. Qui la domanda e' "la scheda c'e' ed e' completa",
# non "il link e' ben formato": la forma del link e' materia del renderer (R08).
_LINK_SCHEDA = re.compile(r"\b(news_\d+)(?:\.md)?\b")
_SOLO_TRATTINI = re.compile(r"^:?-+:?$")


# --- Lettura degli artefatti ------------------------------------------------

def cartella_giorno(giorno: str) -> Path:
    return DAILY_ANALYSIS_DIR / giorno


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def leggi_stato(giorno: str) -> dict:
    p = cartella_giorno(giorno) / "_state.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Uno stato illeggibile vale come stato assente: e' una ricevuta, non la
        # fonte. Non si fa fallire una giornata perche' la ricevuta e' strappata.
        return {}


def scrivi_stato(giorno: str, aggiornamento: dict) -> Path:
    d = cartella_giorno(giorno)
    d.mkdir(parents=True, exist_ok=True)
    p = d / "_state.json"
    stato = leggi_stato(giorno)
    stato.update(aggiornamento)
    p.write_text(json.dumps(stato, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    return p


def _celle(riga: str) -> list[str]:
    """Celle di una riga di tabella Markdown, rispettando i `\\|` nel testo.

    I titoli delle notizie contengono pipe sfuggite (le scrive il digest): uno
    split cieco su "|" spezzerebbe la riga nel punto sbagliato."""
    parti = re.split(r"(?<!\\)\|", riga.strip())
    if len(parti) < 3:
        return []
    return [c.strip() for c in parti[1:-1]]


def _sezione_triage(testo: str) -> list[str]:
    """Le sole righe sotto "## Triage", fino all'intestazione di pari livello.

    Serve davvero: la "Sintesi di sessione" contiene spesso una tabella "Schede
    prodotte" a sei colonne, che una scansione dell'intero file conterebbe come
    righe di triage (4 giornate di agosto in archivio)."""
    righe, dentro = [], False
    for riga in testo.splitlines():
        if riga.startswith("## "):
            dentro = riga.strip() == "## Triage"
            continue
        if dentro:
            righe.append(riga)
    return righe


def righe_triage(testo: str) -> list[dict]:
    """Le righe della tabella di triage di _index.md, come record.

    Chiave di una notizia = sezione/numero ("intl/01"): il numero da solo si
    ripete fra le due sezioni del briefing e non identifica niente."""
    out = []
    for riga in _sezione_triage(testo):
        if not riga.lstrip().startswith("|"):
            continue
        c = _celle(riga)
        if len(c) != 6:
            continue
        if c[0] == "#" or all(_SOLO_TRATTINI.match(x) for x in c if x):
            continue
        m = _LINK_SCHEDA.search(c[5])
        # normalizzata al nome del file, comunque fosse scritta nella tabella
        out.append({
            "chiave": f"{c[1]}/{c[0]}",
            "num": c[0],
            "sez": c[1],
            "decisione": c[3],
            "scheda": f"{m.group(1)}.md" if m else "",
        })
    return out


def sintesi_compilata(testo: str) -> bool:
    corpo = testo.split("## Sintesi di sessione", 1)
    if len(corpo) < 2:
        return False
    corpo = corpo[1].strip()
    return bool(corpo) and SEGNAPOSTO_SINTESI not in corpo


def scheda_valida(path: Path) -> bool:
    """Una scheda e' valida se c'e', non e' vuota e porta i risultati.

    Non si giudica il contenuto analitico: si verifica che il flusso sia arrivato
    in fondo, cioe' che l'event study abbia scritto i suoi risultati."""
    if not path.exists() or path.stat().st_size == 0:
        return False
    testo = path.read_text(encoding="utf-8")
    return all(h in testo for h in INTESTAZIONI_SCHEDA)


# --- Le sei fasi ------------------------------------------------------------

def _fase_input(ctx) -> Esito:
    b = ctx["briefing_path"]
    if not b.exists():
        return Esito(False, [f"briefing assente: {b}"])
    if "</body>" not in b.read_text(encoding="utf-8", errors="replace"):
        return Esito(False, ["briefing senza </body>: ancora in scrittura"])
    n = ctx["n_notizie"]
    if n < MIN_STORIES:
        return Esito(False, [f"solo {n} notizie estratte (minimo {MIN_STORIES})"])
    return Esito(True, [f"{n} notizie, impronta {ctx['impronte']['briefing']}"])


def _fase_dati(ctx) -> Esito:
    if not Path(ds.DB_PATH).exists():
        return Esito(False, [f"database assente: {ds.DB_PATH}"])
    conn = sqlite3.connect(f"file:{ds.DB_PATH}?mode=ro", uri=True)
    try:
        oggi = ctx["oggi"]
        # `fetched_at` e' scritto in due formati nel DB ("...T15:53" da yfinance,
        # "... 15:53" dalle serie derivate): confronto per PREFISSO di data, mai ==.
        fresco = conn.execute(
            "SELECT 1 FROM prices WHERE fetched_at LIKE ? LIMIT 1",
            (f"{oggi.isoformat()}%",)).fetchone()
        if not fresco:
            return Esito(False, [
                f"nessuna riga scritta oggi ({oggi}): l'aggiornamento prezzi "
                f"non ha ancora girato, o non ha ottenuto dati"])
        # Le due serie derivate (assets.source = 'computed') hanno una procedura di
        # aggiornamento manuale documentata in references/serie_derivate.md: la loro
        # staleness e' un avviso, non un blocco. Distinzione presa dal registro, non
        # da una lista scritta a mano qui.
        calcolate = {r[0] for r in conn.execute(
            "SELECT ticker FROM assets WHERE source = 'computed'")}
        problemi = ds.diagnostica(conn, oggi)
    finally:
        conn.close()

    bloccanti = [p for p in problemi
                 if p.categoria == "freschezza" and p.ticker not in calcolate]
    avvisi = [p for p in problemi if p not in bloccanti]
    note = [f"avviso: {p.testo.strip()}" for p in avvisi]
    if bloccanti:
        return Esito(False, [p.testo.strip() for p in bloccanti] + note)
    return Esito(True, [f"aggiornamento di {oggi} presente, serie scaricate fresche"] + note)


def _fase_triage(ctx) -> Esito:
    idx = ctx["index_path"]
    if not idx.exists():
        return Esito(False, ["_index.md assente"])
    righe = ctx["righe"]
    attese = set(ctx["impronte"]["items"])
    trovate = {r["chiave"] for r in righe}
    note, blocca = [], False
    # E' QUESTA la verifica che mancava: un _index.md vuoto non ha righe, il
    # briefing ne ha venti, e l'insieme vuoto non coincide. Prima passava.
    if mancanti := sorted(attese - trovate):
        blocca = True
        note.append(f"{len(mancanti)} notizie del briefing non in tabella: "
                    f"{', '.join(mancanti[:5])}")
    # Righe in piu' NON bloccano: il pericolo e' una notizia persa, non una riga
    # aggiunta. Su 106 giornate in archivio l'unico caso e' il 28/08, che aveva
    # messo in tabella anche il box "One Thing to Watch". Segnalarlo basta.
    if intruse := sorted(trovate - attese):
        note.append(f"avviso: {len(intruse)} righe che non corrispondono a nessuna "
                    f"notizia del briefing: {', '.join(intruse[:5])}")
    if pendenti := [r["chiave"] for r in righe
                    if "✅" not in r["decisione"] and "✖" not in r["decisione"]]:
        blocca = True
        note.append(f"{len(pendenti)} righe non decise: {', '.join(pendenti[:5])}")
    if not sintesi_compilata(idx.read_text(encoding="utf-8")):
        blocca = True
        note.append("Sintesi di sessione vuota o ancora col segnaposto")
    if blocca:
        return Esito(False, note)
    return Esito(True, [f"{len(righe)} righe, tutte decise, sintesi scritta"] + note)


def _fase_schede(ctx) -> Esito:
    note = []
    for r in ctx["righe"]:
        if "✅" not in r["decisione"]:
            continue
        if not r["scheda"]:
            note.append(f"{r['chiave']}: tenuta ma senza link alla scheda")
            continue
        if not scheda_valida(ctx["dir"] / r["scheda"]):
            note.append(f"{r['chiave']} → {r['scheda']}: assente, vuota o senza "
                        f"{' / '.join(INTESTAZIONI_SCHEDA)}")
    if note:
        return Esito(False, sorted(set(note)))
    return Esito(True, [f"{len(ctx['schede_attese'])} schede complete"])


def _fase_html(ctx) -> Esito:
    rep = ctx["dir"] / "report.html"
    if not rep.exists():
        return Esito(False, ["report.html assente"])
    note = []
    t_rep = rep.stat().st_mtime
    piu_recenti = [p.name for p in [ctx["index_path"], *ctx["schede_su_disco"]]
                   if p.exists() and p.stat().st_mtime > t_rep]
    if piu_recenti:
        note.append("report.html piu' vecchio di cio' che rende: "
                    + ", ".join(sorted(piu_recenti)))
    testo = rep.read_text(encoding="utf-8", errors="replace")
    senza_ancora = [s for s in sorted(ctx["schede_attese"])
                    if f'id="doc-{Path(s).stem}"' not in testo]
    if senza_ancora:
        note.append("schede non incorporate nel report: " + ", ".join(senza_ancora))
    if note:
        return Esito(False, note)
    return Esito(True, ["report.html aggiornato, tutte le schede incorporate"])


def _fase_consegna(ctx) -> Esito:
    ric = ctx["stato"].get("consegna")
    if not ric:
        # Non "fallita": SCONOSCIUTA. E' la distinzione che vale per tutte le
        # giornate in archivio, che una ricevuta non ce l'hanno e non l'avranno.
        return Esito(False, ["consegna sconosciuta: nessuna ricevuta in _state.json"])
    if ric.get("esito") != "ok":
        return Esito(False, [f"ultimo invio fallito ({ric.get('quando', 'data ignota')})"])
    rep = ctx["dir"] / "report.html"
    if rep.exists() and ric.get("report_sha") != sha_file(rep):
        return Esito(False, ["il report.html sul disco non e' quello spedito: "
                             "rigenerato dopo l'invio"])
    quando = ric.get("quando", "?")
    return Esito(True, [f"consegnato il {quando}"
                        + (" (segnalato PARZIALE)" if ric.get("parziale") else "")])


CONTROLLI = {
    "input_validato": _fase_input,
    "dati_pronti": _fase_dati,
    "triage_completato": _fase_triage,
    "schede_validate": _fase_schede,
    "html_prodotto": _fase_html,
    "consegna_confermata": _fase_consegna,
}


# --- Stato complessivo ------------------------------------------------------

def _contesto(giorno: str, oggi: date) -> dict:
    d = cartella_giorno(giorno)
    idx = d / "_index.md"
    bp = briefing_path(date.fromisoformat(giorno))
    try:
        parsed = parse_briefing(bp)
        imp = impronte(parsed)
        n = sum(len(v) for v in parsed["sections"].values())
    except FileNotFoundError:
        imp, n = {"briefing": "", "items": {}}, 0
    righe = righe_triage(idx.read_text(encoding="utf-8")) if idx.exists() else []
    return {
        "giorno": giorno,
        "oggi": oggi,
        "dir": d,
        "index_path": idx,
        "briefing_path": bp,
        "impronte": imp,
        "n_notizie": n,
        "righe": righe,
        "schede_attese": {r["scheda"] for r in righe
                          if "✅" in r["decisione"] and r["scheda"]},
        "schede_su_disco": sorted(d.glob("news_*.md")),
        "stato": leggi_stato(giorno),
    }


def schede_riusabili(ctx) -> list[str]:
    """Schede che al ritentativo NON vanno rifatte.

    Una scheda si riusa se: l'impronta del briefing registrata coincide con quella
    attuale, TUTTE le righe di triage che la linkano sono tenute e con il testo
    della notizia immutato, e la scheda passa la verifica di contenuto.

    Sull'insieme e non sulla singola notizia perche' il consolidamento e' reale: il
    14/09 le righe 02, 03, 04, 05 e 08 puntano tutte a news_01.md.

    Cambiano solo il TESTO delle notizie, non le dipendenze: `analogues.py build`
    gira all'inizio di ogni run e include le schede appena prodotte, quindi la
    libreria episodi cambia SEMPRE fra un tentativo e il successivo — legarci il
    riuso lo annullerebbe in partenza.
    """
    registrato = ctx["stato"].get("impronte") or {}
    if not registrato or registrato.get("briefing") != ctx["impronte"]["briefing"]:
        return []
    vecchie, nuove = registrato.get("items", {}), ctx["impronte"]["items"]
    per_scheda: dict[str, list[dict]] = {}
    for r in ctx["righe"]:
        if r["scheda"]:
            per_scheda.setdefault(r["scheda"], []).append(r)
    fuori = []
    for scheda, righe in per_scheda.items():
        if any("✅" not in r["decisione"] for r in righe):
            continue
        if any(vecchie.get(r["chiave"]) != nuove.get(r["chiave"]) for r in righe):
            continue
        if scheda_valida(ctx["dir"] / scheda):
            fuori.append(scheda)
    return sorted(fuori)


def stato_giornata(giorno: str, oggi: date | None = None) -> dict:
    ctx = _contesto(giorno, oggi or date.today())
    fasi, prima = [], None
    for nome in FASI:
        esito = CONTROLLI[nome](ctx) if prima is None else Esito(None, ["non valutata"])
        fasi.append({"fase": nome, "ok": esito.ok, "note": esito.note})
        if prima is None and not esito.ok:
            prima = nome
    registrato = (ctx["stato"].get("impronte") or {}).get("briefing")
    return {
        "date": giorno,
        "fase": prima,                      # None = giornata completa
        "fasi": fasi,
        "impronta_briefing": ctx["impronte"]["briefing"],
        "impronta_registrata": registrato,
        "input_riconosciuto": bool(registrato) and registrato == ctx["impronte"]["briefing"],
        "schede_riusabili": schede_riusabili(ctx),
        "schede_attese": sorted(ctx["schede_attese"]),
    }


def formatta(s: dict) -> str:
    simbolo = {True: "✔", False: "✘", None: "·"}
    righe = [f"Giornata {s['date']}"]
    for f in s["fasi"]:
        righe.append(f"  {simbolo[f['ok']]} {f['fase']}")
        for n in f["note"]:
            righe.append(f"      {n}")
    righe.append("")
    if s["fase"] is None:
        righe.append("Completa: niente da fare.")
    else:
        righe.append(f"Prima fase incompleta: {s['fase']}")
    if s["schede_riusabili"]:
        righe.append(f"Schede riusabili al ritentativo ({len(s['schede_riusabili'])}): "
                     + ", ".join(s["schede_riusabili"]))
    elif s["impronta_registrata"] and not s["input_riconosciuto"]:
        righe.append("⚠ Il briefing e' cambiato rispetto a quello registrato: "
                     "nessuna scheda riusabile, la giornata va rifatta da capo.")
    return "\n".join(righe)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="Giornata da esaminare (YYYY-MM-DD). Default: oggi.")
    ap.add_argument("--fase", action="store_true",
                    help="Stampa solo la prima fase incompleta (o 'completa').")
    ap.add_argument("--json", action="store_true", help="Stato completo in JSON.")
    ap.add_argument("--registra-input", action="store_true",
                    help="Registra in _state.json l'impronta del briefing di quel giorno.")
    ap.add_argument("--registra-consegna", choices=["ok", "fallita"],
                    help="Registra la ricevuta dell'invio.")
    ap.add_argument("--parziale", action="store_true",
                    help="Con --registra-consegna: l'analisi spedita era incompleta.")
    args = ap.parse_args(argv)

    giorno = args.date or date.today().isoformat()
    try:
        date.fromisoformat(giorno)
    except ValueError:
        print(f"Data non valida: {giorno} (atteso YYYY-MM-DD)", file=sys.stderr)
        return 2

    if args.registra_input:
        bp = briefing_path(date.fromisoformat(giorno))
        try:
            imp = impronte(parse_briefing(bp))
        except FileNotFoundError as e:
            print(str(e), file=sys.stderr)
            return 1
        p = scrivi_stato(giorno, {"impronte": imp})
        print(f"Impronta {imp['briefing']} ({len(imp['items'])} notizie) in {p}")
        return 0

    if args.registra_consegna:
        rep = cartella_giorno(giorno) / "report.html"
        ric = {
            "esito": args.registra_consegna,
            "quando": datetime.now().isoformat(timespec="seconds"),
            "parziale": bool(args.parziale),
            "report_sha": sha_file(rep) if rep.exists() else "",
        }
        p = scrivi_stato(giorno, {"consegna": ric})
        print(f"Ricevuta di consegna ({ric['esito']}) in {p}")
        return 0

    s = stato_giornata(giorno)
    if args.fase:
        print(s["fase"] or "completa")
    elif args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
    else:
        print(formatta(s))
    return 0 if s["fase"] is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
