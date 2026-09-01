# Economia del run giornaliero

**Quando aprire questo file:** il costo del run è cresciuto, o stai modificando il
runbook, un tool della pipeline o il formato delle schede.

## Dove va la spesa

Il job delle 08:15 è **l'unica voce di spesa** della pipeline: lo scorecard settimanale
e `forecast_tracking.py` sono Python puro (zero chiamate al modello), il report mensile
è un run al mese.

Misurato il 2026-08-21 sui transcript in `~/.claude/projects/`: media **$27,9 a run**,
intervallo da $12 a $53.

**Il costo dipende quasi solo dal numero di turni**, perché a ogni chiamata di tool
l'intero contesto accumulato viene riletto: il cache-read è l'**85% della spesa** e
cresce col **quadrato** dei turni.

| turni | costo |
|---|---|
| 55 | $23 |
| 96 | $36 |
| 134 | $53 |

Consumo corrente: `news_impact_pipeline/logs/usage.csv` (una riga per run: turni,
token, costo).

## Interventi applicati il 2026-08-21

Nessuno tocca il contenuto delle schede.

1. **`event_study.py --markdown` omette di default il blocco `<details>` per-evento**
   — da 13.023 a 2.743 byte a chiamata. Serve solo per potare il pool o cacciare
   outlier: si richiede con `--detail` su quella singola chiamata.
2. **`run_daily_analysis.sh` gira con `--output-format json`** e accoda una riga a
   `logs/usage.csv`. Prima **il consumo non era misurabile** se non scavando nei
   transcript. Il testo finale resta nel log come prima; se il JSON è malformato (401,
   crash) il grezzo finisce comunque nel log e l'allarme di fallimento continua a
   funzionare.
3. **Sezione "Economia del run" vincolante nel runbook**: scrivi ogni file in un
   passaggio solo; Edit chirurgico per le correzioni; niente riletture di ciò che hai
   appena scritto; niente `--help`. Più una **"Riferimento comandi"** che documenta i
   flag — il 21/08 se ne andavano 10 KB di contesto in `--help` di comandi quotidiani.
4. **Elenco asset rimosso** dal runbook e dal prompt del wrapper, dov'era duplicato e
   stale (diceva "46 asset" con 66 in DB). Fonte unica: `category_asset_map.yaml`.
   Era proprio la copia stale a costringere l'agente a rileggere lo YAML ogni mattina.

## Il principio che li accomuna

Tutti e quattro riducono **byte riletti a ogni turno**, non il numero di operazioni.
In un sistema dove il cache-read è l'85% della spesa, è l'unica leva che conta —
e una **copia stale costa doppio**: occupa contesto *e* costringe a rileggere la fonte
vera per non fidarsene.

## Proposte aperte

Stato e priorità in [MEMORY.md](../MEMORY.md).

- **Cap di lunghezza per scheda/indice**, con glossario unico renderizzato da
  `render_report.py` invece che ripetuto in ogni scheda.
- **Persistenza delle descrizioni degli episodi**: oggi `_episodes.yaml` salva
  data/verso/sotto-temi ma **butta via il testo**, così ogni mattina l'agente ri-scrive
  a memoria descrizioni di episodi già noti. Il 21/08 sono state scritte 129 righe di
  "Blocco dichiarato" su 119 date, **119 delle quali già in libreria**.
