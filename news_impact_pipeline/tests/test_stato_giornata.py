#!/usr/bin/env python3
"""
Le sei fasi di `stato_giornata.py` su cartelle sintetiche, piu' i tre guasti veri
che sono passati inosservati e il caso negativo del riuso.

Nessun framework e nessuna fixture: `assert` e un conteggio. Non tocca il DB vero
ne' le cartelle vere — briefing, analisi e database sono tutti costruiti in `tmp`.
"""
import sqlite3
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bootstrap_market_data as bmd
import diagnosi_serie as ds
import parse_briefing as pb
import stato_giornata as sg

GIORNO = "2026-09-16"
OGGI = date.fromisoformat(GIORNO)

_ok = _ko = 0


def verifica(condizione, descrizione):
    global _ok, _ko
    if condizione:
        _ok += 1
    else:
        _ko += 1
        print(f"  FALLITA: {descrizione}")


def fase_di(giorno=GIORNO):
    return sg.stato_giornata(giorno, oggi=OGGI)


# --- costruzione degli artefatti finti --------------------------------------

def scrivi_briefing(cartella: Path, n=3, testo_primo="Il testo della prima notizia."):
    """Un briefing minimo ma vero: il parser vuole <section> + <h2> + .story."""
    def storia(i, corpo):
        return (f'<div class="story"><span class="story-num">{i:02d}</span>'
                f'<h3>Titolo {i}</h3><p>{corpo}</p>'
                f'<p class="source">Source: <a href="https://esempio/{i}">Fonte {i}</a></p></div>')
    intl = "".join(storia(i, testo_primo if i == 1 else f"Corpo intl {i}.")
                   for i in range(1, n + 1))
    fin = "".join(storia(i, f"Corpo fin {i}.") for i in range(1, n + 1))
    html = (f"<html><head><title>Brief {GIORNO}</title></head><body>"
            f"<section><h2>Top {n} International News</h2>{intl}</section>"
            f"<section><h2>Top {n} Economics &amp; Finance News</h2>{fin}</section>"
            f"</body></html>")
    (cartella / f"{GIORNO}-morning-briefing.html").write_text(html, encoding="utf-8")


def scheda(corpo_completo=True):
    testo = "# Scheda\n\n## Event study\n\n"
    if corpo_completo:
        testo += "### Risultati\n\n| T+1 |\n|---|\n| 0.5 |\n\n## Provenance\n- test\n"
    return testo


def tabella(righe):
    """righe: lista di (sez, num, decisione, scheda)."""
    out = ["## Triage", "",
           "| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |",
           "|---|------|---------|-----------|--------------------|--------|"]
    for sez, num, dec, sch in righe:
        link = f"[{sch}]({sch})" if sch else "—"
        out.append(f"| {num} | {sez} | Titolo {int(num)} | {dec} | motivo | {link} |")
    return "\n".join(out)


def scrivi_index(cartella: Path, righe, sintesi="Temi del giorno: test."):
    (cartella / "_index.md").write_text(
        f"# Daily Analysis — {GIORNO}\n\n{tabella(righe)}\n\n"
        f"## Sintesi di sessione\n\n{sintesi}\n", encoding="utf-8")


def scrivi_db(path: Path, ticker="FINTO", ultima=OGGI, fetch=OGGI, source="yfinance",
              sedute=400):
    conn = sqlite3.connect(path)
    bmd.create_database(conn)
    conn.execute("INSERT OR REPLACE INTO assets (ticker, source) VALUES (?, ?)",
                 (ticker, source))
    righe, d, n = [], ultima, 0
    while n < sedute:
        if d.weekday() < 5:
            righe.append((ticker, d.isoformat(), 1.0, 1.0, 1.0, 1.0, 1.0, 1,
                          source, "final", f"{fetch.isoformat()}T09:00:00"))
            n += 1
        d -= timedelta(days=1)
    conn.executemany(bmd.PRICE_INSERT, righe)
    conn.commit()
    conn.close()


class Scenario:
    """Cartelle finte + database finto, con i moduli puntati li' dentro."""

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.brief_dir = base / "brief"
        self.daily = base / "daily"
        self.giorno = self.daily / GIORNO
        self.giorno.mkdir(parents=True)
        self.brief_dir.mkdir()
        self.db = base / "market.db"
        self._orig = (pb.BRIEFING_DIR, sg.DAILY_ANALYSIS_DIR, ds.DB_PATH)
        pb.BRIEFING_DIR = self.brief_dir
        sg.DAILY_ANALYSIS_DIR = self.daily
        ds.DB_PATH = self.db
        return self

    def __exit__(self, *a):
        pb.BRIEFING_DIR, sg.DAILY_ANALYSIS_DIR, ds.DB_PATH = self._orig
        self.tmp.cleanup()


# --- le sei fasi, una alla volta --------------------------------------------

