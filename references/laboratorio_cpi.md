# Laboratorio CPI USA

Questo esperimento vive in `experiments/cpi_lab/` e nel modulo deterministico `news_impact_pipeline/cpi_lab.py`. Claude Code può raccogliere e normalizzare fonti solo tramite il normale lavoro del maintainer; il motore non usa LLM, servizi o credenziali. Non è collegato ai run giornalieri, a Morning Brief, launchd, scorecard o Telegram.

## Protocollo fissato

`protocol.json` è la versione 1.1.0 (la 1.0.0 partiva dal 2011, prima che esistessero consensi raccolti): headline CPI USA mensile destagionalizzato, valore della prima pubblicazione contro il consenso della stessa metrica; ^GSPC; prezzo `adj_close`; chiusura del giorno del rilascio fino alla quinta seduta XNYS successiva. Il campione iniziale è 2015–2018, la valutazione cronologica inizia nel 2019. Le pubblicazioni precedenti mature possono entrare nei pool successivi; un esito è eleggibile solo se il suo quinto target cade prima del cutoff dell'evento valutato.

La sorpresa è la differenza decimale fra valore iniziale e consenso: `above` oltre +0,05 punti percentuali, `below` sotto −0,05, altrimenti `inline`. Il contesto Fed è il segno dell'ultima variazione non nulla del target: `last_move_up`, `last_move_down`, `unknown`. È una proxy della direzione dell'ultima decisione, non del livello restrittivo. La soglia, le date e le regole sono versionate nel protocollo; ogni modifica richiede una nuova versione prima di una valutazione.

I tre pool sono: tutte le release CPI precedenti mature; release dal filtro attuale `macro_data` + `inflation_print`, tenute alle 30 più recenti e limitate all'archivio CPI verificato; release con uguale fascia di sorpresa e uguale categoria Fed. Quest'ultimo si astiene se la categoria è unknown o il pool ha meno di 10 eventi. Nessun pool si allarga in silenzio. Il confronto degli analoghi correnti è retrospettivo non valido per inferire capacità predittiva: la data di pubblicazione delle etichette e delle fonti nell'indice storico non prova quando fossero note.

### Versione 2.0.0 (`protocols/`)

Tre protocolli fissati e committati prima di eseguirli, dopo il risultato nullo della 1.1.0: `2.0.0-gspc-reazione`, `2.0.0-ief-reazione` (ancora alla chiusura della seduta **prima** del rilascio, fine alla chiusura del giorno: `anchor_offset_sessions: -1`, `horizon_sessions: 0`) e `2.0.0-ief-continuazione` (come la 1.1.0, ma su `IEF`). Ai metodi si aggiunge «solo sorpresa» (`conditioned_methods`). Asset ammessi: `^GSPC` e `IEF`, cioè prezzi; `^TNX` è un rendimento e andrebbe misurato in differenze. Un protocollo nuovo = un file nuovo, mai modificare uno già eseguito.

Esito del 2026-10-04 (12 confronti, quindi soglia di Bonferroni ≈0,004: nessuno la supera). Nel giorno del dato la sorpresa indica il verso più spesso del riferimento (59–66% contro ~51%, migliore `IEF` con sorpresa + Fed: 31/47, p=0,04), ma l'errore sull'ampiezza resta quasi uguale. Su `IEF` a 5 sedute il condizionato sbaglia il verso 32 volte su 47 (p=0,02), ma non è un'inversione: le formulazioni dirette sugli stessi dati danno 54% (opposto alla reazione) e 42% (opposto alla sorpresa), e anno per anno non c'è un andamento coerente.

### Versione 3.0.0 (`protocols/3.0.0-ief-inversione.json`)

Ipotesi fissata il 2026-10-04: la continuazione a 5 sedute di `IEF` ha verso opposto alla reazione del giorno. Non usa il consenso. Si verifica su due campioni mai guardati, i rilasci 2011–2014 (servono solo le date) e i primi 30 rilasci da ottobre 2026, con un binomiale unilaterale ciascuno. Il motore `cpi_lab.py` non la esegue ancora: è un conteggio di segni, si aggiunge quando c'è il primo campione. Aspettativa a priori bassa, scritta nel protocollo.

## Dati da inserire

