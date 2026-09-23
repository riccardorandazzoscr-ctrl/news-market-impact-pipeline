# Piano di intervento — Revisione pipeline (10 run)

> **A chi legge:** sei una sessione Claude Code avviata da Riccardo con un messaggio tipo
> «esegui il prossimo run del piano». Questo file è l'unica istruzione che ti serve.
> Segui il **Protocollo** qui sotto alla lettera, poi fai **un solo run** e fermati.

Origine: `2026-09-15-revisione-pipeline.md` (copia identica in
`mercati_finanza/daily_analysis/_reviews/`). Gli ID R01–R14 sono quelli del report.

---

## Protocollo — da eseguire all'inizio di OGNI sessione

1. **Leggi il report.** `2026-09-15-revisione-pipeline.md`, almeno la sezione «Problemi e
   interventi proposti» e i paragrafi degli ID toccati dal run che stai per fare.
   Non lavorare a memoria: il report contiene i numeri di riga esatti.
2. **Leggi `mercati_finanza/CLAUDE.md` e `mercati_finanza/MEMORY.md`** per il contesto dell'area.
3. **Trova il prossimo run:** il primo qui sotto che non è marcato `[x] FATTO`.
   Se Riccardo ne nomina uno diverso, vince lui.
4. **Controlla il modello consigliato del run** (tabella in fondo).
   - Se sei già sul modello giusto: procedi.
   - Se sei su un modello **più capace** di quello consigliato: **procedi lo stesso**, abbassa
     l'effort. Non chiedere a Riccardo di cambiare modello: costa più il cambio che il risparmio.
   - Se sei su un modello **meno capace** di quello consigliato e il run è marcato **Opus**:
     dillo in una riga e chiedi conferma prima di iniziare.
5. **Esegui SOLO quel run.** Non anticipare i successivi, non "già che ci sono".
6. **Verifica** (blocco Verifica standard, sotto).
7. **Chiudi:** marca il run `[x] FATTO — <data>` in questo file, aggiungi max 3 righe di note
   sotto il run (cosa è stato deciso, cosa è rimasto fuori), e riporta a Riccardo.
8. **Fermati.** Il run successivo è una sessione nuova.

### Regole di lavoro

- **Ponytail attivo:** diff più corto che funziona. Niente astrazioni non richieste, niente
  scaffolding "per dopo". Ma mai pigri sulla *comprensione*: leggi tutto il flusso prima.
- **Root cause, non sintomo.** Prima di modificare una funzione, `grep` di tutti i chiamanti:
  una guardia nella funzione condivisa batte una guardia in ogni chiamante.
- **Niente scatole nere.** Ogni giudizio automatico deve restare esplicito e scavalcabile a mano.
- **Nessun dato variabile trascritto nei file** (conteggi, percentuali): si scrive il comando
  che lo produce.
- **Non avviare mai** la routine vera, invii Telegram, download a pagamento o ricostruzioni
  live degli indici senza che Riccardo lo chieda esplicitamente.
- **Ogni logica non banale lascia UN check runnabile** (un `assert` in un `demo()`/`__main__`
  o un piccolo `test_*.py`). Niente framework, niente fixture.
- Se un run si rivela più grande del previsto: **fermati, spiega, non allargare**.

### Verifica standard (dopo ogni run)

```bash
cd /Users/riccardo/Claude/mercati_finanza
PYTHONDONTWRITEBYTECODE=1 news_impact_pipeline/venv/bin/python news_impact_pipeline/tests/test_analogues_direction.py
PYTHONDONTWRITEBYTECODE=1 news_impact_pipeline/venv/bin/python news_impact_pipeline/tests/test_analogues_match_all.py
sqlite3 -readonly market_data/market_data.db 'PRAGMA quick_check;'
sqlite3 -readonly market_data/market_data.db 'SELECT ticker, MAX(date), SUM(close IS NULL AND adj_close IS NULL) FROM prices GROUP BY ticker;'
```

`run_tests.sh` completo **no**: la suite asset aggiorna il DB vero.

---

## [x] Run 1 — Sanguinamenti veloci — FATTO — 2026-09-15
**ID report:** R03 (parte regex), R06, R10 (parte etichette), + voci sparse
**Modello:** Sonnet 5 · effort medium

Diff piccoli e locali, nessuna decisione architetturale.

- [x] **Regex taxonomy** (`subtheme_taxonomy.yaml`): `ism` (riga ~440) riconosce «Meccanismo»,
      `utili` (riga ~129) riconosce «Utilities». Confini di parola per acronimi e parole complete.
      ⚠️ **Prima di chiudere:** rigenera la libreria episodi e **mostra a Riccardo il diff degli
      episodi che spariscono** — alcuni potrebbero essere veri. Non cancellare nulla senza il suo ok.
