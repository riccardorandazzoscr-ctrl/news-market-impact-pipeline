#!/usr/bin/env python3
"""
calendari_riunioni.py — date ufficiali delle decisioni Fed, BCE e BoJ, e verifica delle
date che la libreria attribuisce alle banche centrali (2026-11-02).

Perché esiste: le schede di giugno-settembre 2026 elencavano gli analoghi a memoria e
mettevano riunioni BoJ o BCE nel giorno della FOMC (BoJ «2025-12-10», BCE «2024-12-18»,
entrambe date FOMC). La libreria le ha prese per buone e alcune schede successive le
hanno ricopiate con un verso dichiarato. Le date delle riunioni sono fatti che non
cambiano: si scaricano una volta dalle fonti ufficiali e si confrontano.

Uso:
  calendari_riunioni.py aggiorna            riscarica i calendari → calendari_riunioni.yaml
                                            (ogni gennaio, per le riunioni del nuovo anno)
  calendari_riunioni.py verifica [--dal AAAA-MM-GG]
      episodi con etichetta `boj`/`ecb` su una data che non è (±1 giorno) una riunione di
      quella banca ma è la riunione di un'altra. Con --dal guarda solo le schede da quel
      giorno (il run giornaliero lo lancia sulle sue). Esce con 1 se trova qualcosa.
  calendari_riunioni.py --check             self-check senza rete né file reali

La correzione di una data sbagliata in una scheda passata va in
knowledge_base/_card_exclusions.yaml, con il motivo.
"""

import argparse
import datetime as dt
import re
import sys
import urllib.request
from pathlib import Path

import yaml

FILE = Path(__file__).with_name("calendari_riunioni.yaml")
DAILY = re.compile(r"card:(\d{4}-\d{2}-\d{2})/")
ETICHETTE = {"boj": "boj", "ecb": "bce"}          # token di libreria → calendario
FED = "https://www.federalreserve.gov/monetarypolicy/"
BCE = "https://www.ecb.europa.eu/press/govcdec/mopo/{y}/html/index_include.en.html"
BOJ = ["https://www.boj.or.jp/en/mopo/mpmsche_minu/past.htm",
       "https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm"]
