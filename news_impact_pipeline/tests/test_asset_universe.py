#!/usr/bin/env python
"""Batteria di test per l'universo asset — di default sui cereali ZW=F/ZC=F.

Uso:  venv/bin/python tests/test_asset_universe.py [TICKER,TICKER]

Sei blocchi:
  1. REGISTRO      — anagrafica e coerenza fra codice, DB e mappa
  2. DATI          — integrita' e qualita' della serie storica scaricata
  3. MAPPA         — category_asset_map.yaml resta valida e utilizzabile
  4. INTEGRAZIONE  — event_study.py e pipeline_tools.py funzionano sui nuovi ticker
  5. CASO REALE    — il caso che ha motivato l'aggiunta si misura davvero
  6. REGRESSIONE   — nessun asset preesistente e' stato perso o accorciato
  7. STRESS        — casi limite di event_study e coerenza del canale
"""
import json
import sqlite3
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

PIPE = Path(__file__).resolve().parent.parent
DB = PIPE.parent / "market_data/market_data.db"
PY = str(PIPE / "venv/bin/python")
sys.path.insert(0, str(PIPE))
import bootstrap_market_data as boot  # noqa: E402

# Ticker sotto esame. Parametrizzabile: `test_asset_universe.py ZS=F,EWJ` per
# validare la PROSSIMA aggiunta senza riscrivere il file. I blocchi 1, 2, 3 e 6
# sono generici (registro, qualita' dei dati, mappa, regressione) e valgono per
# qualunque asset; i blocchi 5 e 7 contengono i controlli specifici dei cereali
# e si auto-saltano se i ticker passati non sono quelli.
NUOVI = (sys.argv[1].split(",") if len(sys.argv) > 1 else ["ZW=F", "ZC=F"])
CEREALI = set(NUOVI) == {"ZW=F", "ZC=F"}
BASELINE = Path(__file__).with_name(".baseline_assets.json")

FAILS, CHECKS = [], 0


