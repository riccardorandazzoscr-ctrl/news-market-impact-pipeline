# Design Document — News-to-Market Impact Pipeline

**Autore**: Riccardo
**Data**: 27 maggio 2026
**Versione**: 1.0
**Status**: Design fase finale, pronto per implementazione

---

## 1. Sintesi

Il progetto consiste nella costruzione di un sistema automatizzato che incrocia notizie economiche e geopolitiche quotidiane con dati di mercato e una knowledge base tematica, producendo per ogni notizia rilevante un'analisi strutturata dell'impatto storico osservato su asset class correlati. La metodologia di riferimento è l'**event study**, standard in finanza empirica (MacKinlay, 1997).

Il sistema non è un trading bot e non produce raccomandazioni operative. Produce informazione descrittiva e storica, intellettualmente onesta e metodologicamente difendibile, utilizzabile come supporto alla comprensione dei mercati e come materia prima per contenuti analitici (LinkedIn) e per lo sviluppo di competenze quantitative spendibili in carriera di asset management o macroeconomic analysis.

---

## 2. Obiettivi e posizionamento

### 2.1 Obiettivi

- Sviluppare un sistema funzionante e replicabile che integri dati di mercato, news e ricerche tematiche in un'unica pipeline analitica.
- Costruire competenze pratiche all'intersezione tra finanza e strumenti AI, utili al posizionamento professionale in asset management o macroanalysis.
- Generare un flusso costante di materiale analitico utilizzabile per il piano editoriale LinkedIn.
- Mantenere ogni passaggio del sistema metodologicamente difendibile in colloquio o discussione con interlocutori esperti.

### 2.2 Cosa il sistema NON è

Non è un trading bot. Non genera segnali operativi né raccomandazioni di acquisto/vendita. Un sistema di trading credibile richiede dataset multi-anno, backtesting rigoroso, gestione del rischio integrata e infrastruttura di esecuzione che esulano dallo scopo del progetto e che, soprattutto, sarebbero indifendibili presentati come output di un progetto personale di studio.

### 2.3 Cosa il sistema È

È un **news-to-market impact analyzer**: data una notizia, il sistema la classifica, identifica gli asset teoricamente esposti, recupera dal database storico episodi metodologicamente analoghi e restituisce statistiche descrittive del movimento osservato. Aggiunge a questo un layer di contesto qualitativo proveniente da deep research tematiche, che segmenta i regimi storici evitando di trattare come equivalenti episodi che appartengono a fasi macroeconomiche distinte.

---

## 3. Architettura: i tre layer

Il sistema è disaccoppiato in tre componenti indipendenti che comunicano attraverso interfacce esplicite. Questa separazione permette di iterare su un layer senza rompere gli altri ed è raccontabile come scelta architetturale matura.

**Layer 1 — Market Data Layer.** Hub locale di dati storici di prezzo e rendimento per un universo predefinito di asset. Persistito su disco, aggiornato giornalmente, ottimizzato per query veloci e deterministiche.

**Layer 2 — Knowledge Base Layer.** Archivio di deep research tematiche, ciascuna corredata da metadata strutturati che ne permettono il matching automatico con eventi del presente. Fornisce il contesto qualitativo e la segmentazione dei regimi.

**Layer 3 — Analytics & Pipeline Layer.** Riceve in input le notizie del briefing quotidiano, le classifica, interroga gli altri due layer e produce l'output analitico finale.

### Flusso operativo giornaliero

Al mattino arriva il briefing con le notizie del giorno. La pipeline classifica ciascuna notizia secondo l'ontologia tematica, identifica gli asset rilevanti, interroga il knowledge base layer per individuare deep research correlate e il regime storico in cui ricade l'evento, e infine interroga il market data layer per eseguire l'event study sugli episodi analoghi del passato. L'output finale è una scheda strutturata per notizia, salvata in formato leggibile e potenzialmente trasformabile in contenuto editoriale.

---

## 4. Layer 1 — Market Data

### 4.1 Universo asset

Diciotto strumenti, distribuiti su cinque famiglie. La numerosità è stata calibrata per coprire le dinamiche cross-asset rilevanti senza creare un carico di data cleaning sproporzionato per la fase MVP.

**Equity indices** (5)
- `^GSPC` — S&P 500 (benchmark globale, canale di trasmissione USD)
- `^STOXX50E` — Euro Stoxx 50 (Eurozona core)
- `FTSEMIB.MI` — FTSE MIB (Italia)
- `^GDAXI` — DAX (Germania, motore industriale europeo)
- `^N225` — Nikkei 225 (Asia sviluppata)

