#!/usr/bin/env python3
"""
bootstrap_market_data.py

Scarica circa 15 anni di prezzi giornalieri per l'universo asset del progetto
"News-to-Market Impact Pipeline" e li salva in un database SQLite.

Questo script si esegue UNA SOLA VOLTA, per costruire il database da zero.
Per gli aggiornamenti quotidiani useremo un altro script (update incrementale).

Come si esegue (dal Terminale, dentro la cartella del progetto):
    venv/bin/python bootstrap_market_data.py
"""

from pathlib import Path
from datetime import date
import sqlite3
import time

import pandas as pd
import yfinance as yf


# --- 1. Dove salviamo il database -------------------------------------------
# Path.home() e' la tua cartella utente (la home dell'utente). Cosi' costruiamo il
# percorso ~/Claude/mercati_finanza/market_data/market_data.db senza scrivere indirizzi a mano.
DB_DIR = Path.home() / "Claude" / "mercati_finanza" / "market_data"
DB_PATH = DB_DIR / "market_data.db"

# Periodo storico da scaricare: dal 1 gennaio 2011 a oggi.
START_DATE = "2011-01-01"
END_DATE = date.today().isoformat()  # oggi, in formato AAAA-MM-GG


# --- 2. L'universo degli asset ----------------------------------------------
# Ogni asset e' un dizionario con la sua anagrafica.
# "download": True  -> scaricabile subito da yfinance.
# "download": False -> lo riempiremo piu' avanti con la fonte FRED (lo spread
#                      BTP-Bund non e' scaricabile direttamente da yfinance).
ASSETS = [
    # --- Indici azionari (equity) ---
    {"ticker": "^GSPC",       "name": "S&P 500",                "asset_class": "equity",       "region": "US",       "currency": "USD", "source": "yfinance", "description": "Benchmark azionario USA",              "download": True},
    {"ticker": "^STOXX50E",   "name": "Euro Stoxx 50",          "asset_class": "equity",       "region": "eurozone", "currency": "EUR", "source": "yfinance", "description": "Blue chip Eurozona",                  "download": True},
    {"ticker": "FTSEMIB.MI",  "name": "FTSE MIB",               "asset_class": "equity",       "region": "italy",    "currency": "EUR", "source": "yfinance", "description": "Indice azionario Italia",             "download": True},
    {"ticker": "^GDAXI",      "name": "DAX",                    "asset_class": "equity",       "region": "germany",  "currency": "EUR", "source": "yfinance", "description": "Indice azionario Germania",           "download": True},
    {"ticker": "^N225",       "name": "Nikkei 225",             "asset_class": "equity",       "region": "japan",    "currency": "JPY", "source": "yfinance", "description": "Indice azionario Giappone",           "download": True},

    # --- Reddito fisso (fixed income) ---
    {"ticker": "^TNX",        "name": "US Treasury 10Y yield",  "asset_class": "fixed_income", "region": "US",       "currency": "USD", "source": "yfinance", "description": "Rendimento Treasury USA 10 anni",     "download": True},
    {"ticker": "IEF",         "name": "iShares 7-10Y Treasury", "asset_class": "fixed_income", "region": "US",       "currency": "USD", "source": "yfinance", "description": "ETF Treasury USA 7-10 anni",          "download": True},
    {"ticker": "IEAG.AS",     "name": "iShares Euro Aggregate Bond", "asset_class": "fixed_income", "region": "eurozone", "currency": "EUR", "source": "yfinance", "description": "ETF obbligazionario Eurozona (aggregate, EUR, listino Amsterdam)", "download": True},
    {"ticker": "BTP_BUND_SPREAD", "name": "Spread BTP-Bund 10Y","asset_class": "fixed_income", "region": "eurozone", "currency": "EUR", "source": "computed", "description": "BTP 10Y - Bund 10Y, in bps, mensile (via FRED, popolato)", "download": False},

    # --- Valute (currencies) ---
    {"ticker": "EURUSD=X",    "name": "EUR/USD",                "asset_class": "fx",           "region": "global",   "currency": "USD", "source": "yfinance", "description": "Cambio euro/dollaro",                 "download": True},
    {"ticker": "JPY=X",       "name": "USD/JPY",                "asset_class": "fx",           "region": "global",   "currency": "JPY", "source": "yfinance", "description": "Cambio dollaro/yen",                  "download": True},
    {"ticker": "GBPUSD=X",    "name": "GBP/USD",                "asset_class": "fx",           "region": "global",   "currency": "USD", "source": "yfinance", "description": "Cambio sterlina/dollaro",             "download": True},
    {"ticker": "CHF=X",       "name": "USD/CHF",                "asset_class": "fx",           "region": "global",   "currency": "CHF", "source": "yfinance", "description": "Cambio dollaro/franco svizzero",      "download": True},

    # --- Materie prime (commodities) ---
    {"ticker": "GC=F",        "name": "Gold futures",           "asset_class": "commodity",    "region": "global",   "currency": "USD", "source": "yfinance", "description": "Oro (futures)",                       "download": True},
    {"ticker": "BZ=F",        "name": "Brent crude futures",    "asset_class": "commodity",    "region": "global",   "currency": "USD", "source": "yfinance", "description": "Petrolio Brent (futures)",            "download": True},

    # --- Cripto ---
    {"ticker": "BTC-USD",     "name": "Bitcoin",                "asset_class": "crypto",       "region": "global",   "currency": "USD", "source": "yfinance", "description": "Bitcoin",                             "download": True},
    {"ticker": "ETH-USD",     "name": "Ethereum",               "asset_class": "crypto",       "region": "global",   "currency": "USD", "source": "yfinance", "description": "Ethereum",                            "download": True},

    # --- Estensione universo (2026-06-05, audit strato 2) ---
    # Azionario tematico/settoriale
    {"ticker": "^NDX",        "name": "Nasdaq-100",             "asset_class": "equity",       "region": "US",       "currency": "USD", "source": "yfinance", "description": "Indice Nasdaq-100 (mega-cap tech USA, proxy tema AI)", "download": True},
    {"ticker": "SOXX",        "name": "iShares Semiconductor ETF", "asset_class": "equity",    "region": "US",       "currency": "USD", "source": "yfinance", "description": "ETF semiconduttori USA (tema AI/chip)", "download": True},
    {"ticker": "URA",         "name": "Global X Uranium ETF",   "asset_class": "equity",       "region": "global",   "currency": "USD", "source": "yfinance", "description": "ETF uranio/nucleare", "download": True},
    {"ticker": "LIT",         "name": "Global X Lithium & Battery ETF", "asset_class": "equity", "region": "global",  "currency": "USD", "source": "yfinance", "description": "ETF litio e batterie (transizione energetica)", "download": True},
    {"ticker": "EEM",         "name": "iShares MSCI Emerging Markets ETF", "asset_class": "equity", "region": "emerging", "currency": "USD", "source": "yfinance", "description": "ETF azionario mercati emergenti", "download": True},
    # Credito / volatilità
    {"ticker": "HYG",         "name": "iShares iBoxx High Yield Corp Bond ETF", "asset_class": "fixed_income", "region": "US", "currency": "USD", "source": "yfinance", "description": "ETF obbligazioni high yield USA (proxy credit spread / rischio)", "download": True},
    {"ticker": "^VIX",        "name": "CBOE Volatility Index",  "asset_class": "volatility",   "region": "US",       "currency": "USD", "source": "yfinance", "description": "Volatilità implicita S&P 500 (barometro risk-off)", "download": True},
    # Materie prime aggiuntive
    {"ticker": "HG=F",        "name": "Copper futures",         "asset_class": "commodity",    "region": "global",   "currency": "USD", "source": "yfinance", "description": "Rame (futures) — bellwether del ciclo economico globale", "download": True},
    # Valute aggiuntive
    {"ticker": "DX-Y.NYB",    "name": "US Dollar Index (DXY)",  "asset_class": "fx",           "region": "global",   "currency": "USD", "source": "yfinance", "description": "Indice del dollaro USA (DXY)", "download": True},

    # --- Energia europea (2026-07-07, lacuna canale energetico EU segnalata dalle schede) ---
    {"ticker": "TTF=F",       "name": "Dutch TTF natural gas futures",       "asset_class": "commodity", "region": "eurozone", "currency": "EUR", "source": "yfinance", "description": "Gas naturale europeo (Dutch TTF) — benchmark del prezzo del gas in Europa; storia da 2017-10", "download": True},
    {"ticker": "EXH9.DE",     "name": "iShares STOXX Europe 600 Utilities",  "asset_class": "equity",    "region": "europe",   "currency": "EUR", "source": "yfinance", "description": "Settore utility europeo — proxy dell'elettricità EU (i prezzi power si trasmettono a margini/valutazioni utility)", "download": True},

    # --- Cina (2026-07-13, canale valuta cinese assente — dazi/EM/commodity) ---
    {"ticker": "CNY=X",       "name": "USD/CNY (yuan onshore)",              "asset_class": "fx",        "region": "china",    "currency": "CNY", "source": "yfinance", "description": "Cambio dollaro/yuan onshore — termometro della guerra commerciale e del sentiment sulla Cina; gestito da PBOC ma segue trend/policy", "download": True},

    # --- Brasile (2026-07-19, canale LatAm/Brasile assente — attiva lo studio elezioni LatAm) ---
    {"ticker": "EWZ",         "name": "iShares MSCI Brazil ETF",            "asset_class": "equity",    "region": "brazil",   "currency": "USD", "source": "yfinance", "description": "ETF azionario Brasile (USD) — cattura equity+valuta nella vista dell'investitore in dollari; canale per elezioni/politica/commodity Brasile", "download": True},
    {"ticker": "BRL=X",       "name": "USD/BRL (real brasiliano)",          "asset_class": "fx",        "region": "brazil",   "currency": "BRL", "source": "yfinance", "description": "Cambio dollaro/real — isola il canale valutario del rischio politico/fiscale brasiliano", "download": True},

    # --- Canada (2026-08-16, lacuna dell'analisi del giorno) --------------------
    # Una scheda su un dazio USA del 50% sul Canada ha dovuto misurare solo effetti
    # di secondo ordine: nessun asset canadese nell'universo. Con l'interscambio
    # USA-Canada intorno ai 900 mld/anno e i dazi diventati strumento ricorrente,
    # il cambio è l'aggiunta a costo più basso — assorbe subito lo shock tariffario
    # senza dipendere dalla composizione settoriale di un indice.
    {"ticker": "CAD=X",       "name": "USD/CAD (dollaro canadese)",         "asset_class": "fx",        "region": "canada",    "currency": "CAD", "source": "yfinance", "description": "Cambio dollaro USA/dollaro canadese — canale diretto per dazi e attriti commerciali USA-Canada; anche proxy petrolio-sensibile (Canada esportatore netto di greggio)", "download": True},

    # --- ASEAN / Sud-Est asiatico (2026-07-30) ---------------------------------
    # Lacuna segnalata 6 volte in 3 sessioni (Thailandia-Cambogia): EEM è troppo
    # diluito (Thailandia ~2% del peso, Cambogia 0%) → le schede ASEAN restavano
    # qualitative. Questi 7 danno il canale diretto FX + equity-paese.
    # NB: la Cambogia non ha un proxy quotato — resta non misurabile.
    {"ticker": "THB=X",       "name": "USD/THB (baht thailandese)",         "asset_class": "fx",        "region": "thailand",  "currency": "THB", "source": "yfinance", "description": "Cambio dollaro/baht — canale valutario diretto della Thailandia (rischio politico, dispute confinarie, dazi)", "download": True},
    {"ticker": "SGD=X",       "name": "USD/SGD (dollaro di Singapore)",     "asset_class": "fx",        "region": "singapore", "currency": "SGD", "source": "yfinance", "description": "Cambio dollaro/dollaro di Singapore — hub finanziario ASEAN, proxy stabile del sentiment regionale", "download": True},
    {"ticker": "MYR=X",       "name": "USD/MYR (ringgit malese)",           "asset_class": "fx",        "region": "malaysia",  "currency": "MYR", "source": "yfinance", "description": "Cambio dollaro/ringgit — Malaysia, esposta a commodity ed elettronica", "download": True},
    {"ticker": "IDR=X",       "name": "USD/IDR (rupia indonesiana)",        "asset_class": "fx",        "region": "indonesia", "currency": "IDR", "source": "yfinance", "description": "Cambio dollaro/rupia — Indonesia, la maggiore economia ASEAN; valuta storicamente sensibile ai deflussi EM", "download": True},
    {"ticker": "THD",         "name": "iShares MSCI Thailand ETF",          "asset_class": "equity",    "region": "thailand",  "currency": "USD", "source": "yfinance", "description": "ETF azionario Thailandia (USD) — canale equity diretto per shock politici/confinari thailandesi", "download": True},
    {"ticker": "EWS",         "name": "iShares MSCI Singapore ETF",         "asset_class": "equity",    "region": "singapore", "currency": "USD", "source": "yfinance", "description": "ETF azionario Singapore (USD) — proxy equity dell'hub finanziario regionale", "download": True},
    {"ticker": "EIDO",        "name": "iShares MSCI Indonesia ETF",         "asset_class": "equity",    "region": "indonesia", "currency": "USD", "source": "yfinance", "description": "ETF azionario Indonesia (USD) — canale equity per elezioni/politica indonesiana", "download": True},

    # --- Difesa + Corea/Taiwan (2026-08-10, lacune più ricorrenti nelle schede) ---
    # Difesa: nessun ETF europeo puro con storia lunga su yfinance. SHLD.L è il
    # miglior compromesso (storia dal 2018, la più lunga fra i candidati testati)
    # ma è un ETF difesa/sicurezza GLOBALE a forte esposizione NATO/Europa, non
    # puramente europeo — trattalo come proxy, non come indice EU-only.
    {"ticker": "SHLD.L",      "name": "HANetf Future of Defence UCITS ETF", "asset_class": "equity",    "region": "global",    "currency": "USD", "source": "yfinance", "description": "ETF tematico difesa/sicurezza globale (forte esposizione NATO/Europa) — proxy per industria della difesa; non è un indice EU-only puro", "download": True},
    {"ticker": "EWY",         "name": "iShares MSCI South Korea ETF",       "asset_class": "equity",    "region": "korea",     "currency": "USD", "source": "yfinance", "description": "ETF azionario Corea del Sud — canale diretto per Samsung/SK Hynix (memoria/HBM), epicentro ricorrente della volatilità AI-hardware", "download": True},
    {"ticker": "EWT",         "name": "iShares MSCI Taiwan ETF",            "asset_class": "equity",    "region": "taiwan",    "currency": "USD", "source": "yfinance", "description": "ETF azionario Taiwan — canale diretto per TSMC/semiconduttori avanzati; anche proxy del rischio geopolitico Taiwan/Cina", "download": True},

    # --- Prodotti raffinati e margine di raffinazione (2026-08-11) --------------
    # Lacuna ricorrente: gli attacchi alle raffinerie (russe e non) colpiscono i
    # PRODOTTI e il MARGINE, non il greggio — con solo BZ=F il canale vero era
    # invisibile. RB=F/HO=F sono in $/gallone (NYMEX), il crack li converte in $/bbl.
    {"ticker": "RB=F",        "name": "RBOB gasoline futures",              "asset_class": "commodity", "region": "US",     "currency": "USD", "source": "yfinance", "description": "Benzina RBOB (futures, $/gallone) — prodotto raffinato; con HO=F e BZ=F costruisce il crack spread", "download": True},
    {"ticker": "HO=F",        "name": "Heating oil / diesel futures",       "asset_class": "commodity", "region": "US",     "currency": "USD", "source": "yfinance", "description": "Gasolio da riscaldamento (futures, $/gallone) — miglior proxy quotato del DIESEL, il prodotto più esposto agli attacchi alle raffinerie russe", "download": True},
    {"ticker": "CRACK_321",   "name": "Crack spread 3-2-1 (vs Brent)",      "asset_class": "commodity", "region": "global", "currency": "USD", "source": "computed", "description": "Margine di raffinazione 3-2-1 in $/barile = (2*RB=F + 1*HO=F)*42/3 - BZ=F. Calcolato da compute_crack_spread.py ad ogni update. NB: combina prodotti NYMEX con greggio Brent (convenzione comune e piu' pertinente al canale europeo/russo del WTI).", "download": False},

    # --- Curva obbligazionaria tedesca (2026-08-11) ----------------------------
    # Mancava un proxy PULITO del tasso privo di rischio tedesco: IEAG.AS e' un
    # aggregato euro (include periferia = rischio di credito) e BTP_BUND_SPREAD e'
    # un differenziale, non un livello. Serviva per confrontare la curva europea
    # con ^TNX (es. "l'Europa prezza l'energia come shock di domanda, gli USA come
    # shock di offerta"). ⚠ E' un PREZZO di ETF obbligazionario: si muove INVERSO
    # ai rendimenti (prezzo su = rendimenti giu'), al contrario di ^TNX che e' un
    # rendimento. Attenzione al segno quando lo si confronta col Treasury.
    {"ticker": "EXX6.DE",     "name": "iShares eb.rexx Gov Germany 10.5+",  "asset_class": "fixed_income", "region": "germany", "currency": "EUR", "source": "yfinance", "description": "ETF su titoli di Stato tedeschi a lunga scadenza — proxy del tasso privo di rischio tedesco (Bund). PREZZO: si muove inverso ai rendimenti, a differenza di ^TNX", "download": True},

    # --- Curve sovrane non-USA + parte lunga USA (2026-08-18) ------------------
    # Lacuna piu' costosa mai emersa (analisi 2026-08-18, sez. 8): la notizia
    # dominante del giorno era un selloff SINCRONIZZATO su quattro curve (JGB,
    # 30Y USA, gilt, ACGB) e ne avevamo UNA sola, per giunta sulla scadenza
    # sbagliata — ^TNX e' il 10 anni, mentre il fenomeno 2026 e' sul 30 anni.
    # La via "rendimenti Stooq" (come BTP_BUND_SPREAD) NON e' percorribile: al
    # 2026-08-18 l'endpoint Stooq risponde 404 anche sui simboli che funzionavano.
    # Si ripiega su ETF obbligazionari quotati, con la stessa convenzione di EXX6.DE.
    # ⚠ SEGNO MISTO IN QUESTO GRUPPO: ^TYX e' un RENDIMENTO (sale = selloff),
    # IGLT.L / 1482.T / VGB.AX sono PREZZI (scendono = selloff). In un selloff
    # globale sincronizzato la tabella mostra ^TYX positivo e gli altri tre
    # negativi: e' coerenza, non divergenza. Da dichiarare in ogni scheda.
    {"ticker": "^TYX",        "name": "US Treasury 30Y yield",               "asset_class": "fixed_income", "region": "US",        "currency": "USD", "source": "yfinance", "description": "Rendimento Treasury USA a 30 anni — la scadenza dove si manifesta il premio a termine (^TNX e' il 10Y e ne cattura solo una parte). RENDIMENTO: sale quando i titoli scendono", "download": True},
    {"ticker": "IGLT.L",      "name": "iShares Core UK Gilts UCITS ETF",     "asset_class": "fixed_income", "region": "uk",        "currency": "GBP", "source": "yfinance", "description": "ETF su Gilt britannici — proxy della curva UK (crisi LDI 2022, budget autunnali). PREZZO: si muove inverso ai rendimenti", "download": True},
    {"ticker": "1482.T",      "name": "iShares Core Japan Gov Bond ETF",     "asset_class": "fixed_income", "region": "japan",     "currency": "JPY", "source": "yfinance", "description": "ETF su JGB giapponesi — proxy della curva Giappone (aste super-long, fine dello YCC, premio a termine). PREZZO: si muove inverso ai rendimenti. Storia dal 2016-05, piu' corta degli altri", "download": True},
    {"ticker": "VGB.AX",      "name": "Vanguard Australian Gov Bond ETF",    "asset_class": "fixed_income", "region": "australia", "currency": "AUD", "source": "yfinance", "description": "ETF su titoli di Stato australiani — proxy della curva ACGB, la quarta del selloff sincronizzato 2026. PREZZO: si muove inverso ai rendimenti. Storia dal 2012-04", "download": True},

    # --- Azionario canadese e chimica europea (2026-08-18) ---------------------
    # Entrambi da sez. 8 dell'analisi 2026-08-18. Il TSX chiude il canale Canada
    # iniziato con CAD=X il 2026-08-16 (avevamo il cambio ma non l'azionario, che
    # e' l'asset piu' direttamente colpito dai dazi). EXV7.DE sostituisce ^GDAXI
    # come proxy della chimica europea: il DAX e' troppo diluito per leggere
    # BASF/Lanxess quando il Reno diventa innavigabile — canale che si ripresenta
    # ogni estate.
    {"ticker": "^GSPTSE",     "name": "S&P/TSX Composite (Canada)",          "asset_class": "equity",       "region": "canada",    "currency": "CAD", "source": "yfinance", "description": "Indice azionario canadese — asset piu' direttamente colpito dai dazi USA-Canada; forte peso di energia e materiali", "download": True},
    {"ticker": "EXV7.DE",     "name": "iShares STOXX Europe 600 Chemicals",  "asset_class": "equity",       "region": "europe",    "currency": "EUR", "source": "yfinance", "description": "ETF settoriale chimica europea — canale diretto per shock logistici fluviali (Reno) e prezzi energia, dove ^GDAXI e' troppo diluito", "download": True},

    # === AUDIT DI COPERTURA (2026-08-19) =======================================
    # Primo batch NON reattivo. Fino a qui ogni ticker era stato aggiunto DOPO che
    # una notizia ne aveva rivelato l'assenza: ~15 aggiunte in 15 giorni, sempre
    # in ritardo di almeno un giorno sull'evento. Qui invece si incrociano le 9
    # categorie dell'ontologia con i canali di trasmissione ricorrenti e si
    # riempiono i buchi PRIMA che una notizia li scopra. Ogni voce cita la data in
    # cui la lacuna era già stata segnalata e mai colmata.
    #
    # Settoriali azionari: l'universo aveva SOXX, EXH9.DE, EXV7.DE e SHLD.L ma
    # nessun modo di distinguere "il mercato ignora lo shock" da "il mercato lo ha
    # ruotato dentro l'indice" — la spiegazione alternativa piu' plausibile a meta'
    # dei nostri risultati piatti sull'azionario (lacuna del 2026-08-12).
    {"ticker": "IGV",         "name": "iShares Expanded Tech-Software ETF",  "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Software/enterprise-AI — con SOXX misura lo spread software-semis, cioe' la rotazione INTERNA al tema AI (lacuna 2026-08-05: Palantir +29,5% contro AMD -9% nella stessa seduta, non misurabile)", "download": True},
    {"ticker": "XLE",         "name": "Energy Select Sector SPDR",           "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Energia azionaria USA — distingue lo shock sul prezzo del greggio (BZ=F) dalla reazione degli utili del settore; serve per i test di rotazione settoriale", "download": True},
    {"ticker": "IYT",         "name": "iShares U.S. Transportation ETF",     "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Trasporti/logistica USA — proxy quotato dei costi di trasporto (chokepoint marittimi, noli, carburante): l'universo non aveva alcun indice di noli (lacuna 2026-08-10)", "download": True},
    {"ticker": "XLV",         "name": "Health Care Select Sector SPDR",      "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Sanitario USA — canale per drug pricing e regolazione farmaceutica, tema `regulatory` ricorrente che senza proxy resta fuori dal triage (lacuna 2026-08-05)", "download": True},
    {"ticker": "ITA",         "name": "iShares U.S. Aerospace & Defense",    "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Difesa USA — complementare a SHLD.L (globale/NATO-Europa): insieme separano un impulso di spesa americano da uno europeo (lacuna 2026-08-09)", "download": True},
    {"ticker": "REMX",        "name": "VanEck Rare Earth & Strategic Metals", "asset_class": "equity",      "region": "global",    "currency": "USD", "source": "yfinance", "description": "Minatori di terre rare e metalli strategici — il canale che LIT non copre (LIT e' la catena batterie, dominata da produttori di celle asiatici): controlli all'export cinesi su gallio/germanio/terre rare (lacuna 2026-08-05 e 2026-08-08)", "download": True},
    {"ticker": "TAN",         "name": "Invesco Solar ETF",                   "asset_class": "equity",       "region": "global",    "currency": "USD", "source": "yfinance", "description": "Solare — con URA e LIT completa la transizione energetica; polisilicio e politiche sul fotovoltaico (lacuna 2026-08-08)", "download": True},
    {"ticker": "INDA",        "name": "iShares MSCI India ETF",              "asset_class": "equity",       "region": "india",     "currency": "USD", "source": "yfinance", "description": "Azionario India — grande importatore netto di energia, canale piu' pulito di EEM per la trasmissione di uno shock petrolifero a un'economia emergente (lacuna 2026-08-12 e 2026-08-13). Storia dal 2012-02", "download": True},

    # Valute mancanti: ognuna era gia' stata chiesta e mai aggiunta.
    {"ticker": "INR=X",       "name": "USD/INR (rupia indiana)",             "asset_class": "fx",           "region": "india",     "currency": "INR", "source": "yfinance", "description": "Rupia indiana — canale valutario dello shock energetico su un importatore netto (lacuna 2026-08-12)", "download": True},
    {"ticker": "KRW=X",       "name": "USD/KRW (won coreano)",               "asset_class": "fx",           "region": "korea",     "currency": "KRW", "source": "yfinance", "description": "Won coreano — su EWY (denominato in dollari) effetto valuta ed effetto azionario restavano confusi: lo studio KB sul ciclo della memoria lo indica come 'la singola aggiunta che migliorerebbe di piu' questo studio'", "download": True},
    {"ticker": "NOK=X",       "name": "USD/NOK (corona norvegese)",          "asset_class": "fx",           "region": "norway",    "currency": "NOK", "source": "yfinance", "description": "Corona norvegese — valuta petrolifera e Norges Bank; senza, le notizie scandinave erano intriaggiabili (lacuna 2026-08-10)", "download": True},
    {"ticker": "ILS=X",       "name": "USD/ILS (shekel israeliano)",         "asset_class": "fx",           "region": "israel",    "currency": "ILS", "source": "yfinance", "description": "Shekel — canale piu' diretto del conflitto mediorientale, finora approssimato con GC=F/^VIX (lacuna 2026-08-10)", "download": True},

    # Curva e volatilita' obbligazionaria.
    {"ticker": "^FVX",        "name": "US Treasury 5Y yield",                "asset_class": "fixed_income", "region": "US",        "currency": "USD", "source": "yfinance", "description": "Rendimento Treasury 5 anni — con ^TNX e ^TYX da' la FORMA della curva USA, non solo il livello: distingue un irripidimento guidato dal front end da uno guidato dal premio a termine (lacuna 2026-08-14). RENDIMENTO: sale quando i titoli scendono", "download": True},
    {"ticker": "^MOVE",       "name": "ICE BofA MOVE Index",                 "asset_class": "volatility",   "region": "US",        "currency": "USD", "source": "yfinance", "description": "Volatilita' implicita obbligazionaria — l'equivalente del VIX per i Treasury: distingue un riprezzamento ordinato da uno stress di mercato. L'universo aveva ^VIX come unica misura di volatilita'", "download": True},

    # Consumo cinese (aggiunti il 2026-08-26). Lacuna del 25/08: il canale della
    # DOMANDA interna cinese non era misurabile. CNY=X e' compresso dal fixing
    # PBOC (mediane a zero su tutti gli orizzonti), EEM e' troppo diluito e HG=F
    # prezza le infrastrutture, non il carrello della spesa — al punto che una
    # trimestrale PDD era stata usata come evidenza macro in mancanza d'altro.
    {"ticker": "KWEB",        "name": "KraneShares CSI China Internet ETF",   "asset_class": "equity",       "region": "china",     "currency": "USD", "source": "yfinance", "description": "Internet/e-commerce cinese (Alibaba, PDD, JD, Meituan) — proxy piu' diretto del consumo discrezionale cinese: e' l'asset che mancava quando le trimestrali delle piattaforme entravano come evidenza macro. Storia dal 2013-08", "download": True},
    {"ticker": "CQQQ",        "name": "Invesco China Technology ETF",        "asset_class": "equity",       "region": "china",     "currency": "USD", "source": "yfinance", "description": "Tecnologia cinese in senso ampio — complementare a KWEB (che e' solo internet/consumo): storia dal 2011-01, copre l'intero range del DB e quindi i regimi pre-2013 che KWEB non raggiunge", "download": True},

    # Australia (aggiunti il 2026-08-27). Lacuna del 26/08: il dato RBA del giorno
    # (media troncata mensile 0,5% contro 0,3% atteso, che riapriva il caso di un
    # rialzo a settembre) e' stato SCARTATO in triage per sola assenza di asset.
    # L'unico proxy era VGB.AX, un prezzo di ETF obbligazionario con storia dal
    # 2012-04: niente cambio, niente azionario. Il briefing tratta le release
    # australiane come "primo dato core dei mercati sviluppati della settimana",
    # cioe' come PRIOR per il core PCE americano — un ruolo che si ripete.
    # ⚠ AUD=X e' USD/AUD (come CAD=X, CNY=X), NON la quotazione di mercato AUD/USD:
    # sale quando il dollaro australiano si INDEBOLISCE. Un dato RBA hawkish lo fa
    # SCENDERE. Convenzione del DB, non un refuso.
    {"ticker": "AUD=X",       "name": "USD/AUD (dollaro australiano)",       "asset_class": "fx",           "region": "australia", "currency": "AUD", "source": "yfinance", "description": "Cambio dollaro USA/dollaro australiano — canale diretto delle release RBA e del ciclo delle materie prime; con VGB.AX separa la reazione VALUTARIA da quella obbligazionaria. Storia completa dal 2011-01. INVERSO: sale = AUD debole", "download": True},
    {"ticker": "^AXJO",       "name": "S&P/ASX 200",                         "asset_class": "equity",       "region": "australia", "currency": "AUD", "source": "yfinance", "description": "Azionario australiano — terza gamba del canale (con AUD=X e VGB.AX) e proxy dell'esposizione al ciclo minerario/cinese in un mercato sviluppato. Storia dal 2011-01", "download": True},

    # Consumo USA (aggiunti il 2026-08-27). Lacuna del 27/08, seconda volta in
    # agosto che una scheda sul consumatore americano si chiude senza asset: il
    # dato piu' informativo del PCE di luglio — beni -49,9 mld contro servizi
    # +86,2 mld a reddito crescente — non era misurabile con nulla in DB.
    # Il segnale sta nel RAPPORTO XLY/XLP, non nel livello di ciascuno: e' li'
    # che si legge la rotazione difensiva. Correlazione dei rendimenti XLY-XLP
    # 0,54 dal 2019 (misurata prima di aggiungerli): sono davvero due cose diverse.
    # ⚠ XLY e' cap-weighted e dominato da Amazon+Tesla — correla 0,89 con ^GSPC:
    # da solo NON e' il consumatore, e' mezzo mega-cap tech. XRT (retail, pesi
    # molto piu' distribuiti) correla 0,76 con XLY e 0,71 con ^GSPC: e' la
    # correzione di quella distorsione, non un duplicato. Su una notizia di
    # spesa delle famiglie usali insieme e commenta la divergenza.
    {"ticker": "XLY",         "name": "Consumer Discretionary Select Sector SPDR", "asset_class": "equity",  "region": "US",        "currency": "USD", "source": "yfinance", "description": "Consumo discrezionale USA — il canale settoriale della domanda delle famiglie. ⚠ Cap-weighted: Amazon e Tesla ne dominano il peso, quindi correla 0,89 con ^GSPC. Da leggere in RAPPORTO a XLP e in contrasto con XRT, non da solo. Storia dal 2011-01", "download": True},
    {"ticker": "XLP",         "name": "Consumer Staples Select Sector SPDR",  "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Beni di prima necessita' USA — il DENOMINATORE difensivo: la rotazione da consumo ciclico a difensivo si misura in XLY/XLP, che e' il segnale, mentre il livello di ciascuno e' dominato dal beta di mercato. Storia dal 2011-01", "download": True},
    {"ticker": "XRT",         "name": "SPDR S&P Retail ETF",                  "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Retail USA con pesi distribuiti — corregge la concentrazione Amazon/Tesla di XLY: separa la spesa effettiva nei negozi dall'andamento di due mega-cap. Storia dal 2011-01", "download": True},

    # Completamento del G10 valutario (2026-08-29). Aggiunta NON reattiva: chiude
    # la CLASSE invece del singolo caso. Il 28/08 una decisione RBNZ e' stata
    # scartata in triage per sola assenza di asset — terza istanza in dieci giorni
    # della stessa classe (Corea 12-27/08, Australia 20-26/08, ora Nuova Zelanda),
    # e il briefing tratta esplicitamente Corea-Giappone-Nuova Zelanda come un
    # unico pattern: le banche centrali che si muovono PRIMA della Fed e ne sono
    # il prior. Verificato che NZD e SEK erano gli ultimi due buchi del G10:
    # con questi due il paniere e' completo e la lacuna non puo' ripresentarsi.
    # ⚠ Come CAD=X/AUD=X/CNY=X: sono USD/XXX, salgono quando la valuta locale si
    # INDEBOLISCE. Una banca centrale hawkish le fa SCENDERE.
    {"ticker": "NZD=X",       "name": "USD/NZD (dollaro neozelandese)",      "asset_class": "fx",           "region": "new_zealand", "currency": "NZD", "source": "yfinance", "description": "Dollaro neozelandese — canale delle decisioni RBNZ, la banca centrale che ha alzato prima e piu' della Fed nel ciclo 2021-2023 ed e' usata come anticipatore. Storia completa dal 2011-01. INVERSO: sale = NZD debole", "download": True},
    {"ticker": "SEK=X",       "name": "USD/SEK (corona svedese)",            "asset_class": "fx",           "region": "sweden",      "currency": "SEK", "source": "yfinance", "description": "Corona svedese — Riksbank, l'altra banca centrale piccola e anticipatrice; con NOK=X separa lo shock scandinavo petrolifero (Norvegia) da quello puramente monetario/ciclico (Svezia). Storia completa dal 2011-01. INVERSO: sale = SEK debole", "download": True},

    # Lacune 1, 2 e 3 dell'analisi del 2026-08-29. Tutte e tre verificate col test
    # di ridondanza (correlazione col concorrente piu' vicino gia' in DB) prima di
    # essere aggiunte: e' il test che il 26/08 aveva scartato COPA.L sul rame.
    {"ticker": "IWM",         "name": "iShares Russell 2000 ETF",            "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Small cap USA — il FATTORE DIMENSIONE, che l'universo non aveva. Le piccole capitalizzazioni hanno molto piu' debito a tasso variabile: sono il primo bersaglio quando il tratto breve della curva si riprezza. Il segnale e' nello SPREAD IWM/^GSPC (dev.std 0,81%/giorno, divergenza >1% nel 19% delle sedute), non nel livello: correla 0,87 con ^GSPC, com'e' normale fra due indici azionari USA. Beta 1,11. Storia dal 2011-01", "download": True},
    {"ticker": "GDX",         "name": "VanEck Gold Miners ETF",              "asset_class": "equity",       "region": "global",    "currency": "USD", "source": "yfinance", "description": "Minatori auriferi — il BETA AZIONARIO dell'oro, dove sta il segnale quando GC=F (marcato debole in scorecard, IC -0,04) non basta. Leva operativa reale e misurata: beta 1,58 su GC=F, e in agosto 2026 oro +15,6% contro GDX +36,3%. Serve anche come termometro dell'affollamento del posizionamento sull'oro. Storia dal 2011-01", "download": True},
    {"ticker": "XLU",         "name": "Utilities Select Sector SPDR",        "asset_class": "equity",       "region": "US",        "currency": "USD", "source": "yfinance", "description": "Utility USA — canale della DOMANDA ELETTRICA come vincolo del capex AI (code di connessione alla rete invece che forniture di chip). ⚠ Copre la generazione/distribuzione, NON l'equipaggiamento di rete e le turbine: quella parte resta scoperta. Scelto al posto di GRID, che correlava 0,80 con SOXX e quindi confondeva i due canali invece di separarli; XLU e' ortogonale al tech (0,31 con SOXX, residuo -0,21 al netto del mercato). Storia dal 2011-01", "download": True},
]


