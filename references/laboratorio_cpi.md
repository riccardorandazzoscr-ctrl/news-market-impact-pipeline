# Laboratorio CPI USA

Questo esperimento vive in `experiments/cpi_lab/` e nel modulo deterministico `news_impact_pipeline/cpi_lab.py`. Claude Code può raccogliere e normalizzare fonti solo tramite il normale lavoro del maintainer; il motore non usa LLM, servizi o credenziali. Non è collegato ai run giornalieri, a Morning Brief o allo scorecard. Dal 2026-10-17 l'archivio si aggiorna da solo: vedi «Automazione» in fondo.

## Protocollo fissato

`protocol.json` è la versione 1.1.0 (la 1.0.0 partiva dal 2011, prima che esistessero consensi raccolti): headline CPI USA mensile destagionalizzato, valore della prima pubblicazione contro il consenso della stessa metrica; ^GSPC; prezzo `adj_close`; chiusura del giorno del rilascio fino alla quinta seduta XNYS successiva. Il campione iniziale è 2015–2018, la valutazione cronologica inizia nel 2019. Le pubblicazioni precedenti mature possono entrare nei pool successivi; un esito è eleggibile solo se il suo quinto target cade prima del cutoff dell'evento valutato.

La sorpresa è la differenza decimale fra valore iniziale e consenso: `above` oltre +0,05 punti percentuali, `below` sotto −0,05, altrimenti `inline`. Il contesto Fed è il segno dell'ultima variazione non nulla del target: `last_move_up`, `last_move_down`, `unknown`. È una proxy della direzione dell'ultima decisione, non del livello restrittivo. La soglia, le date e le regole sono versionate nel protocollo; ogni modifica richiede una nuova versione prima di una valutazione.

I tre pool sono: tutte le release CPI precedenti mature; release dal filtro attuale `macro_data` + `inflation_print`, tenute alle 30 più recenti e limitate all'archivio CPI verificato; release con uguale fascia di sorpresa e uguale categoria Fed. Quest'ultimo si astiene se la categoria è unknown o il pool ha meno di 10 eventi. Nessun pool si allarga in silenzio. Il confronto degli analoghi correnti è retrospettivo non valido per inferire capacità predittiva: la data di pubblicazione delle etichette e delle fonti nell'indice storico non prova quando fossero note.

### Versione 2.0.0 (`protocols/`)

Tre protocolli fissati e committati prima di eseguirli, dopo il risultato nullo della 1.1.0: `2.0.0-gspc-reazione`, `2.0.0-ief-reazione` (ancora alla chiusura della seduta **prima** del rilascio, fine alla chiusura del giorno: `anchor_offset_sessions: -1`, `horizon_sessions: 0`) e `2.0.0-ief-continuazione` (come la 1.1.0, ma su `IEF`). Ai metodi si aggiunge «solo sorpresa» (`conditioned_methods`). Asset ammessi: `^GSPC` e `IEF`, cioè prezzi; `^TNX` è un rendimento e andrebbe misurato in differenze. Un protocollo nuovo = un file nuovo, mai modificare uno già eseguito.

Esito del 2026-10-04 (12 confronti, quindi soglia di Bonferroni ≈0,004: nessuno la supera). Nel giorno del dato la sorpresa indica il verso più spesso del riferimento (59–66% contro ~51%, migliore `IEF` con sorpresa + Fed: 31/47, p=0,04), ma l'errore sull'ampiezza resta quasi uguale. Su `IEF` a 5 sedute il condizionato sbaglia il verso 32 volte su 47 (p=0,02), ma non è un'inversione: le formulazioni dirette sugli stessi dati danno 54% (opposto alla reazione) e 42% (opposto alla sorpresa), e anno per anno non c'è un andamento coerente.

### Versione 3.0.0 (`protocols/3.0.0-ief-inversione.json`)

Ipotesi fissata il 2026-10-04: la continuazione a 5 sedute di `IEF` ha verso opposto alla reazione del giorno. Non usa il consenso. Si verifica su due campioni mai guardati, i rilasci 2011–2014 (servono solo le date) e i primi 30 rilasci da ottobre 2026, con un binomiale unilaterale ciascuno. Si esegue con `cpi_lab.py reversal --protocol experiments/cpi_lab/protocols/3.0.0-ief-inversione.json --releases experiments/cpi_lab/inversione_campione_A.json --db market_data/market_data.db`. **Campione A (2011–2014), 2026-10-04: 27/48 opposti, p unilaterale 0,235: non sostenuta.** Per regola il campione B si esegue comunque, a 30 rilasci maturi da ottobre 2026, con l'ipotesi già sfavorita.