`events.jsonl` contiene un oggetto JSON per riga. Contiene i rilasci reali dal 2015 al 2025 (conteggi: `cpi_lab.py validate`). Fonti: valore iniziale dal comunicato BLS archiviato; consenso = colonna «Median forecast» del calendario economico MarketWatch, letta dall'ultimo snapshot Wayback prima delle 08:30 ET. Il calendario ha cambiato indirizzo: `/economy-politics/calendars/economic` fino al 2019, `/tools/calendars/economic` nel 2019-20, `/economy-politics/calendar` dopo; gli snapshot recenti sono archiviati compressi (gzip). Un rilascio senza mediana pre-rilascio leggibile è `excluded` col motivo; `previous_as_reported` è null tranne nel 2023. Il 2026 non è ancora raccolto. Non riempire i campi deducendoli da etichette come “sopra le attese”. Le fixture sintetiche stanno solo nel test e non vengono conteggiate come evidenza.

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

`calendar.json` deve elencare ogni seduta NYSE nel periodo coperto, con `complete: true`, estremi coincidenti con la lista, una `session_closes` con timestamp e fuso esplicito per ogni seduta e fonte identificabile in `source`. Il rilascio deve precedere la chiusura della seduta; quelli successivi sono esclusi perché il close dello stesso giorno è pre-annuncio. L'assenza di un pacchetto calendario nel venv e l'archivio prezzi non bastano per inferire festività o chiusure anticipate. Rilasci in una data non presente, finestre fuori copertura o prezzi `adj_close` assenti/nulli sono esclusi con motivo, senza spostare l'ancora. Il calendario corrente (2015–2026) è generato con la libreria `exchange_calendars` (XNYS, chiusure anticipate incluse) e coincide seduta per seduta con le date `^GSPC` del DB; il 2020-04-10 (Venerdì Santo, CPI a Borsa chiusa) resta escluso.

## Comandi

Dalla root `mercati_finanza/`:

```bash
V=news_impact_pipeline/venv/bin/python
$V news_impact_pipeline/cpi_lab.py validate --events experiments/cpi_lab/events.jsonl
$V news_impact_pipeline/cpi_lab.py replay --protocol experiments/cpi_lab/protocol.json --events experiments/cpi_lab/events.jsonl --calendar experiments/cpi_lab/calendar.json --episodes knowledge_base/_episodes.yaml --db market_data/market_data.db --runs experiments/cpi_lab/runs
$V news_impact_pipeline/cpi_lab.py report --run experiments/cpi_lab/runs/ID_ESECUZIONE
# versione 2.0: stesso comando replay con --protocol experiments/cpi_lab/protocols/2.0.0-<nome>.json
$V -m unittest discover -s news_impact_pipeline/tests -p 'test_cpi_lab.py'
```

`validate` segnala schema invalido o duplicati con exit code non zero; record esclusi esplicitamente restano distinguibili. `replay` apre SQLite in sola lettura e scrive solo sotto `experiments/cpi_lab/runs/`. Ogni run ha `input.json` autosufficiente (fatti, calendario e prezzi effettivamente letti), `decisions.jsonl` (cutoff, pool selezionati e motivi, senza metriche) e `meta.json` con gli hash. È atomico e non sovrascrive un run. `report` verifica gli hash e ricalcola le metriche in memoria: MAE della mediana, quartili, copertura/ampiezza, accuratezza del segno, astensioni e MAE su casi appaiati. Il tasso di selezione accompagna sempre le metriche; gli zeri e i no-call non entrano nell'accuratezza direzionale.

Il report misura la continuazione dal close di rilascio: non una reazione immediata isolata, perché l'indice USA pubblica CPI alle 08:30 Eastern prima dell'apertura regolare. Il close include inoltre altri eventi del giorno. I prezzi correnti vengono congelati, ma non attestano vintage storiche del provider. Nessun comando prospettico o scheduling è attivo.

## Stato misurabile

- Laboratorio funzionante: codice, test sintetici e riproducibilità offline.
- Valutazione reale eseguibile: dopo aver raccolto e verificato i record CPI con consensi storici, e aver fornito un calendario XNYS completo coperto da ^GSPC.
- Miglioramento dimostrato: richiede risultati reali prospettici o un replay storico con disponibilità temporale di ogni fatto provata; questo pilota da solo non lo dichiara.