def create_database(conn):
    """Crea le due tabelle (assets e prices) se non esistono gia'."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            ticker      TEXT PRIMARY KEY,
            name        TEXT,
            asset_class TEXT,
            region      TEXT,
            currency    TEXT,
            source      TEXT,
            description TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            ticker    TEXT,
            date      DATE,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            adj_close REAL,
            volume    INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)
    conn.commit()


def populate_assets(conn):
    """Riempie la tabella anagrafica con tutti gli asset dell'universo."""
    rows = [
        (a["ticker"], a["name"], a["asset_class"], a["region"],
         a["currency"], a["source"], a["description"])
        for a in ASSETS
    ]
    # INSERT OR REPLACE = se il ticker esiste gia', lo sovrascrive (idempotente).
    conn.executemany(
        "INSERT OR REPLACE INTO assets VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )
    conn.commit()
    print(f"Anagrafica salvata: {len(rows)} strumenti registrati.")


def _to_float(value):
    """Converte in numero decimale; restituisce None se il dato manca (NaN)."""
    return None if pd.isna(value) else float(value)


def _to_int(value):
    """Converte in numero intero; restituisce None se il dato manca (NaN)."""
    return None if pd.isna(value) else int(value)


def download_one(ticker):
    """Scarica i prezzi di UN ticker da yfinance e restituisce una tabella."""
    df = yf.download(
        ticker,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,   # vogliamo sia "Close" sia "Adj Close"
        progress=False,
        threads=False,
    )
    # Con un solo ticker yfinance puo' restituire colonne "a due livelli":
    # le appiattiamo tenendo solo il nome ("Open", "Close", ...).
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def store_prices(conn, ticker, df):
    """Salva nel database i prezzi di un ticker. Restituisce il n. di righe."""
    rows = []
    for timestamp, row in df.iterrows():
        rows.append((
            ticker,
            timestamp.strftime("%Y-%m-%d"),
            _to_float(row.get("Open")),
            _to_float(row.get("High")),
            _to_float(row.get("Low")),
            _to_float(row.get("Close")),
            _to_float(row.get("Adj Close")),
            _to_int(row.get("Volume")),
        ))
    conn.executemany(
        "INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
    )
    conn.commit()
    return len(rows)


def main():
    # Assicura che la cartella del database esista.
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)
        populate_assets(conn)

        da_scaricare = [a for a in ASSETS if a["download"]]
        print(f"\nScarico la storia dal {START_DATE} a oggi per "
              f"{len(da_scaricare)} strumenti...\n")

        righe_totali = 0
        falliti = []
        for a in da_scaricare:
            ticker = a["ticker"]
            try:
                df = download_one(ticker)
                if df.empty:
                    print(f"  [VUOTO]  {ticker:<12} {a['name']}: nessun dato restituito")
                    falliti.append(ticker)
                    continue
                n = store_prices(conn, ticker, df)
                righe_totali += n
                primo = df.index.min().strftime("%Y-%m-%d")
                ultimo = df.index.max().strftime("%Y-%m-%d")
                print(f"  [OK]     {ticker:<12} {a['name']}: "
                      f"{n} righe ({primo} -> {ultimo})")
            except Exception as e:
                print(f"  [ERRORE] {ticker:<12} {a['name']}: {e}")
                falliti.append(ticker)
            time.sleep(0.5)  # piccola pausa tra una richiesta e l'altra

        print(f"\n--- Riepilogo ---")
        print(f"Righe totali salvate: {righe_totali}")
        if falliti:
            print(f"Strumenti senza dati (da rivedere): {', '.join(falliti)}")
        print(f"Database creato in: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