**Fixed income** (4)
- `^TNX` — US Treasury 10Y yield (diretto via yfinance)
- `IEF` — iShares 7-10 Year Treasury Bond ETF (proxy USA)
- `IEAG` — iShares Euro Government Bond UCITS ETF (proxy Eurozona)
- `BTP-BUND spread` — calcolato come differenza tra BTP 10Y e Bund 10Y yield (richiede fonte FRED, vedi §4.3)

**Currencies** (4)
- `EURUSD=X` — EUR/USD
- `JPY=X` — USD/JPY
- `GBPUSD=X` — GBP/USD
- `CHF=X` — USD/CHF (safe haven monetario)

**Commodities** (2)
- `GC=F` — Gold futures (safe haven, monetary hedge)
- `BZ=F` — Brent crude futures (proxy energia globale)

**Crypto** (2)
- `BTC-USD` — Bitcoin
- `ETH-USD` — Ethereum

### 4.2 Profondità storica

Quindici anni, dal 1° gennaio 2011 alla data corrente. Il periodo include la coda della crisi del debito europeo (2011-2012), il taper tantrum (2013), Brexit (2016), la guerra commerciale US-Cina (2018-2019), lo shock COVID (2020), la guerra in Ucraina e lo shock inflazionistico (2022-2023), il ciclo di rialzi Fed/BCE (2022-2024). Campione sufficientemente ricco di regimi per consentire event study significativi.

### 4.3 Fonti dati

**Fonte primaria**: `yfinance` (Python). Gratuita, copre direttamente equity, FX, commodities, crypto e Treasury USA. Affidabile per dati daily.

**Fonte secondaria**: **FRED** (Federal Reserve Economic Data, St. Louis Fed). Gratuita, richiede registrazione e API key. Necessaria per:
- BTP 10Y yield (serie `IRLTLT01ITM156N` mensile, oppure equivalente daily da fonte alternativa)
- Bund 10Y yield (serie `IRLTLT01DEM156N` mensile, oppure equivalente daily)

Per ottenere i rendimenti europei daily potrebbe essere necessario integrare ECB Statistical Data Warehouse o un provider alternativo. Da valutare in fase di implementazione.

### 4.4 Schema database

Persistenza in **SQLite** o **file Parquet** in `~/Claude/market_data/`. Due tabelle.

**Tabella `assets`** — anagrafica strumenti
```
ticker          TEXT PRIMARY KEY
name            TEXT
asset_class     TEXT     -- equity, fixed_income, fx, commodity, crypto
region          TEXT     -- US, eurozone, italy, germany, uk, japan, global
currency        TEXT
source          TEXT     -- yfinance, fred, computed
description     TEXT
```

**Tabella `prices`** — dati di mercato
```
ticker          TEXT
date            DATE
open            REAL
high            REAL
low             REAL
close           REAL
adj_close       REAL
volume          INTEGER
PRIMARY KEY (ticker, date)
```

Su 15 anni e 18 strumenti, dimensioni stimate: ~70.000 righe, qualche centinaio di kilobyte. Indicatori derivati (rendimenti, volatilità, medie mobili) non vengono persistiti: si calcolano al volo nel layer analytics.

### 4.5 Aggiornamento

Job giornaliero che aggiunge l'ultima osservazione disponibile per ogni ticker. Logica incrementale: leggi l'ultima data presente nel DB per ciascun ticker, scarica solo i dati successivi. Eseguibile come cron job o script schedulato.

---

## 5. Layer 2 — Knowledge Base

### 5.1 Struttura cartella

```
~/Claude/knowledge_base/
├── catalog.yaml                    # indice aggregato
├── brexit_dynamics.md
├── ecb_monetary_policy_2022_2024.md
├── us_china_trade_war.md
└── ...
```

Ogni deep research è un file markdown. Il `catalog.yaml` è un file di indice rigenerato automaticamente dal sistema all'avvio, aggregando i blocchi di metadata di ogni research.

### 5.2 Template metadata

Ogni deep research deve chiudersi con un blocco YAML strutturato. Quando si commissiona una nuova deep research, va richiesto esplicitamente di produrre questo blocco a fine documento.

```yaml
---
title: "Titolo descrittivo della research"
date_compiled: YYYY-MM-DD
primary_theme: <tema_principale>      # vedi ontologia §6.1
sub_themes: [tema1, tema2, ...]
relevant_assets: [TICKER1, TICKER2, ...]
time_window:
  start: YYYY-MM-DD
  end: YYYY-MM-DD                      # oppure "present"
regime_phases:
  - <nome_fase>: YYYY-MM-DD to YYYY-MM-DD
  - <nome_fase>: YYYY-MM-DD to YYYY-MM-DD
keywords: [keyword1, keyword2, ...]
---
```

