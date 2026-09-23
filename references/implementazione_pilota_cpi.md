# Laboratorio CPI USA — istruzioni di implementazione per Claude Code

## Mandato

Implementa un primo laboratorio separato dalla pipeline quotidiana per verificare se selezionare precedenti CPI USA in base alla sorpresa rispetto al consenso e al contesto monetario produce analisi più informative.

Questo documento autorizza l'implementazione del pilota e i suoi test locali. Non fermarti alla proposta di un piano. Consegna una prima versione funzionante, con limiti espliciti quando mancano dati. Non integrare ancora il pilota nel Morning Brief, nei job launchd, nella scorecard o nell'invio Telegram.

Il progetto produce analisi descrittive e formazione quantitativa, non segnali operativi di trading. Un risultato negativo o inconcludente è un esito valido dell'esperimento.

Se disponibile, usa `superpowers:executing-plans` per eseguire i passi in sequenza. Non serve delegare. Le istruzioni locali e questo mandato prevalgono sulle convenzioni generiche delle skill.

## Prima di scrivere codice

- Leggi `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`, `Design_Document_NewsImpact.md` e le reference `esperimenti_scartati.md`, `etichette_date_locali.md`, `leggere_lo_scorecard.md`, `economia_del_run.md`.
- Controlla lo stato Git e le modifiche esistenti. Non sovrascrivere lavoro altrui. Ricava la root effettiva del progetto: non codificare percorsi `~/Claude` o `~/Codex`.
- Ispeziona `event_study.py`, `analogues.py`, `forecast_tracking.py` e i test pertinenti dentro `news_impact_pipeline/`.
- Se presente, leggi `daily_analysis/_reviews/2026-09-15-revisione-pipeline.md` come contesto storico. Verifica sul codice corrente ogni difetto rilevante: alcune correzioni potrebbero essere già state implementate.
- Verifica in sola lettura disponibilità, qualità e frequenza delle serie necessarie. Non avviare aggiornamenti, bootstrap o suite con effetti esterni solo per esplorare il progetto.

Correggi nel perimetro del laboratorio i problemi che impediscono una misurazione valida. Non riaprire tutta la revisione della pipeline come prerequisito.

## Perimetro iniziale

Una famiglia: pubblicazioni mensili CPI USA. Variabile primaria: **headline CPI, variazione mensile destagionalizzata**, valore della prima pubblicazione contro consenso della stessa metrica. Core CPI e variazioni annuali possono essere conservati come contesto, ma non diventano nuovi filtri in questa versione.

Un asset primario: `^GSPC`, se presente con copertura utilizzabile. Un orizzonte primario: cinque sedute. Se la serie non è utilizzabile, segnala il problema senza sostituirla silenziosamente con un altro asset. Altri asset e orizzonti restano fuori dalla prima valutazione.

La domanda è: **quale distribuzione storica della continuazione dalla chiusura del giorno di pubblicazione alle cinque sedute successive otteniamo con ciascun metodo?** Non chiamarla reazione immediata all'annuncio. Questa richiederebbe un'altra convenzione e, per isolarla, dati intraday.

Niente nuovi servizi, database vettoriali, agenti ricercatori, API Anthropic o dipendenze pesanti. Usa Python, SQLite e le librerie già disponibili. Non scrivere deep research o relativi prompt: le ricerche restano al maintainer.

## Struttura proposta

Adatta solo se esiste già un equivalente riutilizzabile, spiegando la scelta:

- `news_impact_pipeline/cpi_lab.py`: CLI e funzioni deterministiche di validazione, selezione, replay e valutazione. Parti da un modulo; separalo solo se necessario.
- `news_impact_pipeline/tests/test_cpi_lab.py`: test offline con record e database temporanei.
- `experiments/cpi_lab/protocol.json`: regole dell'esperimento, versionate prima della valutazione.
- `experiments/cpi_lab/events.jsonl`: dati fattuali verificati e relativa provenienza; nessun dato inventato.
- `experiments/cpi_lab/runs/`: input congelati e ricevute delle esecuzioni, separati dagli artefatti di produzione.
- `references/laboratorio_cpi.md`: metodo, schema, comandi e limiti. Aggiorna la mappa del progetto con un link, rispettandone il limite di lunghezza.

