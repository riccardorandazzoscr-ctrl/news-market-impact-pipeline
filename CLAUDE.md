# News-to-Market Impact Pipeline

Classifica le notizie economiche/geopolitiche del giorno, le mappa su eventi di mercato analoghi e
produce un event study. **Non è un trading bot**: statistiche descrittive, per contenuti (LinkedIn) e studio.

Specifica completa: `Design_Document_NewsImpact.md` · Stato e prossimi passi: `MEMORY.md`

## Comandi

```bash
V=news_impact_pipeline/venv/bin/python             # tutti gli script girano in questo venv
$V news_impact_pipeline/bootstrap_market_data.py   # storico una tantum (15 anni)
$V news_impact_pipeline/update_market_data.py      # incrementale: finestra sovrapposta
$V news_impact_pipeline/update_market_data.py --check   # freschezza/buchi, senza scaricare
$V news_impact_pipeline/stato_giornata.py --date AAAA-MM-GG  # a che punto e' la giornata
$V news_impact_pipeline/forecast_tracking.py run   # feedback loop settimanale (= job lun 09:00)
$V news_impact_pipeline/forecast_tracking.py audit # tabelle non acquisite o ambigue
$V news_impact_pipeline/forecast_tracking.py recheck  # valutazioni congelate vs DB di oggi (sola lettura)
cd news_impact_pipeline && ./run_tests.sh          # tutte le suite; con un filtro ne lancia una
# setup venv:
cd news_impact_pipeline && python3 -m venv venv && venv/bin/pip install -r requirements.txt
```

## Dove sta ogni cosa

- `morning brief/YYYY-MM-DD-morning-briefing.html` — briefing del giorno (`run_morning_brief.sh`,
  07:40), letto da `run_daily_analysis.sh`, `parse_briefing.py`, `send_telegram.sh`. Qui dal 2026-09-16.
- `market_data/market_data.db` — SQLite, prezzi giornalieri dal 2011: `assets` (registry) e `prices`.
- `knowledge_base/` — uno studio per sottocartella: fonti + .md di research con blocco YAML finale.
- `news_impact_pipeline/` — script e venv; `category_asset_map.yaml` è la **fonte unica** categoria→asset.
- `daily_analysis/YYYY-MM-DD/` — schede del giorno + `report.html` + `_state.json`
  (impronta del briefing e ricevuta dell'invio; il resto si ricalcola dal disco).
  `forecast_ledger.csv` — previsioni congelate; `_scorecard/` — scorecard settimanali.
- `news_impact_pipeline/tests/` — suite non distruttive (`run_tests.sh`). `test_asset_universe.py`
  accetta i ticker come argomento: **usalo per validare la prossima aggiunta di asset**.

Aggiungere uno studio: cartella sotto `knowledge_base/`, .md col blocco YAML finale (template in
Design_Document §5.2), poi `build_catalog.py` e `analogues.py build`. ⚠ Ogni percorso con un
componente che inizia per `_` è escluso da entrambi (prompt, esempi, copie delle schede).

## Dati che NON si scrivono qui

Interrogali: ogni copia trascritta diventa stale.
```bash
sqlite3 market_data/market_data.db "SELECT COUNT(*) FROM assets;"  # asset
grep -m1 num_entries  knowledge_base/catalog.yaml                  # studi indicizzati
grep -m1 num_episodes knowledge_base/_episodes.yaml                # episodi in libreria
$V news_impact_pipeline/analogues.py stats                         # qualità libreria
```

## Il flusso

Notizia → **l'agente stesso classifica** (ontologia in Design_Document §6.1) → KB per il
contesto di regime → analoghi storici dalla **libreria episodi** (`analogues.py`) → event
study (rendimenti cumulati a T+1, T+3, T+5, T+10) → scheda in `daily_analysis/YYYY-MM-DD/`
→ `forecast_tracking.py register` (una scheda ambigua resta fuori, l'invio parte comunque)
→ `render_report.py` → `send_telegram.sh`.

Automazione: 6 job launchd `com.riccardo.newsimpact.*` (brief, marketdata-update, daily con
ritentativi e WatchPaths, scorecard, monthly, indexkb); i tre con un modello lanciano `claude -p`
headless su Opus 5.5. Orari e ripristino: [routine_giornaliera.md](references/routine_giornaliera.md).

## Reference

- [leggere_lo_scorecard.md](references/leggere_lo_scorecard.md) — **prima di scrivere una lettura
  direzionale.** Benchmark sugli stessi casi e IC per asset/orizzonte; nessuna promozione automatica.
- [esperimenti_scartati.md](references/esperimenti_scartati.md) — un miglioramento al metodo è già stato provato?
- [copertura_asset.md](references/copertura_asset.md) — aggiungere un asset, o perché c'è/non c'è.
- [convenzioni_lettura_asset.md](references/convenzioni_lettura_asset.md) — bond, small cap,
  oro/minatori, spesa AI, consumo USA: il livello da solo dice la cosa sbagliata.
- [serie_derivate.md](references/serie_derivate.md) — aggiornare `BTP_BUND_SPREAD` (procedura
  manuale), spread sovrano italiano o margini di raffinazione.
- [etichette_date_locali.md](references/etichette_date_locali.md) — aggiungi un'etichetta
  canonica, calibri un pattern in `analogues.py`, o un pool dà risultati che non tornano.
- [economia_del_run.md](references/economia_del_run.md) — costo del run cresciuto, o modifichi
  runbook, tool o formato delle schede.
- [quando_si_rompe.md](references/quando_si_rompe.md) — report non uscito, DB vuoto, guasti muti.
- [routine_giornaliera.md](references/routine_giornaliera.md) — orari, modelli, verifica e
  ricarica dei job.
- [implementazione_pilota_cpi.md](references/implementazione_pilota_cpi.md) — il laboratorio
  CPI (pilota separato dalla pipeline quotidiana).

## Vincoli non negoziabili

- ⚠ **Le research le scrive il maintainer, non Claude** (2026-08-16, precisato 2026-08-18).
  Claude non scrive deep research né i relativi prompt di propria iniziativa: una lacuna di KB
  la **descrive** in "Lacune emerse" di `_index.md`. Il prompt `_prompts/<slug>.md` si scrive **solo
  su richiesta esplicita** (`_prompts/README.md`); Claude riprende il file solo per indicizzarlo e cancellare il prompt.
- ⚠ **Nessuna API key Anthropic** (2026-05-28): il classificatore è l'agente nella sessione
  Claude Code, Python espone solo tool deterministici via Bash. `anthropic` non si usa.
- ⚠ `update_market_data.py` importa costanti e helper da `bootstrap_market_data.py`: **non separarli**.
- ⚠ I 6 job launchd girano **da dentro questa cartella**: se viene spostata smettono in
  silenzio. La copia viva dei plist è in `~/Library/LaunchAgents/`, non quella versionata in
  `news_impact_pipeline/launchd/`: va copiata **e ricaricata** (vedi routine_giornaliera.md).
- Riporta **sempre la numerosità (N)**; con N<10 segnala il risultato come indicativo.
- Analogie storiche: **solo informazione disponibile all'epoca** dell'evento (no look-ahead).
- La segmentazione per regime (`regime_phases` nei metadati KB) è la difesa primaria contro
  il mescolare ambienti macro strutturalmente diversi nello stesso campione.
- Gli indicatori calcolati **non si persistono mai**: si calcolano al volo. Uniche eccezioni
  `BTP_BUND_SPREAD` e `CRACK_321`, *serie derivate* salvate come ticker.