### 5.3 Esempio: Brexit

```yaml
---
title: "Brexit: dinamiche economiche e di mercato 2016-2025"
date_compiled: 2026-05-27
primary_theme: geopolitical
sub_themes: [uk_eu_relations, gbp_dynamics, city_of_london, northern_ireland]
relevant_assets: [GBPUSD=X, ^FTSE, FTSEMIB.MI, ^STOXX50E, UK_10Y_GILT]
time_window:
  start: 2016-06-01
  end: present
regime_phases:
  - referendum_shock: 2016-06-23 to 2016-09-30
  - negotiation_period: 2016-10-01 to 2019-10-31
  - no_deal_speculation: 2019-04-01 to 2019-12-31
  - implementation: 2020-01-01 to 2021-12-31
  - post_brexit: 2022-01-01 to present
keywords: [brexit, uk, eu, sterling, gbp, hard brexit, soft brexit, northern ireland protocol, single market]
---
```

I campi chiave sono `primary_theme` (matching tematico), `relevant_assets` (collegamento con il market data layer), `regime_phases` (segmentazione qualitativa dei regimi storici).

---

## 6. Layer 3 — Analytics & Pipeline

### 6.1 Ontologia delle notizie

Categorie di primo livello per la classificazione automatica:

| Categoria | Esempi | Asset tipicamente esposti | Orizzonte |
|---|---|---|---|
| `monetary_policy` | Decisioni Fed/BCE/BoE, dot plot, segnali hawkish/dovish | Yields, FX, banche, equity | 1-5gg |
| `fiscal_policy` | Budget, deficit, debito sovrano | Spread sovrani, equity domestico | 1-10gg |
| `geopolitical` | Conflitti, sanzioni, tensioni diplomatiche | Safe haven (gold, CHF, JPY), energia, equity | 1-5gg |
| `macro_data` | CPI, jobs, GDP release | Yields, FX, equity | intraday-1gg |
| `corporate_idiosyncratic` | Earnings, M&A, eventi su singole aziende | Singolo titolo, settore | intraday-3gg |
| `regulatory` | Cambiamenti normativi, antitrust | Settori specifici | 1-10gg |
| `commodity_energy` | OPEC, shock petrolio, eventi energetici | Energy equity, FX commodity-linked, inflation-sensitive | 1-5gg |
| `financial_stability` | Bank runs, default, contagio | Banche, credit spreads, safe haven | intraday-5gg |
| `structural_themes` | AI, transizione energetica, demographics | Settori tematici long-term | mesi |

### 6.2 Pipeline di classificazione

Input: testo della notizia (dal briefing quotidiano).
Step 1 — Classificazione tematica via LLM (Claude API) secondo l'ontologia §6.1, con sentiment (hawkish/dovish, bullish/bearish, risk-on/risk-off) e confidence score.
Step 2 — Estrazione asset rilevanti combinando la mappa categoria→asset e keyword matching sul testo.
Step 3 — Query al knowledge base layer per recuperare deep research correlate e identificare il regime storico corrente.
Step 4 — Query al market data layer per recuperare i prezzi e calcolare l'event study.

### 6.3 Event study automation

Per ogni asset rilevante, identificazione di N episodi storici simili (matching su categoria, sotto-tema, regime). Per ciascun episodio: calcolo del rendimento cumulato in finestre [T+1, T+3, T+5, T+10 giorni di trading]. Output statistico: media, mediana, deviazione standard, percentili 25-75, numero di episodi nel campione.

**Caveat metodologico critico**: il sistema deve sempre comunicare la dimensione del campione e la dispersione. Una statistica basata su 4 episodi va presentata come tale, non come evidenza robusta.

### 6.4 Struttura output

Per ogni notizia analizzata, una scheda markdown con: classificazione, sentiment, asset rilevanti, deep research correlate, statistiche event study, considerazioni qualitative sul regime corrente. Il file è salvato in `~/Claude/daily_analysis/YYYY-MM-DD/news_NN.md` ed è direttamente convertibile in materia prima per post LinkedIn.

---

## 7. Caveat metodologici

Da tenere sempre presenti nell'uso e nella comunicazione del sistema.

**Sample size**: la maggior parte degli eventi tematici ha pochi episodi storici comparabili. Statistiche su N<10 vanno trattate come indicative, non conclusive.

**Regime dependence**: il comportamento di mercato cambia drasticamente tra regimi (es. cripto pre-2020 vs post-2020). La segmentazione regimica della knowledge base è la principale difesa contro questa fonte di errore.