### Regola sul fornitore del consenso (decisa il 2026-10-04)

**Un fornitore per serie, dichiarato nel protocollo.** Lo stesso CPI può avere consensi diversi di 0,1 punti fra fornitori (gennaio 2023: MarketWatch 0,4, Reuters/Bloomberg 0,5), e con la soglia di ±0,05 la fascia di sorpresa cambia. Quindi:

1. L'archivio registra ogni consenso col suo fornitore in `consensus.provider`. Da settembre 2026 il calendario MarketWatch è Onclusive/Dow Jones, colonna «Forecast»: è un fornitore diverso, registrato come tale.
2. Un replay usa solo i consensi dei fornitori elencati in `consensus_providers` del protocollo. Gli altri risultano esclusi con motivo «fornitore del consenso fuori protocollo». Un protocollo senza il campo usa la mediana MarketWatch (`MW_MEDIAN` nel codice): così i protocolli 1.x e 2.x danno sempre gli stessi esiti.
3. Onclusive entra in un protocollo come serie a sé, che riparte da zero (servono almeno `minimum_pool` eventi). Può unirsi alla mediana storica solo con un raccordo fissato prima: su 12 rilasci, Onclusive e un consenso indipendente catturato prima delle 08:30 (FactSet/Dow Jones dal briefing, o altro) devono dare la stessa fascia di sorpresa almeno 11 volte.

La Wayback Machine non garantisce snapshot futuri. Per costruire la serie Onclusive o il raccordo serve una copia della pagina prima di ogni rilascio: dal 2026-10-17 la cerca il job automatico (sotto). Il protocollo 3.0.0 non usa consensi e non ne è toccato.

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

## Automazione (dal 2026-10-17)

Job launchd `com.riccardo.newsimpact.cpilab`, ogni ora e all'accensione dopo aver atteso la rete, lancia `cpi_lab_auto.py run`
(idempotente: un rilascio perso a Mac spento si recupera al primo giro con la rete; nessun modello; log in `news_impact_pipeline/logs/cpilab.log`, esiti su Telegram).
Un errore va su Telegram solo dopo 12 ore senza un giro riuscito (`logs/cpilab_ultimo_ok`): il 2026-10-21 FRED ha risposto vuoto per mezza giornata e il job si è ripreso da solo.

- **Date dei rilasci**: FRED, release 10 (anche le future). Il sito del BLS risponde 403 agli script.
- **Valore iniziale**: API pubblica BLS v1, serie `CUSR0000SA0`, variazione dagli indici a tre decimali
  arrotondata a un decimale. Si legge solo finché l'ultimo mese pubblicato è quello del rilascio: un
  recupero dopo il CPI successivo diventa `excluded` (le revisioni di febbraio cambiano gli indici).
- **Consenso**: ultima copia Wayback (HTTP 200) del calendario MarketWatch fra 7 giorni prima e le
  08:30 ET, riga «CPI» del giorno e del mese giusti, colonna che si chiami esattamente «Forecast»
  (fornitore Onclusive). MarketWatch risponde 401 agli script e la richiesta «Save Page Now» il
  2026-10-17 è fallita («Job failed»): il job la tenta prima dell'uscita, ma conta sulle copie che
  l'archivio fa da sé. Senza copia il record è `excluded` col motivo.
- **Fed**: FRED `DFEDTARU`; la variazione ha effetto il giorno dopo la decisione, che si conferma
  aprendo il comunicato `monetaryAAAAMMGGa.htm` sul sito Fed. Non trovato → `excluded`.
- **Campione B del 3.0.0**: a 30 rilasci maturi dal 2026-10-01 (verificati o esclusi: servono solo le
  date) scrive `inversione_campione_B.json` ed `inversione_campione_B_esito.json` e si ferma per sempre.
- **Calendario XNYS**: a meno di 90 giorni dalla fine lo estende di un anno con `exchange_calendars`,
  dopo aver controllato che riproduca le ultime 60 sedute già salvate.