Non scrivere nella KB o nei suoi indici. Il laboratorio non deve essere scoperto accidentalmente dall'indicizzatore.

## Passo 1 — Contratto dei dati e validatore

Implementa un record per pubblicazione, identificato stabilmente dalla famiglia e dal mese di riferimento: per esempio `us_cpi:2020-01`. Il mese di riferimento è diverso dalla data di pubblicazione. Headline e core pubblicati insieme appartengono alla stessa pubblicazione, non a due osservazioni indipendenti.

Campi obbligatori:

- `schema_version`, `event_id`, `reference_month`, `release_at` con timezone;
- metrica esplicita `headline_cpi_mom_sa`, unità in punti percentuali;
- `actual_initial`, `consensus`, `previous_as_reported` (quest'ultimo può essere nullo);
- per ogni fatto: fonte, riferimento puntuale al documento, `available_at` e `retrieved_at` distinti;
- consenso: fornitore, metrica e istante di rilevazione anteriore alla pubblicazione;
- sequenza documentata delle ultime due variazioni non nulle del target Fed note prima della pubblicazione, con date, valori e fonti;
- stato di verifica e motivazione dell'eventuale esclusione.

La sorpresa si calcola con aritmetica decimale come `actual_initial - consensus`; non si salva come fatto indipendente. Non confonderla con variazione rispetto al mese precedente o con segno della reazione dell'asset.

Per il primo filtro monetario usa una regola semplice: ultima variazione non nulla del target Fed positiva = `last_move_up`, negativa = `last_move_down`, storia mancante = `unknown`. Esplicita che è una proxy della direzione dell'ultima decisione, non una misura del livello restrittivo della politica. Calcola la categoria dai fatti, senza etichettarla retrospettivamente sulla base dei mercati.

Validazione rigorosa: tipi, numeri finiti, timezone, unità coerenti, duplicati, consenso precedente al rilascio, provenienza dei dati. Duplicati conflittuali devono fallire; nessuna fusione automatica. Dati incompleti possono restare nell'archivio come esclusi, ma non entrare nel campione valido. Valore mancante non significa zero.

**Verifica:** test che rifiutino consenso post-annuncio, metriche diverse, duplicati conflittuali e valori non finiti; test che mantengano separati mese di riferimento e data del rilascio.

## Passo 2 — Prezzi, calendario e limiti temporali

Apri il database di produzione in modalità SQLite `mode=ro`. Riutilizza gli helper di `event_study.py` solo dopo averne verificato ancoraggio e comportamento con prezzi mancanti. Nessuna modifica dei prezzi di produzione.

L'ancora è la chiusura della seduta del rilascio; il target è la quinta seduta successiva. Il rendimento è `100 * (prezzo_target / prezzo_ancora - 1)`. Dichiara la colonna prezzo scelta nel protocollo e usala identicamente per tutti i metodi.

Non trattare una riga di prezzo mancante come una seduta inesistente. Verifica il calendario con strumenti già presenti; se non c'è una fonte affidabile, richiedi un calendario di sedute esplicito per il pilota. Una data inattesa o una quotazione mancante producono esclusione con motivo, non uno spostamento silenzioso dell'ancora.

Per ciascun evento valutato, il cutoff informativo è il suo `release_at`. Un precedente è utilizzabile solo se sia la sua informazione sia il prezzo finale del suo orizzonte erano disponibili prima di quel cutoff. Con soli prezzi giornalieri, usa conservativamente target di sedute anteriori al giorno del rilascio valutato.

Distingui due garanzie: prezzi congelati oggi rendono il replay riproducibile; non dimostrano che il provider mostrasse quegli stessi prezzi all'epoca. Dichiara l'eventuale assenza di vintage storiche.

**Verifica:** database temporaneo con weekend, buco in una seduta, prezzo nullo, esito di un precedente ancora immaturo e evento futuro. Nessuno di questi deve contaminare il campione.

## Passo 3 — Tre metodi con regole congelate

Il protocollo contiene versione, asset, orizzonte, convenzioni, soglia minima, periodo iniziale e periodo di valutazione. Seleziona i periodi in base alla disponibilità delle fonti, prima di vedere i risultati. Ogni modifica successiva genera una nuova versione; non sovrascrivere quella valutata.

1. **Riferimento semplice:** tutte le pubblicazioni CPI precedenti eleggibili nell'archivio verificato.
2. **Metodo corrente:** adattatore alla selezione attuale di `analogues.py`. Congela parametri e versione; registra quali eventi restituisce e gli eventuali fallback. Per il confronto omogeneo, interseca il risultato con l'universo CPI verificato e dichiara che questo è il metodo corrente ristretto al pilota.
3. **Metodo condizionato:** dallo stesso universo del riferimento, scegli gli eventi con identico segno della sorpresa (`above`, `inline`, `below`) e identica categoria `last_move_up`/`last_move_down` dell'evento valutato.

Nel metodo condizionato, categoria sconosciuta o meno di dieci precedenti eleggibili producono astensione. Nessun allargamento silenzioso dei filtri. Applica la soglia minima anche agli altri metodi. Il numero dieci è un minimo operativo, non una garanzia statistica.

Per ogni metodo calcola mediana e quartili dei rendimenti storici. I quartili descrivono una distribuzione empirica: non chiamarli intervallo di confidenza della mediana.

Il metodo corrente può dipendere da schede o research scritte dopo l'evento simulato: `--before` sulla sola data non risolve questo problema. Se non puoi provare la disponibilità temporale delle etichette e fonti, marca quel confronto come **retrospettivo non valido per misurare capacità predittiva**. Non ricostruire etichette da esiti successivi. Il confronto pulito tra riferimento semplice e metodo condizionato può comunque procedere.

**Verifica:** casi sintetici nei quali il riferimento e il metodo condizionato producano pool diversi e attesi; consenso in linea distinto da assente; astensione sotto soglia; nessun recupero di eventi futuri o ancora immaturi.

## Passo 4 — Replay riproducibile e osservazione prospettica

Implementa un replay cronologico: per ogni rilascio usa solo precedenti maturi, senza suddivisioni casuali tra addestramento e valutazione.

Ogni esecuzione deve avere un `run_id`, versione del codice e del protocollo, hash degli input e una copia immutabile dei fatti e dei prezzi effettivamente letti. Hash senza copia o sorgente immutabile non basta per riprodurre un risultato dopo un aggiornamento del DB.

Rispetta la regola locale sugli indicatori: non salvare mediane, rendimenti, conteggi, percentuali o scorecard derivate. Conserva gli input congelati, gli identificativi selezionati, cutoff e motivi decisionali; genera statistiche e report a richiesta. Una stessa esecuzione deve poter essere ricostruita senza consultare il database vivo.

Distingui esplicitamente `historical_replay` da `prospective`. Per una futura osservazione prospettica, registra input e decisione prima dell'ancora di chiusura; acquisisci successivamente i prezzi necessari all'esito in un file separato senza cambiare la ricevuta originaria. Rifiuta la qualifica prospettica se l'ancora è già passata. Non attivare scheduling in questa fase.

**Verifica:** una modifica al database originale non cambia il risultato ricalcolato da una ricevuta congelata; un run esistente non viene sovrascritto; registrare gli esiti non altera input e decisioni iniziali.

## Passo 5 — Valutazione e lacune

Mostra a console, per metodo:

- eventi eleggibili, valutati ed esclusi, con motivi; numerosità dei pool e frequenza di astensione;
- errore assoluto medio della mediana rispetto al rendimento successivo, in punti percentuali;
- copertura e ampiezza della fascia interquartile;
- accuratezza del segno, tenendo separati casi nulli e astensioni.

Confronta gli errori su **identici eventi valutabili da entrambi i metodi**, affiancando sempre la copertura sul totale: astenersi sui casi difficili non deve apparire automaticamente come un miglioramento. Non aggregare asset o orizzonti per aumentare artificialmente N. Non proclamare superiorità sulla base di pochi eventi o di una sola metrica. In questa versione non servono ottimizzazione dei parametri o ricerca automatica di soglie.

Produci a richiesta l'elenco delle lacune dai motivi di esclusione: consenso non verificabile, metrica ambigua, storia monetaria assente, prezzo mancante, campione insufficiente. Una lacuna genera una descrizione del dato necessario, non una deep research o un prompt automatico. Per eventuali annotazioni nella KB segui il flusso locale delle “Lacune emerse”.

## Interfaccia da consegnare

I seguenti sono comandi da implementare, eseguiti dalla root del progetto:

```bash
V=news_impact_pipeline/venv/bin/python
$V news_impact_pipeline/cpi_lab.py validate --events experiments/cpi_lab/events.jsonl
$V news_impact_pipeline/cpi_lab.py replay --protocol experiments/cpi_lab/protocol.json --events experiments/cpi_lab/events.jsonl --db market_data/market_data.db --runs experiments/cpi_lab/runs
$V news_impact_pipeline/cpi_lab.py report --run experiments/cpi_lab/runs/ID_ESECUZIONE
$V -m unittest discover -s news_impact_pipeline/tests -p 'test_cpi_lab.py'
```

`validate` restituisce exit code non zero per dati malformati; gli esclusi espliciti sono distinti dagli errori di schema. `replay` stampa il percorso della ricevuta e non scrive fuori dalla directory del laboratorio. `report` legge solo il run congelato e stampa risultati e limiti senza persistere indicatori.

Documenta inoltre il comando di registrazione prospettica e quello di acquisizione degli esiti, se implementati. Non presentarli come attivi o schedulati.

## Come procedere se mancano dati reali

Prima cerca materiale già disponibile nella KB e nei dati locali. L'estrazione di fatti documentati è ammessa; ogni campo deve conservare la propria provenienza. Non assumere che un comunicato ufficiale contenga anche il consenso degli analisti.

Se non trovi consensi storici verificabili, completa comunque codice, test e dimostrazione con fixture **esplicitamente sintetiche**, conservate nei test e separate dai dati reali. Lascia l'archivio reale vuoto o con soli record verificati. L'assenza di un campione deve produrre “dati insufficienti”, mai risultati sintetici presentati come evidenza finanziaria.

Specifica poi quali dati deve fornire il maintainer, con formato e fonti già utilizzabili se note. Non acquistare accessi, non aprire abbonamenti e non introdurre chiamate LLM nel motore deterministico.

## Criteri di completamento e consegna

- Tutti i test critici sopra descritti passano offline e senza modificare produzione.
- Una demo sintetica attraversa validazione, selezione, replay e report.
- Il replay è riproducibile dopo cambiamenti al DB vivo; nessun look-ahead nei casi di prova.
- La comparabilità del metodo corrente e i limiti delle vintage sono espliciti.
- Nessuna modifica a scheduler, report giornalieri, consegna, KB o ledger esistente.
- La documentazione contiene comandi per calcolare lo stato, non copie di conteggi o metriche variabili.

Alla fine comunica: file creati/modificati, comandi eseguiti, test e relativi esiti, dati reali utilizzabili, lacune bloccanti e prossimo passo. Distingui chiaramente **laboratorio funzionante**, **valutazione reale eseguibile** e **miglioramento dimostrato**: sono tre traguardi diversi. Non dichiarare il terzo perché hai raggiunto il primo.

L'integrazione nella pipeline quotidiana sarà una decisione successiva del maintainer, fondata sui risultati di questo esperimento.