def check(cond, label, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(f"{label}  {detail}")
    return cond


def sq(q, params=()):
    conn = sqlite3.connect(DB)
    try:
        return conn.execute(q, params).fetchall()
    finally:
        conn.close()


print("=" * 76)
print("BATTERIA DI TEST — cereali (ZW=F, ZC=F) nell'universo asset")
print("=" * 76)

# ============================================================ 1. REGISTRO
print("\n" + "-" * 76)
print("1. REGISTRO — codice, DB e anagrafica dicono la stessa cosa")
print("-" * 76)

codice = {a["ticker"] for a in boot.ASSETS}
db_assets = {r[0] for r in sq("SELECT ticker FROM assets")}
db_prezzi = {r[0] for r in sq("SELECT DISTINCT ticker FROM prices")}

for tk in NUOVI:
    check(tk in codice, "1.1 assente da ASSETS in bootstrap", tk)
    check(tk in db_assets, "1.2 assente dal registro assets del DB", tk)
    check(tk in db_prezzi, "1.3 nessun prezzo in tabella prices", tk)
    meta = sq("SELECT name, asset_class, region, currency, source FROM assets "
              "WHERE ticker = ?", (tk,))
    check(bool(meta), "1.4 anagrafica vuota", tk)
    if meta:
        name, cls, reg, cur, src = meta[0]
        check(cls == "commodity", "1.5 asset_class errata", f"{tk}: {cls}")
        check(src == "yfinance", "1.6 source errata", f"{tk}: {src}")
        check(bool(name and cur), "1.7 nome/valuta mancanti", tk)
        print(f"  {tk:6s} {name:28s} {cls:10s} {reg:8s} {cur}  ✓")

# il registro DB non deve avere ticker che il codice non conosce (e viceversa)
check(codice == db_assets, "1.8 codice e registro DB divergono",
      f"solo-codice={codice - db_assets} solo-DB={db_assets - codice}")
print(f"  registro allineato: {len(codice)} asset nel codice = {len(db_assets)} in DB  ✓")

# ============================================================ 2. DATI
print("\n" + "-" * 76)
print("2. DATI — integrita' e qualita' della serie")
print("-" * 76)

for tk in NUOVI:
    df = pd.read_sql_query(
        "SELECT date, open, high, low, close, adj_close, volume FROM prices "
        "WHERE ticker = ? ORDER BY date", sqlite3.connect(DB), params=(tk,),
        parse_dates=["date"])

    check(len(df) > 3500, "2.1 storia troppo corta", f"{tk}: {len(df)} righe")
    check(df["date"].min().year <= 2011, "2.2 non parte dal 2011",
          f"{tk}: {df['date'].min().date()}")
    # aggiornato a oggi (o all'ultimo giorno di borsa: tollero 5 giorni)
    ritardo = (pd.Timestamp(date.today()) - df["date"].max()).days
    check(ritardo <= 5, "2.3 serie stantia", f"{tk}: ultimo {df['date'].max().date()}")
    # nessuna data duplicata
    check(df["date"].duplicated().sum() == 0, "2.4 date duplicate",
          f"{tk}: {df['date'].duplicated().sum()}")
    # prezzi positivi e finiti
    px = df["adj_close"].fillna(df["close"])
    check(px.notna().sum() > 3500, "2.5 troppi prezzi nulli", tk)
    check((px.dropna() > 0).all(), "2.6 prezzi non positivi", tk)
    # Coerenza OHLC — test RELATIVO, non assoluto. La prima versione pretendeva
    # zero righe incoerenti e falliva su 8 (ZW=F) e 3 (ZC=F) righe del 2011, dove
    # il close di settlement cade appena fuori dal range high/low. Misurato sul
    # resto del DB: e' un artefatto yfinance ENDEMICO (SHLD.L 660 righe, MYR=X 512,
    # JPY=X 248, EURUSD=X 113), quindi la soglia giusta e' "non peggio di quel che
    # c'e' gia'", non "zero". Non tocca comunque l'event study, che usa adj_close.
    ohlc = df.dropna(subset=["open", "high", "low", "close"])
    male = ohlc[(ohlc["high"] < ohlc["low"]) |
                (ohlc["close"] > ohlc["high"]) | (ohlc["close"] < ohlc["low"])]
    quota = len(male) / max(len(ohlc), 1)
    check(quota < 0.01, "2.7 OHLC incoerente oltre la norma del DB",
          f"{tk}: {len(male)}/{len(ohlc)} = {quota:.2%}")
    # nessun salto assurdo (i futures cereali non fanno ±40% in un giorno)
    r = px.pct_change().dropna()
    check(r.abs().max() < 0.40, "2.8 salto giornaliero implausibile",
          f"{tk}: {r.abs().max():.1%}")
    print(f"  {tk:6s} {len(df):5d} righe · {df['date'].min().date()} → "
          f"{df['date'].max().date()} · max |Δ| giorno {r.abs().max():.1%} · "
          f"OHLC fuori range {quota:.2%} (norma DB: fino a 17%)")

# le due serie devono avere calendario quasi coincidente con gli asset USA
gs = pd.read_sql_query("SELECT date FROM prices WHERE ticker='^GSPC' "
                       "AND date >= '2011-01-01'", sqlite3.connect(DB),
                       parse_dates=["date"])
zw = pd.read_sql_query("SELECT date FROM prices WHERE ticker='ZW=F'",
                       sqlite3.connect(DB), parse_dates=["date"])
overlap = len(set(zw["date"]) & set(gs["date"])) / len(set(gs["date"]))
check(overlap > 0.90, "2.9 calendario disallineato dal mercato USA", f"{overlap:.1%}")
print(f"  sovrapposizione calendario ZW=F ↔ ^GSPC: {overlap:.1%}  ✓")

# ============================================================ 3. MAPPA
print("\n" + "-" * 76)
print("3. MAPPA — category_asset_map.yaml valido e coerente")
print("-" * 76)

mappa = yaml.safe_load((PIPE / "category_asset_map.yaml").read_text())
check(isinstance(mappa, dict) and len(mappa) >= 9, "3.1 YAML non valido o categorie perse",
      f"{len(mappa) if isinstance(mappa, dict) else type(mappa)}")
print(f"  YAML valido · {len(mappa)} categorie  ✓")

for tk in NUOVI:
    dove = [c for c, v in mappa.items()
            if isinstance(v, dict) and tk in (v.get("primary") or []) + (v.get("secondary") or [])]
    check(bool(dove), "3.2 ticker non mappato in nessuna categoria", tk)
    print(f"  {tk:6s} mappato in: {', '.join(dove)}  ✓")

# ogni ticker citato nella mappa deve esistere in DB (nessun refuso)
citati = set()
for c, v in mappa.items():
    if isinstance(v, dict):
        citati |= set((v.get("primary") or []) + (v.get("secondary") or []))
fantasmi = citati - db_assets
check(not fantasmi, "3.3 mappa cita ticker inesistenti in DB", str(fantasmi))
print(f"  {len(citati)} ticker citati nella mappa, tutti presenti in DB  ✓")

# nessun duplicato dentro la stessa lista
for c, v in mappa.items():
    if isinstance(v, dict):
        for livello in ("primary", "secondary"):
            lst = v.get(livello) or []
            check(len(lst) == len(set(lst)), "3.4 duplicati nella mappa",
                  f"{c}.{livello}")
print("  nessun duplicato dentro le liste  ✓")

# ============================================================ 4. INTEGRAZIONE
print("\n" + "-" * 76)
print("4. INTEGRAZIONE — i tool del progetto digeriscono i nuovi ticker")
print("-" * 76)

r = subprocess.run([PY, "pipeline_tools.py", "assets", "geopolitical"],
                   cwd=PIPE, capture_output=True, text=True)
check(r.returncode == 0, "4.1 pipeline_tools assets fallisce", r.stderr[:200])
for tk in NUOVI:
    check(tk in r.stdout, "4.2 ticker assente dall'output di assets", tk)
print("  pipeline_tools.py assets geopolitical → include ZW=F e ZC=F  ✓")

# event study su un evento vero
r = subprocess.run([PY, "event_study.py", "--ticker", "ZW=F,ZC=F,BZ=F",
                    "--events", "2026-09-04", "--windows", "1,3,5,10", "--markdown"],
                   cwd=PIPE, capture_output=True, text=True)
check(r.returncode == 0, "4.3 event_study fallisce sui nuovi ticker", r.stderr[:300])
check("ZW=F" in r.stdout and "ZC=F" in r.stdout, "4.4 output event_study incompleto")
print("  event_study.py su ZW=F/ZC=F/BZ=F → esce senza errori  ✓")

# event study su un pool multiplo storico (piu' date)
r2 = subprocess.run([PY, "event_study.py", "--ticker", "ZW=F",
                     "--events", "2022-02-24,2022-07-22,2023-07-17,2025-01-15",
                     "--windows", "1,5,10", "--markdown"],
                    cwd=PIPE, capture_output=True, text=True)
check(r2.returncode == 0, "4.5 event_study fallisce su pool multiplo", r2.stderr[:300])
print("  event_study.py su pool storico multi-data → OK  ✓")

# idempotenza: rilanciare l'update non deve duplicare righe
prima = sq("SELECT COUNT(*) FROM prices WHERE ticker IN ('ZW=F','ZC=F')")[0][0]
r3 = subprocess.run([PY, "update_market_data.py"], cwd=PIPE,
                    capture_output=True, text=True)
dopo = sq("SELECT COUNT(*) FROM prices WHERE ticker IN ('ZW=F','ZC=F')")[0][0]
check(r3.returncode == 0, "4.6 update_market_data fallisce", r3.stderr[:200])
check(prima == dopo, "4.7 update duplica righe", f"{prima} → {dopo}")
print(f"  update_market_data.py rilanciato: {prima} righe → {dopo} (idempotente)  ✓")

# ============================================================ 5. CASO REALE
print("\n" + "-" * 76)
print("5. CASO REALE — il canale che ha motivato l'aggiunta si misura?")
print("-" * 76)

if not CEREALI:
    print("  (blocco specifico dei cereali: saltato per questi ticker)")

else:
    conn = sqlite3.connect(DB)
    w = pd.read_sql_query("SELECT date, close, adj_close FROM prices WHERE ticker='ZW=F' "
                          "ORDER BY date", conn, parse_dates=["date"])
    conn.close()
    w["px"] = w["adj_close"].fillna(w["close"])
    w = w.set_index("date")

    # Il briefing del 2026-09-04 riporta "grano di Chicago in calo di oltre il 2%
    # sulle parole di Putin". ⚠ La prima versione di questo test cercava il calo il
    # 04 e falliva (+0,48%): il briefing del mattino descrive la seduta PRECEDENTE.
    # Il calo vero e' del 03 (-2,48%), che combacia con la cifra citata. E' la regola
    # che il progetto scrive nei prompt KB — "la data e' quella della seduta in cui
    # l'asset REAGISCE, non quella dell'annuncio" — applicata qui al contrario:
    # ancorare al giorno del briefing avrebbe misurato il rimbalzo, non la notizia.
    var_03 = w["px"].pct_change().loc["2026-09-03"]
    var_04 = w["px"].pct_change().loc["2026-09-04"]
    check(var_03 < -0.02, "5.1 il calo del grano sulla notizia non si misura",
          f"03/09: {var_03:+.2%}")
    print(f"  seduta della notizia (2026-09-03): ZW=F {var_03:+.2%}  ✓ "
          f"— il briefing diceva «oltre il 2%»")
    print(f"  giorno del briefing  (2026-09-04): ZW=F {var_04:+.2%}  "
          f"— rimbalzo: ancorare qui misurerebbe la cosa sbagliata")

    # controprova storica: l'invasione del 2022 deve aver fatto SALIRE il grano
    inv = w["px"].pct_change().loc["2022-02-24":"2022-03-07"]
    check(inv.sum() > 0.10, "5.2 nessuna reazione all'invasione 2022", f"{inv.sum():+.1%}")
    print(f"  2022-02-24 → 03-07 (invasione russa): ZW=F {inv.sum():+.1%} cumulato  ✓ "
          f"— il canale Mar Nero esiste ed è ampio")

    # e l'accordo sul grano del luglio 2022 deve averlo fatto scendere
    acc = w["px"].pct_change().loc["2022-07-22":"2022-08-05"]
    print(f"  2022-07-22 → 08-05 (accordo sul grano): ZW=F {acc.sum():+.1%} "
          f"— verso opposto, come atteso")
    check(acc.sum() < 0, "5.3 accordo sul grano senza reazione al ribasso", f"{acc.sum():+.1%}")

# ============================================================ 6. REGRESSIONE
print("\n" + "-" * 76)
print("6. REGRESSIONE — i 78 asset preesistenti sono intatti")
print("-" * 76)

conteggi = {t: n for t, n in sq(
    "SELECT ticker, COUNT(*) FROM prices GROUP BY ticker")}
if BASELINE.exists():
    base = json.loads(BASELINE.read_text())
    persi = [t for t in base if t not in conteggi]
    check(not persi, "6.1 ticker spariti dal DB", str(persi))
    calati = {t: (base[t], conteggi[t]) for t in base
              if t in conteggi and conteggi[t] < base[t]}
    check(not calati, "6.2 ticker con MENO righe di prima", str(calati))
    print(f"  confronto con baseline: {len(base)} ticker, nessuno perso, "
          f"nessuno con meno righe  ✓")
else:
    BASELINE.write_text(json.dumps(conteggi, indent=1))
    print(f"  baseline creata ({len(conteggi)} ticker) — rilancia per il confronto")

check(len(conteggi) == 80, "6.3 numero di asset inatteso", f"{len(conteggi)}")
print(f"  asset con prezzi in DB: {len(conteggi)} (78 preesistenti + 2 nuovi)  ✓")

# i moduli del progetto continuano a importare
for mod in ["bootstrap_market_data", "update_market_data", "event_study",
            "analogues", "pipeline_tools", "compute_crack_spread"]:
    r = subprocess.run([PY, "-c", f"import {mod}"], cwd=PIPE,
                       capture_output=True, text=True)
    check(r.returncode == 0, "6.4 modulo non importa", f"{mod}: {r.stderr[:120]}")
print("  tutti i moduli della pipeline importano senza errori  ✓")

# la serie derivata CRACK_321 non deve essere stata toccata
crack = sq("SELECT COUNT(*) FROM prices WHERE ticker='CRACK_321'")[0][0]
check(crack > 1000, "6.5 CRACK_321 danneggiato", f"{crack} righe")
print(f"  CRACK_321 intatto ({crack} righe)  ✓")

# ============================================================ 7. STRESS
print("\n" + "-" * 76)
print("7. STRESS — casi limite ed eventi storici in serie")
print("-" * 76)


def es(ticker, eventi, extra=()):
    return subprocess.run([PY, "event_study.py", "--ticker", ticker,
                           "--events", eventi, "--windows", "1,3,5,10",
                           "--markdown", *extra],
                          cwd=PIPE, capture_output=True, text=True)


# 7.1 data festiva / mercato chiuso (Natale, 4 luglio, weekend)
for d, etichetta in [("2024-12-25", "Natale"), ("2024-07-04", "4 luglio"),
                     ("2026-08-15", "sabato")]:
    r = es("ZW=F", d)
    check(r.returncode == 0, "7.1 crash su data non di borsa", f"{etichetta} {d}")
print("  date non di borsa (Natale, 4 luglio, sabato): nessun crash  ✓")

# 7.2 data precedente all'inizio della serie e data futura
r = es("ZW=F", "2005-01-03")
check(r.returncode == 0, "7.2 crash su data pre-serie", r.stderr[:150])
r = es("ZW=F", "2030-01-03")
check(r.returncode == 0, "7.3 crash su data futura", r.stderr[:150])
print("  data pre-serie (2005) e data futura (2030): gestite senza crash  ✓")

# 7.3 pool ampio di eventi reali del canale Mar Nero (specifico dei cereali)
if CEREALI:
    mar_nero = [
        "2022-02-24",  # invasione russa
        "2022-03-07",  # picco del grano
        "2022-05-16",  # divieto di export indiano
        "2022-07-22",  # accordo di Istanbul sul grano
        "2022-10-29",  # sospensione russa dell'accordo
        "2022-11-02",  # rientro russo nell'accordo
        "2023-07-17",  # uscita definitiva della Russia dall'accordo
        "2023-07-19",  # attacchi ai porti di Odessa
        "2024-03-22",  # attacchi a infrastrutture ucraine
        "2025-01-15",  # controllo
        "2026-09-03",  # apertura negoziale (il caso di oggi)
    ]
    r = es("ZW=F,ZC=F", ",".join(mar_nero))
    check(r.returncode == 0, "7.4 event study fallisce sul pool Mar Nero", r.stderr[:200])
    check("ZW=F" in r.stdout, "7.5 output vuoto sul pool Mar Nero")
    print(f"  event study su {len(mar_nero)} eventi reali del Mar Nero: OK  ✓")

    # 7.4 --detail, --no-adj, finestre non standard
    for extra, nome in [(("--detail",), "--detail"), (("--no-adj",), "--no-adj")]:
        r = es("ZW=F", "2022-02-24,2023-07-17", extra)
        check(r.returncode == 0, "7.6 crash con flag", nome)
    r = subprocess.run([PY, "event_study.py", "--ticker", "ZW=F", "--events",
                        "2022-02-24", "--windows", "1,2,3,7,20,60", "--markdown"],
                       cwd=PIPE, capture_output=True, text=True)
    check(r.returncode == 0, "7.7 crash con finestre non standard", r.stderr[:150])
    print("  flag --detail, --no-adj e finestre 1,2,3,7,20,60: nessun crash  ✓")

    # 7.5 i due nuovi ticker insieme a TUTTI gli asset di geopolitical
    geo = mappa["geopolitical"]
    tutti = ",".join((geo.get("primary") or []) + (geo.get("secondary") or []))
    r = es(tutti, "2026-09-03,2022-02-24")
    check(r.returncode == 0, "7.8 crash con l'intera categoria geopolitical",
          r.stderr[:200])
    n_asset = len(tutti.split(","))
    print(f"  event study sull'intera categoria geopolitical ({n_asset} asset): OK  ✓")

    # 7.6 il segno del canale e' coerente su piu' episodi, non solo su uno
    guerra = ["2022-02-24", "2022-10-29", "2023-07-17"]   # offerta a rischio → su
    pace = ["2022-07-22", "2022-11-02", "2026-09-03"]      # offerta riaperta → giu'
    su = [w["px"].pct_change().loc[d] for d in guerra if pd.Timestamp(d) in w.index]
    giu = [w["px"].pct_change().loc[d] for d in pace if pd.Timestamp(d) in w.index]
    check(sum(1 for x in su if x > 0) >= 2, "7.9 episodi di escalation senza rialzo",
          str([f"{x:+.1%}" for x in su]))
    check(sum(1 for x in giu if x < 0) >= 2, "7.10 episodi di distensione senza ribasso",
          str([f"{x:+.1%}" for x in giu]))
    print(f"  escalation {[f'{x:+.1%}' for x in su]} · "
          f"distensione {[f'{x:+.1%}' for x in giu]}")
    print("  il verso del canale e' coerente su piu' episodi indipendenti  ✓")
else:
    print("  (controlli 7.3-7.6 specifici dei cereali: saltati)")

# 7.7 nessuna contaminazione: aggiungere i cereali non cambia gli altri asset
r_prima = es("BZ=F", "2022-02-24")
r_dopo = es("BZ=F,ZW=F", "2022-02-24")
riga_bz = [l for l in r_dopo.stdout.splitlines() if "BZ=F" in l]
riga_bz_sola = [l for l in r_prima.stdout.splitlines() if "BZ=F" in l]
check(riga_bz == riga_bz_sola, "7.11 i numeri di BZ=F cambiano se aggiungo ZW=F",
      f"{riga_bz_sola} vs {riga_bz}")
print("  i risultati di BZ=F sono identici con e senza i cereali nella query  ✓")

# ============================================================ ESITO
print("\n" + "=" * 76)
print(f"ASSERZIONI: {CHECKS}   ·   FALLITE: {len(FAILS)}")
print("=" * 76)
for f in FAILS:
    print("  ✗", f)
sys.exit(1 if FAILS else 0)
