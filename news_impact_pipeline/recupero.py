#!/usr/bin/env python3
"""
recupero.py — recupero delle direzioni che le research scrivono in prosa.

Contratto: daily_analysis/_reviews/2026-09-21-r04-r01-schema-episodi.md §7.

Le research hanno una tabella di episodi con «Direzione attesa» e «Asset-canale»
scritti in prosa («JPY forte, risk-off»), che il motore non sa leggere: quelle
coppie (data, asset) restano fuori da ogni pool direzionale. Il recupero le
trasforma in dichiarazioni del registro `_direction_reviews.yaml`, SENZA
riscrivere la research (decisione del maintainer, 2026-09-21).

Chi decide cosa:
  - questo script è deterministico: prepara lo scheletro e, dopo, sposta nel
    registro ciò che è stato approvato. Non interpreta la prosa;
  - il verso lo legge l'agente in sessione, riga per riga, **senza aprire il
    DB prezzi**: il verso è la pressione ATTESA all'epoca, e scriverci l'esito
    renderebbe la scorecard una misura della propria copiatura;
  - nel registro entra solo ciò che il maintainer ha approvato. Una riga non
    approvata non viene usata: il sistema resta com'è, mai peggio.

Uso:
  recupero.py prepara "<percorso della research relativo alla KB>"
      → knowledge_base/_recupero/<cartella>.yaml (non sovrascrive un lavoro esistente)
  recupero.py promuovi knowledge_base/_recupero/<cartella>.yaml
      → le voci con `stato: approvata` entrano nel registro; la libreria viene
        ricostruita e, se una revisione è invalida, il registro torna com'era.

Il prefisso `_` della cartella tiene le proposte fuori da catalogo e libreria:
una proposta non può entrare nei pool per sbaglio.
"""

import sqlite3
import sys
from pathlib import Path

import yaml

import kb_metadata
from diagnosi_serie import DB_PATH

KB_DIR = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base"
OUT_DIR = KB_DIR / "_recupero"
REVIEW_PATH = KB_DIR / "_direction_reviews.yaml"
VERSI = {"pos", "neg", "neutral"}


def _tickers() -> set[str]:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        return {r[0] for r in conn.execute("SELECT ticker FROM assets")}
    finally:
        conn.close()


def prepara(rel: str) -> Path:
    path = KB_DIR / rel
    if not path.is_file() or not kb_metadata.is_study(Path(rel).parts):
        raise SystemExit(f"Research non trovata o non indicizzabile: {rel}")
    out = OUT_DIR / f"{Path(rel).parts[0]}.yaml"
    if out.exists():
        raise SystemExit(f"{out} esiste già: è lavoro in corso, non lo sovrascrivo.")
    text = path.read_text(encoding="utf-8")
    theme = (kb_metadata.extract(text) or {}).get("primary_theme", "")
    tick = _tickers()

    voci = []
    for head, rows in kb_metadata.tables(kb_metadata.strip(text)):
        idx = next((i for i, h in enumerate(head)
                    if h.startswith("data") or h == "date"), None)
        if idx is None or head[:5] == kb_metadata.CANON_HEADER:
            continue
        for line, cells in rows:
            data = kb_metadata.cell_date(cells[idx]) if idx < len(cells) else None
            # Candidati = ticker del DB citati nella riga. È solo un promemoria:
            # quali asset dichiarare lo decide chi legge, non questo elenco.
            candidati = sorted(t for t in tick
                               if any(t in c.replace("`", "") for c in cells))
            voci.append({"riga": line.strip(), "data": data, "tema": theme,
                         "fonte": f"kb:{rel}", "candidati": candidati,
                         "dichiarazioni": [], "meccanismo": [], "evento": "",
                         "stato": "da_rivedere"})
    if not voci:
        raise SystemExit(f"Nessuna tabella di episodi in formato libero in {rel}")
    OUT_DIR.mkdir(exist_ok=True)
    out.write_text(yaml.safe_dump({"research": rel, "voci": voci},
                                  sort_keys=False, allow_unicode=True, width=100),
                   encoding="utf-8")
    print(f"{len(voci)} righe → {out}")
    return out