**Look-ahead bias**: nella selezione degli episodi storici, il sistema deve usare solo informazione disponibile al momento dell'evento, mai dati che riflettono conoscenza ex-post.

**Correlation ≠ causation**: il sistema misura associazioni temporali tra notizie e movimenti, non causalità. La narrativa causale è responsabilità dell'analista (l'utente), non del sistema.

**Survivorship bias**: l'universo asset è fisso. Asset che hanno smesso di esistere (es. crypto fallite) non sono nel sistema, e questo può alterare le statistiche su certe classi.

---

## 8. Sequenza implementativa

**Fase 1 — Market Data Foundation** (~1-2 settimane di lavoro part-time)
Setup ambiente Python, installazione dipendenze, script di bootstrap che scarica 15 anni di storia per l'universo asset via yfinance, persistenza in SQLite o Parquet, script di aggiornamento incrementale, configurazione API FRED per yields europei.

**Fase 2 — Knowledge Base Infrastructure** (~3-5 giorni)
Creazione della struttura cartella, definizione formale del template metadata YAML, retroactive metadata tagging delle deep research già esistenti, costruzione del meccanismo di rigenerazione automatica del `catalog.yaml`.

**Fase 3 — News Classification Engine** (~1-2 settimane)
Implementazione della pipeline di classificazione via Claude API, definizione formale delle mapping categoria→asset, sistema di estrazione keyword, integrazione con il briefing giornaliero esistente.

**Fase 4 — Event Study Analytics** (~2-3 settimane)
Implementazione del motore di event study, definizione operativa del concetto di "episodio analogo", calcolo statistiche cumulative, gestione casi limite (sample size insufficiente, mancanza di dati per certe finestre).

**Fase 5 — Integration & Daily Automation** (~1 settimana)
Orchestrazione end-to-end, generazione automatica delle schede giornaliere, integrazione con il workflow esistente del briefing, eventuale notifica/sintesi al termine dell'esecuzione.

---

## 9. Dipendenze tecniche

**Linguaggio**: Python 3.10+

**Pacchetti principali**:
- `yfinance` — download dati di mercato
- `fredapi` — accesso FRED
- `pandas`, `numpy` — manipolazione dati
- `sqlalchemy` o accesso diretto a SQLite — persistenza
- `pyarrow` — supporto Parquet (se preferito a SQLite)
- `pyyaml` — parsing metadata knowledge base
- `anthropic` — chiamate API Claude per classificazione

**Credenziali esterne**:
- FRED API key (registrazione gratuita su fred.stlouisfed.org)
- Anthropic API key (già disponibile)

**Strutture cartelle**:
```
~/Claude/
├── market_data/           # database asset
├── knowledge_base/        # deep research + catalog
├── daily_briefing/        # briefing esistente
├── daily_analysis/        # output del sistema, per data
└── news_impact_pipeline/  # codice del progetto
```

---

## 10. Integrazione con il workflow LinkedIn

Ogni scheda giornaliera prodotta dal sistema è materia prima per il piano editoriale LinkedIn secondo il format già definito nel progetto "LinkedIn — Content & Strategy": hook → concetto → takeaway, 150-250 parole, tono analitico ma accessibile, mai overclaim.

Esempio di trasformazione tipica: notizia su decisione BCE → output del sistema con statistiche storiche di reazione del Bund e dello spread BTP-Bund a decisioni analoghe → post LinkedIn che racconta la dinamica storica come framework interpretativo per l'evento corrente.

La pipeline produce così, in modo strutturale e non episodico, contenuto coerente con il posizionamento finance + AI literacy, sostenuto da metodologia esplicita, e difendibile sia tecnicamente sia metodologicamente in caso di domande.

---

## Appendice — Glossario essenziale

**Event study**: metodologia accademica per misurare l'impatto di eventi su prezzi di mercato, isolando il movimento attribuibile all'evento dal rumore di fondo. MacKinlay (1997) è il riferimento canonico.

**Regime**: fase macroeconomica e di mercato caratterizzata da dinamiche stabili (es. inflazione bassa + tassi bassi 2010-2021 è un regime; inflazione alta + rialzi rapidi 2022-2024 è un altro regime).

**Look-ahead bias**: errore metodologico che consiste nell'utilizzare in un'analisi informazione che non era disponibile al momento dell'evento analizzato.

**Survivorship bias**: errore che consiste nel limitare l'analisi solo agli asset/entità sopravvissute fino al presente, escludendo quelle scomparse e quindi distorcendo le statistiche.