def test_le_sei_fasi_in_ordine():
    with Scenario() as s:
        verifica(fase_di()["fase"] == "input_validato", "briefing assente → input_validato")

        scrivi_briefing(s.brief_dir)
        verifica(fase_di()["fase"] == "dati_pronti", "briefing completo → dati_pronti")

        scrivi_db(s.db)
        verifica(fase_di()["fase"] == "triage_completato", "DB fresco → triage_completato")

        righe = [("intl", "01", "✅", "news_01.md"), ("intl", "02", "✖", ""),
                 ("intl", "03", "✖", ""), ("fin", "01", "✖", ""),
                 ("fin", "02", "✖", ""), ("fin", "03", "✖", "")]
        scrivi_index(s.giorno, righe)
        verifica(fase_di()["fase"] == "schede_validate", "triage chiuso → schede_validate")

        (s.giorno / "news_01.md").write_text(scheda(), encoding="utf-8")
        verifica(fase_di()["fase"] == "html_prodotto", "schede valide → html_prodotto")

        (s.giorno / "report.html").write_text(
            '<section class="doc" id="doc-news_01">x</section>', encoding="utf-8")
        verifica(fase_di()["fase"] == "consegna_confermata", "report reso → consegna_confermata")

        sg.scrivi_stato(GIORNO, {"consegna": {
            "esito": "ok", "quando": "ora", "parziale": False,
            "report_sha": sg.sha_file(s.giorno / "report.html")}})
        verifica(fase_di()["fase"] is None, "ricevuta registrata → giornata completa")


# --- i tre guasti veri ------------------------------------------------------

def test_indice_vuoto_non_passa():
    """Il buco aperto: nessun ⏳ e nessun segnaposto, quindi il vecchio controllo
    lo dava per compilato. Ma non copre nessuna delle notizie in ingresso."""
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        scrivi_db(s.db)
        (s.giorno / "_index.md").write_text("", encoding="utf-8")
        st = fase_di()
        verifica(st["fase"] == "triage_completato", "indice vuoto → si ferma sul triage")
        note = " ".join(st["fasi"][2]["note"])
        verifica("6 notizie del briefing non in tabella" in note,
                 f"l'indice vuoto dice quante notizie mancano (note: {note})")


def test_run_interrotto_a_meta_riusa_le_schede_gia_fatte():
    """L'11/09: limite di sessione a 6 schede su 20, e il ritentativo le rifaceva."""
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        scrivi_db(s.db)
        sg.main(["--date", GIORNO, "--registra-input"])
        righe = [("intl", "01", "✅", "news_01.md"), ("intl", "02", "✅", "news_02.md"),
                 ("intl", "03", "⏳", ""), ("fin", "01", "⏳", ""),
                 ("fin", "02", "⏳", ""), ("fin", "03", "⏳", "")]
        scrivi_index(s.giorno, righe, sintesi="_(nota dell'analista: Da compilare dopo il triage.)_")
        (s.giorno / "news_01.md").write_text(scheda(), encoding="utf-8")
        (s.giorno / "news_02.md").write_text(scheda(corpo_completo=False), encoding="utf-8")
        st = fase_di()
        verifica(st["fase"] == "triage_completato", "righe ⏳ → fermo sul triage")
        verifica(st["schede_riusabili"] == ["news_01.md"],
                 f"si riusa solo la scheda completa (riusabili: {st['schede_riusabili']})")


def test_report_reso_ma_mai_consegnato():
    """Render e invio erano `|| WARN`: fallivano e il run usciva 0 lo stesso."""
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        scrivi_db(s.db)
        righe = [("intl", "01", "✅", "news_01.md")] + \
                [(sz, n, "✖", "") for sz, n in
                 (("intl", "02"), ("intl", "03"), ("fin", "01"), ("fin", "02"), ("fin", "03"))]
        scrivi_index(s.giorno, righe)
        (s.giorno / "news_01.md").write_text(scheda(), encoding="utf-8")
        (s.giorno / "report.html").write_text(
            '<section class="doc" id="doc-news_01">x</section>', encoding="utf-8")
        st = fase_di()
        verifica(st["fase"] == "consegna_confermata", "senza ricevuta → fermo sulla consegna")
        verifica("sconosciuta" in " ".join(st["fasi"][5]["note"]),
                 "la consegna assente è SCONOSCIUTA, non fallita")

        # e una ricevuta che non corrisponde al report sul disco non vale
        sg.scrivi_stato(GIORNO, {"consegna": {"esito": "ok", "quando": "ieri",
                                              "parziale": False, "report_sha": "altro"}})
        verifica(fase_di()["fase"] == "consegna_confermata",
                 "ricevuta di un ALTRO report → non conferma")