MESI = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MESE = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _testo(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def _giorno(y: int, mese: str, giorni: str) -> str:
    """«Jan/Feb 31-1» → l'ultimo giorno, quello della decisione."""
    return dt.date(y, MESI.index(mese.split("/")[-1][:3]) + 1,
                   int(giorni.split("-")[-1])).isoformat()


def scarica_fed(fino: int) -> set[str]:
    # Le conference call senza decisione restano fuori: non sono riunioni.
    out = set()
    for y in range(2010, fino - 5):            # le pagine storiche hanno ~5 anni di ritardo
        for m in re.finditer(rf"\b({MESE}(?:/{MESE})?) (\d{{1,2}}(?:-\d{{1,2}})?) "
                             r"(?:Meeting|\(unscheduled\))", _testo(_get(f"{FED}fomchistorical{y}.htm"))):
            out.add(_giorno(y, m[1], m[2]))
    parti = re.split(r"(\d{4}) FOMC Meetings", _testo(_get(f"{FED}fomccalendars.htm")))
    for i in range(1, len(parti), 2):
        for m in re.finditer(rf"\b({MESE}(?:/{MESE})?) (\d{{1,2}}(?:-\d{{1,2}})?)\*? "
                             r"(?:\(unscheduled\) )?(?:Statement|Meeting|\(unscheduled\))", parti[i + 1]):
            out.add(_giorno(int(parti[i]), m[1], m[2]))
    return out


def scarica_bce(fino: int) -> set[str]:
    mesi = {m: i + 1 for i, m in enumerate("January February March April May June July "
                                            "August September October November December".split())}
    out = set()
    for y in range(2010, fino + 1):
        for m in re.finditer(r"(\d{1,2}) ([A-Z][a-z]+) (\d{4}) (?:Combined monetary policy decisions"
                             r" and statement|Monetary policy decisions)", _testo(_get(BCE.format(y=y)))):
            out.add(dt.date(int(m[3]), mesi[m[2]], int(m[1])).isoformat())
    return out


def scarica_boj() -> set[str]:
    # Prima colonna della tabella annuale: «Apr. 30 (Wed.), May 1 (Thurs.)» → l'ultimo giorno.
    out = set()
    for url in BOJ:
        for cap in re.finditer(r"Table : (\d{4})</caption>(.*?)</table>", _get(url), re.S):
            for riga in re.findall(r"<tr>(.*?)</tr>", cap[2], re.S):
                td = re.search(r"<td[^>]*>(.*?)</td>", riga, re.S)
                if not td:
                    continue
                mese = giorno = None
                for a, b, c in re.findall(r"(Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)"
                                          r"\.? (\d{1,2})\b|, (\d{1,2}) \(", _testo(td[1])):
                    mese, giorno = (a[:3], int(b)) if a else (mese, int(c))
                if mese:
                    out.add(dt.date(int(cap[1]), MESI.index(mese) + 1, giorno).isoformat())
    return out


def aggiorna():
    anno = dt.date.today().year
    cal = {"fed": scarica_fed(anno), "bce": scarica_bce(anno), "boj": scarica_boj()}
    for k, v in cal.items():
        if len(v) < 8 * (anno - 2010):         # una pagina cambiata di formato dà pochi match
            raise SystemExit(f"{k}: solo {len(v)} date, il formato della fonte è cambiato?")
    testa = (f"# Date delle DECISIONI di politica monetaria (ultimo giorno della riunione), dal 2010.\n"
             f"# Generato da calendari_riunioni.py aggiorna il {dt.date.today()} dalle fonti ufficiali:\n"
             f"# {FED}fomccalendars.htm (+ fomchistoricalAAAA.htm), {BCE.format(y='AAAA')},\n"
             f"# {BOJ[0]}. Fed: riunioni anche straordinarie, non le conference call; BCE: riunioni\n"
             f"# di politica monetaria (non le decisioni d'emergenza fuori riunione). Non modificare a mano.\n")
    FILE.write_text(testa + yaml.safe_dump({k: sorted(v) for k, v in cal.items()}),
                    encoding="utf-8")
    print(", ".join(f"{k} {len(v)}" for k, v in cal.items()), "→", FILE)


def sospetti(eps: list[dict], cal: dict[str, list[str]], dal: str | None = None) -> list[tuple]:
    """(data, tema, etichetta, banca della data, fonte) delle date fuori calendario."""
    cal = {k: set(v) for k, v in cal.items()}
    inizio = min(min(v) for v in cal.values())
    vicino = lambda d, s: any((dt.date.fromisoformat(d) + dt.timedelta(days=k)).isoformat() in s
                              for k in (-1, 0, 1))
    out = set()
    for e in eps:
        if e["date"] < inizio:
            continue
        altre = [b for b, s in cal.items() if e["date"] in s]
        for ev in e.get("events") or []:
            for v in ev.get("evidence") or []:
                m = DAILY.match(v["source"])
                if dal and not (m and m[1] >= dal):
                    continue
                for tok, banca in ETICHETTE.items():
                    if (tok in v["subthemes_local"] and not vicino(e["date"], cal[banca])
                            and (fuori := [b for b in altre if b != banca])):
                        out.add((e["date"], e["theme"], tok, fuori[0], v["source"]))
    return sorted(out)


def verifica(dal: str | None):
    import analogues
    cal = yaml.safe_load(FILE.read_text(encoding="utf-8"))
    righe = sospetti(analogues._load(), cal, dal)
    for d, tema, tok, altra, fonte in righe:
        print(f"{d} {tema}: etichetta `{tok}` ma è una riunione {altra.upper()}, non "
              f"{ETICHETTE[tok].upper()} (±1 giorno) — {fonte}")
    if righe:
        sys.exit(1)
    print("Nessuna data di banca centrale fuori calendario" + (f" dal {dal}." if dal else "."))


def _self_check():
    ev = lambda src, *lbl: {"sources": [src], "evidence": [{"source": src, "subthemes_local": list(lbl)}]}
    cal = {"fed": ["2024-12-18", "2025-12-10"], "bce": ["2024-12-12"], "boj": ["2024-12-19", "2025-12-19"]}
    eps = [
        {"date": "2025-12-10", "theme": "monetary_policy",      # BoJ messa sulla FOMC: sospetto
         "events": [ev("card:2026-06-16/news_01.md", "boj", "rate_decision")]},
        {"date": "2024-12-18", "theme": "monetary_policy",      # BoJ del 19/12: ±1 giorno, regge
         "events": [ev("card:2026-06-16/news_01.md", "boj"),
                    ev("kb:bce/s.md", "ecb")]},                  # BCE del 12/12: sospetto, da KB
        {"date": "2024-05-02", "theme": "monetary_policy",      # nessuna riunione: non si giudica
         "events": [ev("card:2026-09-10/news_06.md", "boj", "fx_intervention")]},
        {"date": "2009-01-01", "theme": "monetary_policy", "events": [ev("kb:x.md", "boj")]},
    ]
    s = sospetti(eps, cal)
    assert [(d, tok, altra) for d, _, tok, altra, _ in s] == [
        ("2024-12-18", "ecb", "fed"), ("2025-12-10", "boj", "fed")], s
    assert [x[0] for x in sospetti(eps, cal, dal="2026-06-16")] == ["2025-12-10"], "solo schede dal"
    assert sospetti(eps, cal, dal="2026-07-01") == []
    assert _giorno(2017, "Jan/Feb", "31-1") == "2017-02-01"
    assert _giorno(2024, "March", "19-20") == "2024-03-20"
    print("calendari_riunioni: tutti i check passati")


if __name__ == "__main__":
    p = argparse.ArgumentParser(usage=__doc__)
    p.add_argument("comando", nargs="?", choices=["aggiorna", "verifica"])
    p.add_argument("--dal", metavar="AAAA-MM-GG")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    if a.check:
        _self_check()
    elif a.comando == "aggiorna":
        aggiorna()
    elif a.comando == "verifica":
        verifica(a.dal)
    else:
        p.error("serve un comando: aggiorna, verifica, o --check")
