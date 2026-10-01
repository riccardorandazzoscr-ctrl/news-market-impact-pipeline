# Laboratorio CPI USA

Questo esperimento vive in `experiments/cpi_lab/` e nel modulo deterministico `news_impact_pipeline/cpi_lab.py`. Claude Code può raccogliere e normalizzare fonti solo tramite il normale lavoro del maintainer; il motore non usa LLM, servizi o credenziali. Non è collegato ai run giornalieri, a Morning Brief, launchd, scorecard o Telegram.

## Protocollo fissato

`protocol.json` è la versione 1.0.0: headline CPI USA mensile destagionalizzato, valore della prima pubblicazione contro il consenso della stessa metrica; ^GSPC; prezzo `adj_close`; chiusura del giorno del rilascio fino alla quinta seduta XNYS successiva. Il campione iniziale è 2011–2018, la valutazione cronologica inizia nel 2019. Le pubblicazioni precedenti mature possono entrare nei pool successivi; un esito è eleggibile solo se il suo quinto target cade prima del cutoff dell'evento valutato.

La sorpresa è la differenza decimale fra valore iniziale e consenso: `above` oltre +0,05 punti percentuali, `below` sotto −0,05, altrimenti `inline`. Il contesto Fed è il segno dell'ultima variazione non nulla del target: `last_move_up`, `last_move_down`, `unknown`. È una proxy della direzione dell'ultima decisione, non del livello restrittivo. La soglia, le date e le regole sono versionate nel protocollo; ogni modifica richiede una nuova versione prima di una valutazione.

I tre pool sono: tutte le release CPI precedenti mature; release dal filtro attuale `macro_data` + `inflation_print`, tenute alle 30 più recenti e limitate all'archivio CPI verificato; release con uguale fascia di sorpresa e uguale categoria Fed. Quest'ultimo si astiene se la categoria è unknown o il pool ha meno di 10 eventi. Nessun pool si allarga in silenzio. Il confronto degli analoghi correnti è retrospettivo non valido per inferire capacità predittiva: la data di pubblicazione delle etichette e delle fonti nell'indice storico non prova quando fossero note.

## Dati da inserire

`events.jsonl` contiene un oggetto JSON per riga. L'archivio iniziale non contiene eventi reali: nelle ricerche locali non ho trovato una serie completa di headline mensili con consenso verificabile e istante di rilevazione. Non riempire i campi deducendoli da etichette come “sopra le attese”. Le fixture sintetiche stanno solo nel test e non vengono conteggiate come evidenza.

Record verificato minimo:

```json
{
  "schema_version": 1,
  "event_id": "us_cpi:2020-01",
  "reference_month": "2020-01",
  "release_at": "2020-02-13T08:30:00-05:00",
  "metric": "headline_cpi_mom_sa",
  "unit": "percentage_points",
  "actual_initial": {"value": "0.2", "unit": "percentage_points", "source": {"publisher": "BLS", "document_ref": "URL o identificativo puntuale del comunicato e della riga/tabella", "available_at": "2020-02-13T08:30:00-05:00", "retrieved_at": "2026-10-01T12:00:00+02:00"}},
  "consensus": {"value": "0.2", "unit": "percentage_points", "metric": "headline_cpi_mom_sa", "provider": "fornitore specifico", "observed_at": "2020-02-13T08:00:00-05:00", "source": {"publisher": "fornitore specifico", "document_ref": "snapshot/report puntuale", "available_at": "2020-02-13T08:00:00-05:00", "retrieved_at": "2026-10-01T12:00:00+02:00"}},
  "previous_as_reported": null,
  "fed_history_complete_through": "2020-02-13T08:20:00-05:00",
  "fed_moves": [
    {"decision_at": "2019-12-11T14:00:00-05:00", "change_percentage_points": "-0.25", "source": {"publisher": "Federal Reserve", "document_ref": "FOMC release puntuale", "available_at": "2019-12-11T14:00:00-05:00", "retrieved_at": "2026-10-01T12:00:00+02:00"}},
    {"decision_at": "2020-01-29T14:00:00-05:00", "change_percentage_points": "0.25", "source": {"publisher": "Federal Reserve", "document_ref": "FOMC release puntuale", "available_at": "2020-01-29T14:00:00-05:00", "retrieved_at": "2026-10-01T12:00:00+02:00"}}
  ],
  "verification_status": "verified",
  "exclusion_reason": null
}
```