def _righe_registro(voce: dict) -> list[dict]:
    """Le dichiarazioni di una voce approvata, nel formato del registro."""
    out = []
    for dic in voce.get("dichiarazioni") or []:
        verso = dic.get("verso")
        if verso is None:
            continue                 # gruppo 3 ancora aperto: resta fuori
        riga = {"date": voce["data"], "theme": voce["tema"],
                "reference": dic["asset"], "source": voce["fonte"],
                "reason": dic.get("perché", "").strip()}
        if verso == "escluso":
            riga["status"] = "excluded"
        elif verso in VERSI:
            riga["direction"] = verso
        else:
            raise SystemExit(f"{voce['data']} {dic['asset']}: verso '{verso}' "
                             f"non è pos/neg/neutral/escluso")
        if not riga["reason"]:
            raise SystemExit(f"{voce['data']} {dic['asset']}: manca il perché")
        if voce.get("meccanismo"):
            riga["mechanism"] = list(voce["meccanismo"])
        if voce.get("evento"):
            riga["description"] = voce["evento"]
        out.append(riga)
    return out


def promuovi(proposta: Path):
    import analogues   # import tardivo: serve solo qui, per validare ricostruendo

    doc = yaml.safe_load(proposta.read_text(encoding="utf-8"))
    nuove = []
    for voce in doc["voci"]:
        if voce.get("stato") == "approvata":
            nuove += _righe_registro(voce)
    if not nuove:
        print("Nessuna voce approvata: niente da promuovere.")
        return

    prima = REVIEW_PATH.read_text(encoding="utf-8")
    # Si APPENDE testo invece di riscrivere il file: il registro è compilato a
    # mano e ha commenti in testa, che un dump YAML cancellerebbe.
    REVIEW_PATH.write_text(prima.rstrip("\n") + "\n" + yaml.safe_dump(
        nuove, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    try:
        analogues.cmd_build()
    except ValueError as exc:
        REVIEW_PATH.write_text(prima, encoding="utf-8")
        raise SystemExit(f"Revisione invalida, registro ripristinato: {exc}")

    for voce in doc["voci"]:
        if voce.get("stato") == "approvata":
            voce["stato"] = "promossa"
    proposta.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                       width=100), encoding="utf-8")
    print(f"{len(nuove)} dichiarazioni promosse nel registro.")


def _self_check():
    """Check runnabile: `python recupero.py --check`. Niente DB, niente file reali."""
    voce = {"data": "2024-03-19", "tema": "monetary_policy", "fonte": "kb:boj/s.md",
            "meccanismo": ["boj_normalization"], "evento": "Uscita da NIRP e YCC",
            "dichiarazioni": [
                {"asset": "JPY=X", "verso": "neg", "perché": "Stretta: yen atteso più forte."},
                {"asset": "^N225", "domanda": "Verso atteso non scritto nella riga."},
                {"asset": "^VIX", "verso": "escluso", "perché": "Nessuna attesa dichiarata."}]}
    righe = _righe_registro(voce)
    assert [r["reference"] for r in righe] == ["JPY=X", "^VIX"], righe
    assert righe[0]["direction"] == "neg" and "status" not in righe[0]
    assert righe[1]["status"] == "excluded" and "direction" not in righe[1]
    assert righe[0]["mechanism"] == ["boj_normalization"]
    assert righe[0]["description"] == "Uscita da NIRP e YCC"
    for rotta in ({"asset": "X", "verso": "rialzo", "perché": "x"},
                  {"asset": "X", "verso": "pos", "perché": " "}):
        try:
            _righe_registro({**voce, "dichiarazioni": [rotta]})
            raise AssertionError(f"doveva fallire: {rotta}")
        except SystemExit:
            pass
    print("recupero: tutti i check passati")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--check"]:
        _self_check()
    elif len(sys.argv) == 3 and sys.argv[1] == "prepara":
        prepara(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "promuovi":
        promuovi(Path(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