- [x] **`send_telegram.sh`** (riga ~20): controlla lo stato HTTP **e** il campo JSON `ok`.
      Ricevuta per ogni artefatto atteso; se ne parte solo uno dei due, l'esito finale non è
      successo (riga ~65).
- [x] **`update_market_data.py`** (riga ~90): il ciclo esce con codice ≠ 0 se tutti i download
      falliscono. Il wrapper controlla l'esito prima di avviare l'analisi.
- [x] **`requirements.txt`**: aggiungi `openpyxl` (importato da `export_to_excel.py`).
      Mentre ci sei, versioni vincolate per riprodurre l'ambiente.
- [x] **`fetch_daily_spread.py`** (riga ~196): oggi avverte quando manca la data di controllo
      ma scrive ugualmente. Deve non scrivere.
- [x] **Etichette scorecard** (`forecast_tracking.py` riga ~669): togli i giudizi
      «affidabile»/«controproducente» agganciati a soglie di IC. Solo per ora, etichette prudenti:
      la statistica seria è il Run 11. Togli anche dal runbook la lettura «IC negativo = segno
      sbagliato» — è falsa: previsioni `[1,2,3,4]` e realizzati `[4,3,2,1]` danno IC −1 con tutti
      i segni corretti.

**Note di chiusura:**
- Libreria episodi rigenerata (1075→1096 tot., ma per il fix regex: −23 `activity_growth`
  falsi (Conference Board, testo «Meccanismo:»), −4 `earnings_shock` falsi (Fukushima/TMI,
  testo «Utility nucleari») — spot-check sulla fonte conferma sono falsi positivi. **Diff non
  ancora approvato da Riccardo**: `git diff knowledge_base/_episodes.yaml` per rivedere,
  `git checkout -- knowledge_base/_episodes.yaml` per annullare.
- Rimosso il verdetto ✅/❌ dalla tabella 5-bis di `forecast_tracking.py`: ho dovuto
  aggiornare a cascata anche `run_daily_analysis.sh`, `PHASE5_RUNBOOK.md`,
  `references/leggere_lo_scorecard.md` e `glossario.md`, che istruivano a leggere quel
  marcatore — non era nella lista ma senza quel fix il prompt del daily si sarebbe rotto.
- Venv ricreato da zero con Python 3.12 (stesso minor già in uso) dopo conferma di Riccardo:
  `venv/bin/pip` aveva shebang stale su un path pre-riorganizzazione. Reinstallate le
  dipendenze pinnate da `requirements.txt`, test standard rilanciati e verdi.

---

## [x] Run 2 — Prezzi — FATTO — 2026-09-15
**ID report:** R05
**Modello:** Opus 5 · effort high

Casi limite veri: calendari di mercato, revisioni degli adjusted, transazioni sul DB.
È il punto dove un fix confidente e sbagliato corrompe lo storico.

- [x] `update_market_data.py` (riga ~65): finestra sovrapposta invece di `MAX(date) + 1`.
      Oggi una barra scaricata a mercato aperto resta definitiva per sempre.
- [x] Stato esplicito «barra provvisoria / definitiva».
- [x] Riparare buchi precedenti all'ultima data, righe senza prezzo, revisioni degli adjusted.
      Nel DB reale esistono righe con `close` e `adj_close` entrambi NULL.
- [x] Controlli di freschezza e copertura per ticker, coerenti con i calendari di mercato.
      Il conteggio dei ticker del wrapper non rileva nulla di tutto questo.
- [x] La finestra va scelta **per fonte e strumento**: un lookback breve unico non copre
      le revisioni storiche.
- [x] Conservare provenienza e stato dei prezzi. **Non** persistere indicatori calcolati.

**Note di chiusura:**
- Finestra sovrapposta per classe (fx/crypto 5g, resto 10g) + passata profonda il sabato
  (o `--deep`) che rilegge tutto lo storico: è l'unica che cattura le revisioni di
  `adj_close`, che si riscrivono all'indietro. Tre colonne nuove su `prices`
  (`source`, `status`, `fetched_at`), ALTER idempotente in `create_database`: ha imposto
  di rendere espliciti i cinque `INSERT ... VALUES (?,?,?,?,?,?,?,?)` posizionali sparsi
  fra spread, crack e FRED, che si sarebbero rotti al primo ALTER.
- Soglia dei buchi = ponte festivo più lungo di **quel** ticker, dedotto dalla sua storia
  precedente alla finestra esaminata (niente calendario di borsa da mantenere, e un buco
  non può alzare la propria soglia). Prima versione col 99° percentile: 9 falsi positivi
  su Capodanno giapponese e Natale tedesco, scartata. Ora `--check` sul DB vero riporta
  **solo** le 13 righe senza prezzo che il report aveva trovato a mano.
- **Niente è stato scaricato né cancellato.** Le 13 righe rotte e le barre di oggi ancora
  provvisorie le ripara il prossimo `update_market_data.py` vero (lo lanci tu, o il job
  delle 08:00). Se la fonte non le ripubblica restano segnalate: nessuna riga viene
  cancellata d'ufficio. ⚠ Fuori tema ma emerso: `BTP_BUND_SPREAD` è fermo all'11/09,
  il refresh Stooq di lunedì 14 non ha aggiornato.

---

## [x] Run 3 — Parser briefing e link — FATTO — 2026-09-15
**ID report:** R08
**Modello:** Sonnet 5 · effort medium

Circoscritto e indipendente dal resto. Terzo perché è la cosa che Riccardo vede ogni mattina.

- [x] `parse_briefing.py` (riga ~136): oggi legge **solo il primo paragrafo** della storia.
      Conservare tutto il testo di contenuto.
- [x] Separare `Markets` dalle fonti; mantenere URL e date di pubblicazione (oggi le fonti
      sono testo senza URL).
- [x] `render_report.py` (riga ~98): i link `news_NN.md` del triage devono diventare **ancore
      interne** alle schede incorporate. Oggi nell'HTML che arriva su Telegram non portano da nessuna parte.
- [x] La guardia shell deve usare **il parser vero**, non contare `class="story"`: un HTML
      senza contenitore `<section>` oggi passa il controllo ed estrae zero notizie.

**Note di chiusura:**
- Corpo storia: ora tutti i `<p>` non-fonte, non solo il primo. Verificato sul briefing
  vero del 15/09: tutte le 20 storie avevano un secondo paragrafo che oggi si perdeva.
  Fonti: da stringa piatta a lista `{name, url}` (link `<a>` quando ci sono, altrimenti
  split su `;`/`/` del testo). Nessun consumer esistente dipendeva dal vecchio formato
  stringa (solo `format_listing`, aggiornato).
- `render_report.py`: i link `[testo](news_NN.md)` nel markdown diventano `[testo](#doc-news_NN)`
  prima della conversione, sia in `_index.md` sia nelle schede stesse — coerente con l'`id`
  di sezione già assegnato da `render()`.
- Guardia shell: **solo** `run_daily_analysis.sh` (`conta_story()`/`brief_completo()`, il
  cancello prima del run Opus costoso) è passata al parser vero via nuovo flag
  `parse_briefing.py --count`. **Non toccato** `run_morning_brief.sh`: stesso grep fragile,
  ma lì è idempotenza/logging del job che *produce* il brief, non un cancello su una spesa
  a valle — cambiarlo avrebbe richiesto riscrivere anche i fixture HTML di
  `test_morning_brief.sh` (oggi senza `<section>`), un secondo run.
- "Markets" (bullet 2 del checklist): il layout attuale dei briefing non ha uno span/campo
  `Markets` distinto (esisteva in un layout di maggio-giugno 2026, assente da agosto in poi).
  Niente da separare oggi — non inventato un campo che i dati reali non hanno.
- Toccati anche 3 fixture di test che si aspettavano il vecchio grep: `test_briefing_race.sh`
  (ora punta al venv vero via uno shim — un symlink nudo rompe la risoluzione del prefix
  del venv — e i suoi `<h2>` finti dicevano "World", non riconosciuto dal parser: ora
  "International"), `test_index_incompleto.sh` e `test_watchdog.sh` (stub python: aggiunto
  un ramo per `parse_briefing.py --count` che replica il vecchio conteggio, dato che testano
  la completezza dell'*analisi*, non il parsing del brief).
- Nuovo `tests/test_parse_briefing.py` (6 assert, in `run_tests.sh parser`): corpo
  multi-paragrafo, fonti con URL, `--count` zero su HTML senza `<section>`, riscrittura link.
- Verifica standard + `run_tests.sh briefing/analisi/watchdog/parser/brief`: tutte verdi
  (incluse le regressioni sui 145 briefing reali in archivio, 109 giorni di analisi reali).

---

## [x] Run 4a — Completamento verificabile: PIANO — FATTO — 2026-09-15
**ID report:** R07
**Modello:** Opus 5 · effort high

**Questo run non scrive codice di produzione.** Produce un piano scritto che Riccardo approva.
Usa la skill `superpowers:brainstorming` o plan mode. Output: un file di piano in
`mercati_finanza/daily_analysis/_reviews/` o nello scratchpad, a scelta di Riccardo.

Da progettare: stati distinti per **input validato → dati pronti → triage completato →
schede validate → HTML prodotto → consegna confermata**, legati all'identità/contenuto
dell'input e non solo alla data.

**Note di chiusura:**
- Piano approvato in `daily_analysis/_reviews/2026-09-15-r07-stati-completamento.md`.
  Tre decisioni di Riccardo, **da non rinegoziare nel Run 4b**: (1) la verità è il disco,
  `_state.json` è solo ricevuta (impronta input + ricevuta consegna); (2) prezzi bloccanti
  **senza** flag di scavalco — si sblocca riparando il dato; (3) una scheda si invalida
  solo se cambia il testo della notizia, non le dipendenze.
- Fatti verificati sul DB e non dedotti, che il Run 4b deve dare per buoni: `assets.source
  = 'computed'` distingue già le due serie derivate (niente lista a mano); `fetched_at` ha
  due formati, confronto per prefisso di data; il consolidamento fa linkare la stessa
  scheda da più righe di triage, quindi le impronte lavorano su insiemi.
- Emerso a margine: `BTP_BUND_SPREAD` è **ancora** fermo all'11/09 (segnalato dal Run 2).
  Le 13 righe senza prezzo sono invece sparite: l'update delle 15:53 le ha riparate.

## [x] Run 4b — Completamento verificabile: IMPLEMENTAZIONE — FATTO — 2026-09-15
**Modello:** Opus 5 · effort high
**Precondizione:** piano del Run 4a approvato da Riccardo.

- [x] `run_daily_analysis.sh` `index_completo` (riga ~99): oggi un indice **completamente vuoto
      passa**. Verificare corrispondenza con le notizie in ingresso, esistenza delle schede,
      link e risultati attesi.
- [x] Il retry deve ripartire **dalla prima fase incompleta**. Oggi l'indice completo fa uscire
      subito e non ripara rendering/consegna falliti (che sono ridotti a warning, riga ~410).
- [x] Riuso delle schede già validate se input e dipendenze non sono cambiati (risparmia anche token).
- [x] `WatchPaths` launchd: l'arrivo del briefing può avviare l'analisi **prima** dell'aggiornamento
      prezzi. Serve una dipendenza vera sulla disponibilità dei dati, non un orario.
- [x] Verificare che ci sia **un solo scheduler proprietario per fase**: configurazione presente,
      servizio abilitato e servizio caricato sono tre cose diverse.
      `launchctl print-disabled gui/$(id -u) | rg newsimpact`

**Note di chiusura:**
- Nuovo `stato_giornata.py` (sei fasi, riuso schede, ricevuta) + `parse_briefing.py --impronte`;
  `index_completo`/`brief_completo` eliminati, il wrapper si dirama sulla prima fase incompleta.
  Scheduler verificato: 6 plist versionati = 6 vivi = 6 caricati, nessuno disabilitato,
  contenuti identici. **Nessuna modifica ai plist**, come da piano.
- Due cose fuori dal piano, entrambe imposte dal codice. (1) L'identità di una notizia è la
  coppia **sezione+numero**: i numeri si ripetono fra `intl` e `fin` (stessa classe d'errore
  dell'R02). (2) La diagnosi delle serie è finita in `diagnosi_serie.py`: stava in
  `update_market_data.py`, che per rispondere importava yfinance e pandas — 2,2s di avvio a
  ogni controllo di fase, su una domanda che usa solo `sqlite3`.
- Scelte *misurate*, non assunte: il controllo sui titoli riscritti è stato **scartato** (20
  giornate su 106 li riscrivono); le righe di triage in più sono un avviso, non un blocco (unico
  caso in archivio: il 28/08 col box "One Thing to Watch" in tabella); il riferimento alla
  scheda si accetta anche senza link (due giornate di fine giugno lo scrivono nudo).

---

## [x] Run 5a — Schema KB: PROGETTAZIONE — FATTO — 2026-09-21
**ID report:** R04 + R01
**Modello:** Opus 5 · effort high

**Solo design, niente implementazione.** Da definire:
- Formato comune degli episodi per schede giornaliere **e** KB: evento, data/ora annuncio,
  geografia, istituzione, meccanismo, asset di riferimento, pressione attesa all'epoca,
  fonte, incertezza.
- Schema validato: tipi, valori nulli, struttura degli intervalli, date possibili, ticker.

**Note di chiusura:**
- Spec in `daily_analysis/_reviews/2026-09-21-r04-r01-schema-episodi.md`. Il problema non
  era quello descritto: le research **hanno già** una tabella di episodi (18 studi su 29,
  colonne quasi identiche) e le loro date sono già tutte in libreria — manca che direzione
  e asset siano *campi* invece che prosa. Quindi niente schema nuovo: si porta sulle
  research il contratto della scheda, che funziona per tre regole scritte nel template
  (un asset dichiarato, vocabolario chiuso, convenzione detta sul posto). Unica variante
  decisa da Riccardo: colonna `Asset` per riga, perché una research tocca più asset.
- Emerso e **più grande del problema KB**: le schede di agosto dichiarano episodi con zero
  `direction_reference`, e a settembre il campo compare solo dal giorno 14 in poi — stessa
  causa, righe inutilizzabili. Riccardo ha chiesto che il recupero copra schede **e**
  research. Il verso si dichiara senza mai aprire il DB prezzi (sarebbe look-ahead
  circolare: la scorecard misurerebbe la propria copiatura).
- Riuso invece di costruzione: le dichiarazioni recuperate vanno in
  `knowledge_base/_direction_reviews.yaml`, che ha già la forma del record ed è già
  validato — servono due campi nuovi (`mechanism`, `description`) e togliere il vincolo
  che la fonte sia una scheda. Resta aperto per il 5b: se riscrivere la tabella dentro il
  `.md` della research o lasciarla in prosa (la spec raccomanda la seconda).

## [x] Run 5b — Schema KB: IMPLEMENTAZIONE (parte 1/2) — FATTO — 2026-09-21
**Modello:** Opus 5 · effort high
**Precondizione:** schema del Run 5a approvato.

⚠ **Run spezzato in due.** Questa parte chiude R04 (parser, schema, scanner,
pubblicazione). Il ramo KB di `analogues.py` e il recupero delle righe già scritte
passano al **Run 5c**, sotto.

- [x] **Un solo parser YAML** per catalogo ed episodi. Oggi sono due e divergono: YAML valido
      con `primary_theme: "macro_data"` passa il catalogo e perde il tema nell'estrattore.
- [x] `build_catalog.validate` (riga ~96): validare tipi e strutture, non solo presenza dei campi.
      Oggi la research BoJ usa stringhe per `time_window`/`regime_phases`, passa, e
      `monthly_digest.kb_regimes` (riga ~83) restituisce come fase corrente il carattere `)`.
- [x] `index_studies.sh` (riga ~50): oggi considera indicizzata un'intera cartella se **un
      qualsiasi** Markdown contiene un fence YAML. Scoperta file condivisa fra scanner e builder,
      ricorsiva, che rilevi rimozioni e rinomine.
- [x] Indici generati in temporaneo, validati, pubblicati **atomicamente**. Un errore su un file
      deve essere esplicito, mai pubblicare un catalogo degradato in silenzio.

**Note di chiusura:**
- Nuovo `kb_metadata.py`: l'unico parser dei metadati KB, senza dipendenze pesanti (lo
  importano sia il builder sia `analogues`). Il difetto dei due parser era **peggio** di
  come il report lo descriveva: con `primary_theme` fra virgolette l'estrattore restituiva
  tema vuoto, e un tema vuoto fa scartare ogni riga in `add()` — una research col tema
  quotato appariva nel catalogo e contribuiva **zero** episodi, senza un warning da nessuna
  parte. Riprodotto prima di correggere, ora coperto da test.
- La validazione distingue **ERRORE** (non pubblica) da **avviso** (pubblica). Un ticker
  esterno resta avviso: esiste `external_assets_mentioned` per dichiararlo. Il primo run
  del nuovo builder ha rifiutato di pubblicare per il solo file BoJ, con messaggio preciso;
  corretti i suoi due campi alla forma canonica (28/29 file già la usavano, nessun cambio
  di contenuto) e la fase corrente nel digest mensile è tornata `post_ycc_2024_2026`
  invece di `)`.
- Lo scanner non ha più una propria nozione di «indicizzato»: `build_catalog.py --scan`
  risponde allo shell. Lo staleness è per **contenuto**, quindi rileva rimozioni e
  rinomine che la vecchia mtime non vedeva mai. Effetto misurato del parser unico sulla
  libreria: **0 episodi persi, 9 guadagnano sotto-temi** (liste `sub_themes` multilinea che
  la vecchia regex buttava via). Nuova suite `run_tests.sh kb`, 36 asserzioni.

---

## [x] Run 5c — Ramo KB di `analogues` e strumento di recupero — FATTO — 2026-09-23
**ID report:** R01 + resto di R03
**Modello:** Opus 5 · effort high (eseguito su Opus 5.5)
**Precondizione:** Run 5b parte 1 chiuso. Contratto in
`daily_analysis/_reviews/2026-09-21-r04-r01-schema-episodi.md` — **già approvato, non
rinegoziare**: la research non si riscrive, le dichiarazioni vivono nel registro.

⚠ **Run spezzato di nuovo.** Il codice è chiuso; il recupero vero passa al **Run 5d**, perché
richiede più sessioni e prima una decisione di metodo del maintainer (vedi 5d).

- [x] `analogues.py` ramo KB: legge la **tabella canonica** `| Data | Asset | Verso |
      Meccanismo | Evento |` e produce `directions_by_reference`. Se presente è l'autorità
      del file: la prosa si spegne.
- [x] Revisioni con fonte research (`source: kb:<percorso>`), con controllo equivalente:
      la research deve contenere quella data.
- [x] **Non** convertire automaticamente i versi legacy: il recupero passa da una proposta
      che il maintainer approva.
- [x] R03 resto, parte deterministica: etichette dalla **riga** della tabella (Tankan);
      date di solo mese e intervalli nella cella rifiutati.
- [x] Normalizzare le tabelle esistenti: date italiane lette, `AC` → seduta di reazione.
- [x] `mechanism` e `description` nel registro, opzionali.

**Note di chiusura:**
- Due regole che sembravano ovvie **misurate e scartate prima di scriverle**. (1) «Tabella =
  autorità» anche sulle research in formato libero: avrebbe cancellato episodi veri scritti
  in prosa (Bolsonaro, Boric, controlli all'export sui chip, bando su Micron). Vale quindi
  solo per la tabella canonica. (2) «Data successiva alla compilazione = spuria»: prende una
  sola data, ed è un evento vero in calendario; le spurie vere sono *anteriori*. Separare una
  nota editoriale da un episodio in prosa è un giudizio, non una regola: le date spurie delle
  research vecchie si chiudono research per research, nel recupero.
- Effetto sulla libreria: **+13 episodi, 0 rimossi** — 6 dalla research semiconduttori (che
  prima non contribuiva nessuno dei suoi 12 eventi: date italiane) e 7 dalla bitcoin (date
  italiane in grassetto); gli altri eventi erano già in libreria da schede. Etichette dalla riga:
  +34 guadagnate, 5 perse — 2 contaminazioni vere tolte (Tankan; `fixing` preso da una
  frase che lo *nega*), 2 legittime perse (Ryazan, `boj_normalization` sul 19/03/2024),
  recuperabili con `mechanism` nel registro. Le `AC` seguono il template (data = prima
  seduta di reazione), perché l'event study ancora T=0 alla chiusura del primo giorno ≥ data.
- Nuovo `recupero.py` (prepara / promuovi) e **pilota sulla research BoJ** in
  `knowledge_base/_recupero/Giappone : Bank of Japan.yaml`, **non ancora promosso**: 9
  dichiarazioni nuove, 9 concordi con schede già esistenti (verifica indipendente delle
  regole, inversioni comprese — conteggi dopo la regola della sorpresa), 4 escluse con
  motivo, 14 domande, 6 senza azione. Simulazione
  di promozione su copia del registro: tutto valido. Template delle research nuove aggiornato
  alla tabella canonica. Suite `kb` a 71 asserzioni più il check di `recupero.py`.

---

## [ ] Run 5d — Recupero delle righe già scritte
**ID report:** R01
**Modello:** Opus 5.5 · effort high
**Precondizione:** il maintainer ha **rivisto il pilota BoJ**.

✅ **DECISO dal maintainer il 2026-09-23: il verso è la SORPRESA rispetto al già prezzato**,
non il meccanismo in astratto. Scritto in entrambi i template (scheda e research) e applicato
al pilota: i due conflitti si chiudono a `pos` come le schede, e due righe BoJ su rialzi
«ampiamente attesi» tornano domande. Da non rinegoziare. Conseguenza per il recupero: il
verso narrativo di una research vecchia vale solo se la riga dice che l'evento era una
sorpresa o non dice che era scontato; «atteso/telegrafato» + verso del meccanismo → domanda.

⚠ **Questione di metodo emersa dal pilota, da decidere prima di tutto.** Cosa significa
«verso atteso»? Il pilota ha trovato due letture incompatibili già presenti nei dati:
- **pressione del meccanismo in sé** — un rialzo spinge lo yen su → `JPY=X neg`. È quella
  che scrivono le research;
- **sorpresa rispetto a quanto già prezzato** — il rialzo del 19/03/2024 era scontato,
  l'informazione nuova era la guidance accomodante → yen più debole → `pos`. È quella che
  hanno usato le schede di settembre (14/09 e 18/09), e il registro rifiuta giustamente una
  revisione che contraddica una scheda.
Stesso conflitto sul 2025-07-31. La risposta va scritta **in entrambi i template** (scheda e
research): oggi entrambi dicono «pressione attesa» e ammettono tutte e due le letture.

- [x] Decidere la regola del verso (sorpresa) e scriverla nei due template.
- [x] Rivedere e promuovere il pilota BoJ (`recupero.py promuovi`) — 2026-09-23.
      Promosse 32 righe: gli 11 versi già scritti dalle schede sono tutti concordi, nessuna coppia delle schede è cambiata. 2016-09-21 JPY=X **non** escluso:
      un veto nel registro spegne anche il `pos` delle schede. Il 2024-08-05 è escluso come riga di esito, come l'08-06.
      I tre Nikkei il cui verso la riga non scrive (2016-01-29, 2024-03-19, 2024-07-31) restano aperti: riempirli sarebbe look-ahead.
- [ ] Le altre research con tabella, in ordine di valore: prima quelle sugli asset che le
      schede usano davvero come `direction_reference` (comando per vederli in §9 della spec).
      Pesando le righe post-2011 per quante schede usano i loro ticker, il 2026-09-23 venivano
      prima **Dazi e guerra commerciale USA** e poi **Russia-Ucraina attrito energetico** (i più usati sono `BZ=F` e `^GSPC`).
      ⚠ Prima di preparare: confrontare ogni esclusione con i versi delle schede sulla stessa coppia.
      - [x] **Dazi** — 2026-09-23, 60 righe promosse. Un'entrata in vigore di una misura il cui annuncio
        è nella stessa tabella conta come scontata → esclusa. 2020-01-15 lasciato alla scheda (`pos`,
        benché la riga dica «scontato»); 2025-12-08 SOXX aperto (le contro-restrizioni erano note?).
      - [x] **Russia-Ucraina attrito energetico** — 2026-09-23, 46 righe promosse, nessuna aperta.
        «Marginale» + «Atteso» → `neutral` (6 pacchetti UE); un picco di prezzo come data d'ancora
        (Brent 2022-03-08, TTF 2022-08-22) → escluso. Etichette di meccanismo prese da quelle in libreria.
      - [ ] **Sorprese macro e reaction function** — prossima (poi raffinerie russe, Brasile fiscale).
- [ ] Le schede senza `direction_reference` (agosto e prima metà di settembre): `recupero.py
      prepara` oggi gestisce solo le research, serve il ramo per le schede. Per una scheda
      l'asset non è nella riga: va scelto fra i ticker del suo event study.
- [ ] Le date spurie delle research in formato libero (note tecniche, date di scrittura):
      durante il recupero di ciascuna, con esclusione motivata.

> **Finché il Run 5d non è chiuso: non commissionare nuove research.** Oggi però una research
> nuova scritta col template aggiornato entra già pulita (tabella canonica, prosa spenta):
> il divieto resta per prudenza finché il metodo del verso non è deciso.

---

## [ ] Run 6 — `event_id`
**ID report:** R02
**Modello:** Opus 5 · effort high
**Precondizione:** Run 5b chiuso.

Il più invasivo: chiavi, matching e migrazione dati.

- [ ] Oggi la chiave è `(date, theme)` (`analogues.py` riga ~392): Tankan giapponese e ISM
      statunitense dello stesso giorno vengono **fusi**, e la query `japan_release AND ism`
      recupera il 1 aprile 2024 pur non esistendo alcun evento che soddisfi entrambi.
- [ ] `event_id` distinto dalla data, che tiene insieme attributi e provenienza dello stesso evento.
- [ ] Selezionare prima gli **eventi** pertinenti, deduplicare le **date di mercato** solo dopo,
      per il calcolo dei rendimenti. La deduplicazione degli anchor già nell'event study **si conserva**.
- [ ] Query di regressione con risultati attesi e **casi negativi**: un Tankan non deve diventare
      un ISM americano per unione delle fonti.

---

## [ ] Run 7 — Forecast identificate
**ID report:** R09
**Modello:** Opus 5 · effort medium

Logica chiara, vincolo delicato: **non riscrivere il track record già registrato.**

- [ ] `forecast_tracking.parse_card` (riga ~119): acquisire una dichiarazione esplicita
      «previsione attiva» / «solo statistica descrittiva» / «scenario alternativo».
      Oggi ogni mediana di tabella diventa una previsione, anche quando il runbook dice di no.
- [ ] Chiave del ledger (riga ~228): aggiungere **scenario** e `forecast_id`. Oggi due tabelle
      dello stesso asset/orizzonte con mediane opposte collidono e vince la prima.
- [ ] Salvare prezzi e date target usati, più la versione della scheda: oggi le valutazioni
      non sono riproducibili.
- [ ] Separare valutazione **congelata** al momento e **ricalcolo** su dati revisionati.
- [ ] Una correzione della scheda deve aggiornare la registrazione, non essere ignorata.

---

## [ ] Run 8 — Mensile allineato
**ID report:** R12
**Modello:** Sonnet 5 · effort medium
**Precondizione:** Run 7 chiuso (riusa il codice di estrazione scorecard).

- [ ] `monthly_digest.latest_scorecard_excerpt` (riga ~69): includere la tabella per asset 5-bis,
      non solo sintesi e sezione per tema.
- [ ] `forecast_tracking.py` (riga ~657): la tabella per tema usa ancora una correlazione
      aggregata fra asset — proprio l'aggregazione che il giornaliero ha abbandonato.
- [ ] Regimi selezionati **per data del report**, non «ultima fase elencata».
- [ ] `PHASE6_RUNBOOK.md` (riga ~9): togliere le affermazioni numeriche e direzionali fisse
      sull'edge per tema.
- [ ] Il validatore mensile attuale **respinge già** i report incompleti di giugno e agosto:
      non è un buco da tappare. Resta da completare il consuntivo delle previsioni mensili,
      da non confondere col ledger giornaliero.

---

## [ ] Run 9 — Istruzioni canoniche
**ID report:** R13
**Modello:** Sonnet 5 · effort medium

Lavoro editoriale su Markdown. **Le scelte le fa Riccardo:** questo run gli presenta le
divergenze e aspetta, non decide da solo.

- [ ] Divergenze da risolvere:
      - prompt briefing/wrapper ammettono edizioni parziali, il controllo di salute pretende
        esattamente venti storie;
      - il template glossario dice di non rispiegare le sigle, PHASE5 ne prescrive l'espansione;
      - «scrivi il file una volta sola» convive con scaffold + modifica;
      - «non rileggere ciò che hai appena scritto» confonde risparmio di contesto con verifica;
      - il recupero DB ha un fallback FRED per lo spread che `references/quando_si_rompe.md`
        (riga ~206) **vieta** (produrrebbe una serie mensile al posto della giornaliera).
- [ ] Anche la descrizione dello spread in `ASSETS` è ancora mensile/FRED e viene riscritta
      dall'update: correggere **nella fonte del registro**, non solo nel DB.
- [ ] Una specifica operativa canonica; prompt dei task brevi che la referenziano; template
      compatibili; controlli generati dallo stesso contratto.
- [ ] Spostare cronologie e post-mortem **fuori** dai file caricati a ogni run.
- [ ] Separare regole editoriali, parametri e spiegazioni storiche.

---

## [ ] Run 10 — Telemetria
**ID report:** R14
**Modello:** Sonnet 5 · effort medium

- [ ] Registro unico per esecuzione e fase: identità run, modello, fase, inizio/fine, stato,
      tentativo, token input/cache/output, chiamate agli strumenti, artefatti validati.
      Oggi `record_claude_usage.py` copre giornaliero e briefing; indicizzazione e mensile no.
- [ ] I campi mancanti non devono diventare zero; un JSON malformato deve produrre una riga
      di tentativo fallito, non sparire.
- [ ] Nel giornaliero il trap può rimuovere il grezzo prima della registrazione: registrare
      anche i run interrotti, o almeno uno stato esplicito «consumo sconosciuto».
      «Nessun dato di usage» ≠ «nessun consumo».
- [ ] Misurare consumo **per scheda utile** e **per giornata completata**, includendo
      coordinamento, recuperi e ricerche.
- [ ] Non spacciare per costo: i costi riportati dal client, i token e la quota abbonamento
      sono grandezze diverse. Niente medie storiche riciclate come fattura.

---

## Non pianificati — da rivalutare, NON da anticipare

- **R10 statistica seria** (Opus 5 · high): indipendenza delle osservazioni, accuratezza del
  segno vs ordinamento delle magnitudini vs copertura degli intervalli, raggruppamento per
  giornata/evento. È ricerca, non manutenzione. Ha senso dopo il Run 7, con dati migliori.
- **R11 regime e no-look-ahead** (Opus 5 · high): serve solo se si passa da uso descrittivo a
  backtest vero. Finché non è deciso: YAGNI.
- **Lock e guardie serie derivate**: il report li dà come *rischio dedotto dal codice*, non
  incidenti osservati. Prima verificare che accadano davvero, poi eventualmente correggere.
  (`compute_crack_spread.py` può sostituire lo storico con un risultato vuoto; i lock directory
  di scorecard/indicizzazione/mensile non hanno recupero per proprietario o scadenza.)

---

## Tabella modelli

| Run | Blocco | Modello | Effort |
|---|---|---|---|
| 1 | Sanguinamenti veloci | Sonnet 5 | medium |
| 2 | Prezzi R05 | **Opus 5** | high |
| 3 | Parser + link R08 | Sonnet 5 | medium |
| 4a | Piano completamento R07 | **Opus 5** | high |
| 4b | Implementazione R07 | **Opus 5** | high |
| 5a | Schema KB (design) | **Opus 5** | high |
| 5b | Schema KB + ingestione R04/R01 | **Opus 5** | high |
| 6 | `event_id` R02 | **Opus 5** | high |
| 7 | Forecast R09 | **Opus 5** | medium |
| 8 | Mensile R12 | Sonnet 5 | medium |
| 9 | Istruzioni R13 | Sonnet 5 | medium |
| 10 | Telemetria R14 | Sonnet 5 | medium |

**Criterio:** Opus dove un errore corrompe dati o dove serve tenere in testa tutta la catena;
Sonnet dove il diff è locale e il file da leggere è uno. L'effort alto serve al ragionamento,
non alla lunghezza del codice: il Run 1 scrive più righe del Run 7 e costa un decimo.

**Sul cambio modello:** se sei già su Opus e il run dice Sonnet, **fallo comunque** abbassando
l'effort. Cambiare sessione costa più del risparmio.
