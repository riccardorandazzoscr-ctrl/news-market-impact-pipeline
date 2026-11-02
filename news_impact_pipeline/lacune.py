#!/usr/bin/env python3
"""
lacune.py — classifica delle lacune di KB e proposte di verso (2026-11-01).

Le lacune si scrivono in "Lacune emerse" di ogni `_index.md` (PHASE5_RUNBOOK.md, passo 4).
Fino a ottobre 2026 erano solo prosa: ~100 in un mese, quasi tutte "aperte", e nessuno
vedeva che erano sempre le stesse. Ora ogni lacuna porta un'etichetta fissa:

    `#lacuna bce-commenti tipo=verso tema=monetary_policy sotto=ecb,hawkish rif=EURUSD=X`

  tipo=studio  manca una research (la scrive il maintainer; slug = nome del prompt in _prompts/)
  tipo=verso   gli episodi ci sono ma non dichiarano il verso su `rif`: si chiude con il
               registro `_direction_reviews.yaml`, senza research (sotto: `verso`).
               `sotto=a,b` = unione dei token, `sotto=a+b` = intersezione (come --match-all)
  tipo=asset   manca il ticker nel DB (references/copertura_asset.md)
  stato=chiusa la lacuna è colmata a quella data; se l'etichetta ricompare dopo, è riaperta

Una riga di triage scartata (✖) per colpa di una lacuna cita solo lo slug: `#lacuna bce-commenti`.
I conteggi non si scrivono da nessuna parte: li produce questo comando.

Uso:
  lacune.py [--tutte] [--al AAAA-MM-GG]   classifica: aperte prima, poi per giorni negli
                                           ultimi 30 e notizie scartate
  lacune.py verso <slug> [...]             per una lacuna tipo=verso, scrive in
      knowledge_base/_recupero/Lacuna <slug>.yaml gli episodi del tema/sotto-tema senza
      verso su `rif`, nel formato di recupero.py. Il verso lo legge l'agente in sessione
      SENZA aprire i prezzi; il maintainer approva; poi `recupero.py promuovi <file>`.
  lacune.py --check                        self-check senza file reali
"""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path.home() / "Claude" / "mercati_finanza"
DAILY_DIR = ROOT / "daily_analysis"
KB_DIR = ROOT / "knowledge_base"
OUT_DIR = KB_DIR / "_recupero"
TAG_RE = re.compile(r"#lacuna ([a-z0-9][a-z0-9-]*)((?:[ \t]+[a-z]+=[^\s`]+)*)")
TIPI = {"studio", "verso", "asset"}


def leggi(testi: dict[str, str]) -> dict[str, dict]:
    """{giorno: testo di _index.md} → {slug: {attr, giorni, scarti, chiusa_il}}."""
    out: dict[str, dict] = {}
    for giorno in sorted(testi):
        for riga in testi[giorno].splitlines():
            for m in TAG_RE.finditer(riga):
                lac = out.setdefault(m[1], {"attr": {}, "giorni": set(), "scarti": [],
                                            "chiusa_il": None})
                attr = dict(kv.split("=", 1) for kv in m[2].split())
                if riga.lstrip().startswith("|"):
                    if "✖" in riga:
                        lac["scarti"].append(giorno)
                    continue
                if attr.get("tipo") and attr["tipo"] not in TIPI:
                    raise SystemExit(f"{giorno} #lacuna {m[1]}: tipo={attr['tipo']} "
                                     f"non è {'/'.join(sorted(TIPI))}")
                lac["attr"].update({k: v for k, v in attr.items() if k != "stato"})
                if attr.get("stato") == "chiusa":
                    lac["chiusa_il"] = giorno
                else:
                    lac["giorni"].add(giorno)
    return out


def aperta(lac: dict) -> bool:
    return not lac["chiusa_il"] or any(g > lac["chiusa_il"] for g in lac["giorni"])


def _testi() -> dict[str, str]:
    return {p.parent.name: p.read_text(encoding="utf-8")
            for p in DAILY_DIR.glob("20??-??-??/_index.md")}


def classifica(tutte: bool, al: str):
    dal = (date.fromisoformat(al) - timedelta(days=30)).isoformat()
    righe = []
    for slug, lac in leggi({g: t for g, t in _testi().items() if g <= al}).items():
        if not tutte and not aperta(lac):
            continue
        a = lac["attr"]
        recenti = sum(dal < g <= al for g in lac["giorni"])
        scarti = sum(dal < g <= al for g in lac["scarti"])
        prompt = "sì" if (KB_DIR / "_prompts" / f"{slug}.md").exists() else "—"
        righe.append((not aperta(lac), -recenti, -scarti, slug,
                      f"| `{slug}` | {a.get('tipo', '?')} | {a.get('tema', '')} | "
                      f"{a.get('rif', '')} | {recenti} | {scarti} | {max(lac['giorni'], default='—')} | "
                      f"{prompt} | {'chiusa ' + lac['chiusa_il'] if not aperta(lac) else 'aperta'} |"))
    print(f"Lacune al {al} (finestra: 30 giorni). Tipo verso = registro dei versi, "
          "non research; tipo asset = copertura_asset.md.\n")
    print("| Lacuna | Tipo | Tema | Rif. | Giorni 30gg | ✖ 30gg | Ultima | Prompt | Stato |")
    print("|---|---|---|---|---:|---:|---|---|---|")
    for *_, riga in sorted(righe):
        print(riga)
    if not righe:
        print("| — | | | | | | | | |")