def test_report_piu_vecchio_di_una_scheda():
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        scrivi_db(s.db)
        righe = [("intl", "01", "✅", "news_01.md")] + \
                [(sz, n, "✖", "") for sz, n in
                 (("intl", "02"), ("intl", "03"), ("fin", "01"), ("fin", "02"), ("fin", "03"))]
        scrivi_index(s.giorno, righe)
        (s.giorno / "news_01.md").write_text(scheda(), encoding="utf-8")
        rep = s.giorno / "report.html"
        rep.write_text('<section class="doc" id="doc-news_01">x</section>', encoding="utf-8")
        import os
        vecchio = rep.stat().st_mtime - 60
        os.utime(rep, (vecchio, vecchio))
        st = fase_di()
        verifica(st["fase"] == "html_prodotto", "report più vecchio della scheda → da rifare")


# --- caso negativo: il briefing è cambiato ----------------------------------

def test_briefing_cambiato_nessun_riuso():
    """Lo stato è legato all'IDENTITÀ dell'input, non alla data: se il briefing
    viene rigenerato con un altro testo, le schede in cartella non valgono più."""
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        scrivi_db(s.db)
        sg.main(["--date", GIORNO, "--registra-input"])
        righe = [("intl", "01", "✅", "news_01.md")] + \
                [(sz, n, "✖", "") for sz, n in
                 (("intl", "02"), ("intl", "03"), ("fin", "01"), ("fin", "02"), ("fin", "03"))]
        scrivi_index(s.giorno, righe)
        (s.giorno / "news_01.md").write_text(scheda(), encoding="utf-8")
        verifica(fase_di()["schede_riusabili"] == ["news_01.md"],
                 "input immutato → la scheda si riusa")

        scrivi_briefing(s.brief_dir, testo_primo="Testo COMPLETAMENTE diverso.")
        st = fase_di()
        verifica(st["input_riconosciuto"] is False, "briefing riscritto → input non riconosciuto")
        verifica(st["schede_riusabili"] == [], "briefing riscritto → nessun riuso")


# --- dati_pronti: cosa blocca e cosa no -------------------------------------

def test_dati_pronti_blocca_solo_sulle_serie_scaricate():
    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        # nessun aggiornamento oggi: l'ultima scrittura è di ieri
        scrivi_db(s.db, fetch=OGGI - timedelta(days=1))
        st = fase_di()
        verifica(st["fase"] == "dati_pronti", "nessuna riga scritta oggi → blocca")
        verifica("non ha ancora girato" in " ".join(st["fasi"][1]["note"]),
                 "e dice che l'aggiornamento non ha girato")

    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        # serie SCARICATA ferma da 30 giorni, ma riscritta oggi
        scrivi_db(s.db, ticker="VECCHIO", ultima=OGGI - timedelta(days=30))
        st = fase_di()
        verifica(st["fase"] == "dati_pronti", "serie scaricata stantia → blocca")
        verifica(any("[freschezza] VECCHIO" in n for n in st["fasi"][1]["note"]),
                 "e nomina il ticker fermo")

    with Scenario() as s:
        scrivi_briefing(s.brief_dir)
        # stessa serie stantia, ma DERIVATA (assets.source = 'computed'):
        # ha una procedura manuale documentata, quindi è un avviso, non un blocco.
        scrivi_db(s.db, ticker="DERIVATO", ultima=OGGI - timedelta(days=30),
                  source="computed")
        st = fase_di()
        verifica(st["fase"] == "triage_completato", "serie derivata stantia → NON blocca")
        verifica(any("avviso:" in n for n in st["fasi"][1]["note"]),
                 "ma resta segnalata come avviso")


# --- parsing della tabella: le trappole vere --------------------------------

def test_tabella_di_triage_letta_bene():
    testo = ("## Triage\n\n"
             "| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |\n"
             "|---|------|---------|-----------|--------------------|--------|\n"
             "| 01 | intl | Titolo con \\| dentro | ✅ | x | [news_01](news_01.md) |\n"
             "| 01 | fin | Altro titolo | ✖ | y | — |\n\n"
             "## Sintesi di sessione\n\n"
             "### Schede prodotte\n\n"
             "| Scheda | Tema | Asset | N | Esito | Note |\n"
             "|---|---|---|---|---|---|\n"
             "| news_01 | a | b | 9 | c | d |\n")
    righe = sg.righe_triage(testo)
    verifica(len(righe) == 2, f"solo le righe sotto ## Triage ({len(righe)} lette)")
    verifica({r["chiave"] for r in righe} == {"intl/01", "fin/01"},
             "sezione+numero: 01 intl e 01 fin sono notizie diverse")
    verifica(righe[0]["scheda"] == "news_01.md", "il link alla scheda viene estratto")


if __name__ == "__main__":
    for nome, fn in sorted(globals().items()):
        if nome.startswith("test_") and callable(fn):
            print(f"· {nome}")
            fn()
    print("=" * 70)
    print(f"ASSERZIONI: {_ok}   ·   FALLITE: {_ko}")
    print("Tutte verdi." if not _ko else "CI SONO FALLIMENTI.")
    raise SystemExit(1 if _ko else 0)
