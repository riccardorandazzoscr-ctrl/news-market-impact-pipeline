# News-to-Market Impact Pipeline

Classifica le notizie economiche/geopolitiche del giorno, le mappa su eventi di mercato
storicamente analoghi e produce un event study strutturato. **Non è un trading bot**:
statistiche storiche descrittive, per contenuti analitici (LinkedIn) e per costruire
competenze di finanza quantitativa.

Specifica completa: `Design_Document_NewsImpact.md` · Stato e prossimi passi: `MEMORY.md`

## Comandi

Tutti gli script girano nel venv dentro `news_impact_pipeline/`; qui abbreviato `$V`.

```bash
V=news_impact_pipeline/venv/bin/python
$V news_impact_pipeline/bootstrap_market_data.py   # storico una tantum (15 anni)
$V news_impact_pipeline/update_market_data.py      # incrementale: solo le righe mancanti
$V news_impact_pipeline/forecast_tracking.py run   # feedback loop settimanale (= job lun 09:00)
cd news_impact_pipeline && ./run_tests.sh          # tutte le suite (asset | analogues)
# setup venv:
cd news_impact_pipeline && python3 -m venv venv && venv/bin/pip install -r requirements.txt
```

## Dove sta ogni cosa

- `market_data/market_data.db` — SQLite, prezzi giornalieri dal 2011. Tabelle `assets`
  (registry) e `prices` (ticker × data, OHLCV + adj_close).
- `knowledge_base/` — una sottocartella per studio: materiale di origine + un .md di deep
  research che termina con un blocco YAML (template in Design_Document §5.2).
- `news_impact_pipeline/` — script e venv. `category_asset_map.yaml` è la **fonte unica**
  della mappa categoria→asset.
- `daily_analysis/YYYY-MM-DD/` — schede del giorno + `report.html`.
- `news_impact_pipeline/tests/` — suite non distruttive, si lanciano con `run_tests.sh`.
  `test_asset_universe.py` accetta i ticker come argomento: **usalo per validare la
  prossima aggiunta di asset**, non serve riscriverlo.

Aggiungere uno studio: cartella sotto `knowledge_base/`, .md col blocco YAML finale, poi
`build_catalog.py` (ricorsivo, `source_file` relativo alla KB, i file senza YAML saltati)
e `analogues.py build`. ⚠ Ogni percorso con un componente che inizia per `_` è escluso da
entrambi: tiene i blocchi YAML e le date di esempio dei prompt fuori dagli indici.

## Dati che NON si scrivono qui

Interrogali: ogni copia trascritta diventa stale. Il conteggio asset è cambiato 10 volte
in agosto 2026, e questa riga diceva ancora 68 con 78 in DB.
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
→ `render_report.py` → `send_telegram.sh`.

Automazione: 5 job launchd `com.riccardo.newsimpact.*` — marketdata-update 08:00, daily
08:15 (+ WatchPaths sul briefing), scorecard lunedì 09:00, monthly 1° del mese 09:30,
indexkb.

## Reference

- [leggere_lo_scorecard.md](references/leggere_lo_scorecard.md) — **prima di scrivere una
  lettura direzionale.** L'edge è spaccato per asset: su alcuni il segno storico è
  inaffidabile. Come si calcola l'IC, e perché.
- [esperimenti_scartati.md](references/esperimenti_scartati.md) — stai per proporre un
  miglioramento al metodo: controlla se è già stato provato e misurato.
- [copertura_asset.md](references/copertura_asset.md) — valuti se aggiungere un asset, o
  vuoi capire perché uno c'è o non c'è.
- [convenzioni_lettura_asset.md](references/convenzioni_lettura_asset.md) — la scheda tocca
  obbligazionario, small cap, oro/minatori, spesa AI o consumo USA: il livello da solo dice
  la cosa sbagliata.
- [serie_derivate.md](references/serie_derivate.md) — devi aggiornare `BTP_BUND_SPREAD`
  (fetch morto, procedura manuale), o la scheda tocca lo spread sovrano italiano o i
  margini di raffinazione.
- [etichette_date_locali.md](references/etichette_date_locali.md) — aggiungi un'etichetta
  canonica, calibri un pattern in `analogues.py`, o un pool dà risultati che non tornano.
- [economia_del_run.md](references/economia_del_run.md) — il costo del run è cresciuto, o
  modifichi runbook, tool o formato delle schede.
- [quando_si_rompe.md](references/quando_si_rompe.md) — il report non è uscito, il DB
  sembra vuoto, o qualcosa fallisce in silenzio.

## Vincoli non negoziabili

- ⚠ **Le research le scrive il maintainer, non Claude** (2026-08-16, precisato 2026-08-18).
  Claude non scrive deep research né i relativi prompt di propria iniziativa: davanti a una
  lacuna di KB si limita a **descriverla** in "Lacune emerse" di `_index.md`. Il prompt in
  `_prompts/<slug>.md` si scrive **solo su richiesta esplicita** (vedi `_prompts/README.md`);
  Claude riprende il file solo per indicizzarlo e cancellare il prompt.
- ⚠ **Nessuna API key Anthropic** (2026-05-28): il classificatore è l'agente nella sessione
  Claude Code, Python espone solo tool deterministici via Bash. `anthropic` non si usa.
- ⚠ `update_market_data.py` importa costanti e helper da `bootstrap_market_data.py` —
  **non separarli**.
- ⚠ I 5 job launchd girano **da dentro questa cartella**: se viene spostata, i plist vanno
  modificati **e ricaricati** (`launchctl bootout` poi `bootstrap`), o smettono in silenzio.
- Riporta **sempre la numerosità (N)**; con N<10 segnala il risultato come indicativo.
- Analogie storiche: **solo informazione disponibile all'epoca** dell'evento (no look-ahead).
- La segmentazione per regime (`regime_phases` nei metadati KB) è la difesa primaria contro
  il mescolare ambienti macro strutturalmente diversi nello stesso campione.
- Gli indicatori calcolati **non si persistono mai**: si calcolano al volo. Uniche eccezioni
  `BTP_BUND_SPREAD` e `CRACK_321`, *serie derivate* salvate come ticker.