def _kb_prima(fonti: list[str]) -> list[str]:
    return sorted(dict.fromkeys(fonti), key=lambda s: not s.startswith("kb:"))


def episodi_senza_verso(eps: list[dict], tema: str, sotto: list[str], rif: str,
                        tutti: bool = False) -> tuple[list[tuple[str, list[str]]], str]:
    """(data, fonti candidate, KB prima) degli episodi del tema senza verso né esclusione su `rif`.

    La fonte è quella della descrizione che porta il sotto-tema: un episodio è una
    data, e sotto la stessa data possono stare eventi diversi (una riunione BoJ e
    una BCE). La revisione si aggancia all'evento della sua fonte, quindi deve
    essere la fonte giusta. `tutti`: i token in intersezione (`sotto=a+b`).
    """
    del_tema = [e for e in eps if e["theme"] == tema]
    pool = [e for e in del_tema
            if rif not in (e.get("directions_by_reference") or {})
            and rif not in (e.get("direction_review_excluded") or {})]
    test = all if tutti else any
    porta = lambda etichette: test(any(w in st for st in etichette or []) for w in sotto)
    tutte_le_fonti = lambda e: [s for ev in e.get("events") or [] for s in ev["sources"]]
    if not sotto:
        return [(e["date"], _kb_prima(tutte_le_fonti(e))) for e in pool], "tema"
    # Come in `find`: prima le etichette della singola descrizione, poi del documento.
    # Si scende al documento solo se il sotto-tema non esiste in locale: se esiste ed è
    # già tutto dichiarato, la lacuna di verso è chiusa, non va allargata.
    fonti_locali = lambda e: [v["source"] for ev in e.get("events") or []
                              for v in ev.get("evidence") or [] if porta(v.get("subthemes_local"))]
    if any(fonti_locali(e) for e in del_tema):
        return ([(e["date"], _kb_prima(f)) for e in pool if (f := fonti_locali(e))],
                "sotto-tema locale")
    return ([(e["date"], _kb_prima(tutte_le_fonti(e))) for e in pool if porta(e.get("subthemes"))],
            "sotto-tema del documento")


def _testo(fonte: str) -> str:
    path = (KB_DIR / fonte[3:]) if fonte.startswith("kb:") else (DAILY_DIR / fonte[5:])
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _riga_della_fonte(fonte: str, giorno: str) -> str:
    return next((r.strip()[:300] for r in _testo(fonte).splitlines() if giorno in r), "")