Il record è solo uno schema d'esempio, non un dato del CPI di quella data. I numeri vanno sostituiti con fatti citati prima di copiarlo. Per storia Fed assente si usa `fed_moves: []`, `fed_history_status: "unknown"` e `fed_history_source` con provenienza della verifica; il record può alimentare i due metodi non condizionati, mentre il terzo si astiene. Un record incompleto con `verification_status: "excluded"` deve includere `exclusion_reason`; non entra nei pool.

Il valore headline iniziale deve riferirsi al primo comunicato BLS, non alla serie mensile oggi rivista. Il consenso deve identificare fornitore, metrica mensile SA esatta e prova archiviata prima dell'ora di rilascio. Il comunicato ufficiale BLS non prova il consenso. `previous_as_reported` è il mese precedente come mostrato in quel comunicato, oppure null. Tutti gli orari hanno fuso esplicito; `available_at` è distinto da `retrieved_at`.

`calendar.json` deve elencare ogni seduta NYSE nel periodo coperto, con `complete: true`, estremi coincidenti con la lista, una `session_closes` con timestamp e fuso esplicito per ogni seduta e fonte identificabile in `source`. Il rilascio deve precedere la chiusura della seduta; quelli successivi sono esclusi perché il close dello stesso giorno è pre-annuncio. L'assenza di un pacchetto calendario nel venv e l'archivio prezzi non bastano per inferire festività o chiusure anticipate. Rilasci in una data non presente, finestre fuori copertura o prezzi `adj_close` assenti/nulli sono esclusi con motivo, senza spostare l'ancora. Il calendario vuoto corrente è intenzionale finché il maintainer non inserisce una fonte completa.

## Comandi

Dalla root `mercati_finanza/`:

```bash
V=news_impact_pipeline/venv/bin/python
$V news_impact_pipeline/cpi_lab.py validate --events experiments/cpi_lab/events.jsonl
$V news_impact_pipeline/cpi_lab.py replay --protocol experiments/cpi_lab/protocol.json --events experiments/cpi_lab/events.jsonl --calendar experiments/cpi_lab/calendar.json --episodes knowledge_base/_episodes.yaml --db market_data/market_data.db --runs experiments/cpi_lab/runs
$V news_impact_pipeline/cpi_lab.py report --run experiments/cpi_lab/runs/ID_ESECUZIONE
$V -m unittest discover -s news_impact_pipeline/tests -p 'test_cpi_lab.py'
```

`validate` segnala schema invalido o duplicati con exit code non zero; record esclusi esplicitamente restano distinguibili. `replay` apre SQLite in sola lettura e scrive solo sotto `experiments/cpi_lab/runs/`. Ogni run ha `input.json` autosufficiente (fatti, calendario e prezzi effettivamente letti), `decisions.jsonl` (cutoff, pool selezionati e motivi, senza metriche) e `meta.json` con gli hash. È atomico e non sovrascrive un run. `report` verifica gli hash e ricalcola le metriche in memoria: MAE della mediana, quartili, copertura/ampiezza, accuratezza del segno, astensioni e MAE su casi appaiati. Il tasso di selezione accompagna sempre le metriche; gli zeri e i no-call non entrano nell'accuratezza direzionale.

Il report misura la continuazione dal close di rilascio: non una reazione immediata isolata, perché l'indice USA pubblica CPI alle 08:30 Eastern prima dell'apertura regolare. Il close include inoltre altri eventi del giorno. I prezzi correnti vengono congelati, ma non attestano vintage storiche del provider. Nessun comando prospettico o scheduling è attivo.

## Stato misurabile

- Laboratorio funzionante: codice, test sintetici e riproducibilità offline.
- Valutazione reale eseguibile: dopo aver raccolto e verificato i record CPI con consensi storici, e aver fornito un calendario XNYS completo coperto da ^GSPC.
- Miglioramento dimostrato: richiede risultati reali prospettici o un replay storico con disponibilità temporale di ogni fatto provata; questo pilota da solo non lo dichiara.