def verso(slug: str):
    import analogues   # import tardivo: la classifica non ha bisogno della libreria

    lac = leggi(_testi()).get(slug)
    if lac is None:
        raise SystemExit(f"Nessuna etichetta `#lacuna {slug}` nelle giornate.")
    a = lac["attr"]
    if a.get("tipo") != "verso" or not a.get("tema") or not a.get("rif"):
        raise SystemExit(f"{slug}: serve tipo=verso con tema= e rif= (trovato: {a})")
    out = OUT_DIR / f"Lacuna {slug}.yaml"
    if out.exists():
        raise SystemExit(f"{out} esiste già: è lavoro in corso, non lo sovrascrivo.")
    tutti = "+" in a.get("sotto", "")
    sotto = [analogues._norm_label(s) for s in re.split(r"[,+]", a.get("sotto", "")) if s]
    eps, livello = episodi_senza_verso(analogues._load(), a["tema"], sotto, a["rif"], tutti)
    if not eps:
        print(f"{slug}: nessun episodio senza verso su {a['rif']} ({livello}): o i versi "
              "sono già dichiarati (chiudila) o mancano gli episodi (tipo=studio).")
        return
    voci, scartati = [], []
    for giorno, fonti in sorted(eps, reverse=True):
        # Il registro accetta una scheda solo se DICHIARA la data fra i suoi analoghi
        # (analogues.declared_episodes): la libreria ne legge anche altre, citate in prosa.
        fonte = next((f for f in fonti if f.startswith("kb:") or giorno in
                      analogues.declared_episodes(_testo(f))), None)
        if fonte is None:
            scartati.append(giorno)
            continue
        voci.append({
            "data": giorno, "tema": a["tema"],
            # Il registro vuole la scheda senza prefisso (`2026-08-31/news_01.md`).
            "fonte": fonte[5:] if fonte.startswith("card:") else fonte,
            "riga": _riga_della_fonte(fonte, giorno),
            "evento": "", "meccanismo": [],
            "dichiarazioni": [{"asset": a["rif"],
                               "domanda": "Pressione ATTESA all'epoca su questo asset? "
                                          "pos/neg/neutral/escluso + perché; niente prezzi."}],
            "stato": "da_rivedere"})
    OUT_DIR.mkdir(exist_ok=True)
    out.write_text(yaml.safe_dump(
        {"research": f"lacuna {slug} ({a['tema']}, {a.get('sotto') or 'tutto il tema'}, "
                     f"rif {a['rif']}; {livello})", "voci": voci},
        sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"{len(voci)} episodi senza verso su {a['rif']} ({livello}) → {out}"
          + (f"; {len(scartati)} senza una fonte che il registro accetti: {', '.join(scartati)}"
             if scartati else ""))


def _self_check():
    testi = {
        "2026-10-07": "| 03 | fin | X | ✖ | pool vuoto `#lacuna bce-commenti` |\n"
                      "- **BCE** `#lacuna bce-commenti tipo=verso tema=monetary_policy "
                      "sotto=ecb rif=EURUSD=X`\n",
        "2026-10-14": "- **BCE** `#lacuna bce-commenti`\n"
                      "- **Midterm** `#lacuna midterm-usa tipo=studio tema=geopolitical`\n",
        "2026-10-20": "- chiusa `#lacuna midterm-usa stato=chiusa`\n"
                      "- **Uragani** `#lacuna uragani tipo=studio stato=chiusa`\n",
        "2026-10-25": "- di nuovo `#lacuna uragani`\n",
    }
    lac = leggi(testi)
    b = lac["bce-commenti"]
    assert b["giorni"] == {"2026-10-07", "2026-10-14"} and b["scarti"] == ["2026-10-07"], b
    assert b["attr"] == {"tipo": "verso", "tema": "monetary_policy", "sotto": "ecb",
                         "rif": "EURUSD=X"}, b["attr"]
    assert aperta(b)
    assert not aperta(lac["midterm-usa"]), "chiusa dopo l'ultima occorrenza"
    assert aperta(lac["uragani"]), "ricomparsa dopo la chiusura: riaperta"
    try:
        leggi({"2026-10-01": "`#lacuna x tipo=boh`"})
        raise AssertionError("tipo invalido accettato")
    except SystemExit:
        pass

    ev = lambda src, *lbl: {"sources": [src], "evidence": [{"source": src, "subthemes_local": list(lbl)}]}
    eps = [
        # Stessa data, due eventi: la fonte giusta è quella della BCE, non della BoJ.
        {"date": "2024-06-06", "theme": "monetary_policy", "subthemes": ["ecb", "boj"],
         "events": [ev("card:2026-06-16/news_01.md", "boj"), ev("kb:bce/s.md", "ecb", "hawkish")]},
        {"date": "2024-07-18", "theme": "monetary_policy", "subthemes": ["ecb"],
         "events": [ev("kb:bce/s.md", "ecb")], "directions_by_reference": {"EURUSD=X": ["neg"]}},
        {"date": "2024-09-12", "theme": "monetary_policy", "subthemes": ["ecb"],
         "events": [ev("kb:bce/s.md", "ecb")], "direction_review_excluded": {"EURUSD=X": "x"}},
        {"date": "2024-10-17", "theme": "monetary_policy", "subthemes": ["ecb", "fomc"],
         "events": [ev("card:2026-07-01/news_02.md", "fomc")]},
        {"date": "2024-03-19", "theme": "macro_data", "events": [ev("kb:x.md", "ecb")]},
    ]
    pool, liv = episodi_senza_verso(eps, "monetary_policy", ["ecb"], "EURUSD=X")
    assert pool == [("2024-06-06", ["kb:bce/s.md"])] and liv == "sotto-tema locale", pool
    pool, _ = episodi_senza_verso(eps, "monetary_policy", ["ecb", "fomc"], "EURUSD=X", tutti=True)
    assert pool == [("2024-10-17", ["card:2026-07-01/news_02.md"])], "AND locale vuoto → documento"
    assert _kb_prima(["card:2026-08-31/news_01.md", "kb:a/b.md"]) == ["kb:a/b.md", "card:2026-08-31/news_01.md"]
    pool, liv = episodi_senza_verso(eps, "monetary_policy", ["rba"], "EURUSD=X")
    assert pool == [] and liv == "sotto-tema del documento"
    pool, liv = episodi_senza_verso(eps[1:3], "monetary_policy", ["ecb"], "EURUSD=X")
    assert pool == [] and liv == "sotto-tema locale", "tutto dichiarato: niente ripiego"
    print("lacune: tutti i check passati")


if __name__ == "__main__":
    p = argparse.ArgumentParser(usage=__doc__)
    p.add_argument("comando", nargs="*", help="vuoto = classifica; `verso <slug> [...]`")
    p.add_argument("--tutte", action="store_true", help="anche le lacune chiuse")
    p.add_argument("--al", default=date.today().isoformat(), metavar="AAAA-MM-GG")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    if a.check:
        _self_check()
    elif a.comando[:1] == ["verso"] and len(a.comando) > 1:
        for s in a.comando[1:]:
            verso(s)
    elif not a.comando:
        classifica(a.tutte, a.al)
    else:
        p.error(f"comando sconosciuto: {' '.join(a.comando)}")
