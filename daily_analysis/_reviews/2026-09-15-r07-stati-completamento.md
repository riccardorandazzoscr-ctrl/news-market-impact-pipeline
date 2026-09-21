# R07 — Stati di completamento verificabili della catena giornaliera

**Piano del Run 4a**, approvato da Riccardo il 2026-09-15. Da eseguire nel **Run 4b**
(Opus 5 · effort high), in una sessione nuova. Origine: `2026-09-15-revisione-pipeline.md`
§R07 e `~/Claude/PIANO_REVISIONE_PIPELINE.md`.

Questo file è la specifica. Non contiene codice di produzione.

---

## Il problema, in una riga

La catena giornaliera ha oggi due soli stati — «`_index.md` compilato» e «non compilato» —
e li usa sia per decidere se c'è lavoro da fare, sia per decidere se il lavoro è riuscito.
Tutto ciò che sta **dopo** l'indice (render, consegna) è invisibile: fallisce in `WARN` e
il run esce `0`.

Guasti già accaduti che cadono in questo buco: 07/09 (briefing parziale → zero notizie
senza errore), 11/09 (limite di sessione a 6 schede su 20 → scheletro spedito come
completo), 24/08 (529 → silenzio totale). Più il buco aperto: un indice **vuoto** passa
`index_completo`, perché non ha né `⏳` né il segnaposto della Sintesi.

## Le tre decisioni prese nel Run 4a

Sono scelte di Riccardo, non default: chi esegue il Run 4b non le rinegozia da solo.

1. **La verità è il disco.** Le fasi si verificano rileggendo gli artefatti. `_state.json`
   è una **ricevuta**, non la fonte: tiene solo ciò che il disco non sa. Se stato e disco
   divergono, vince il disco.
2. **Dipendenza dai prezzi bloccante, senza scavalco nel codice.** Niente flag
   `--senza-prezzi`. Se i dati non sono pronti l'analisi non parte; si sblocca riparando
   il dato, non aggirando il controllo. Costo accettato e dichiarato: un guasto prolungato
   della fonte prezzi blocca l'analisi del giorno finché non si interviene a mano.
3. **Una scheda si invalida solo se cambia il testo della notizia.** Non le dipendenze.
   Ragione tecnica: `analogues.py build` gira all'inizio di ogni run e include le schede
   appena prodotte, quindi la libreria episodi cambia **sempre** fra un tentativo e il
   successivo — legarci il riuso lo annullerebbe in partenza.

---

## 1. Le sei fasi e la loro verifica

| # | Fase | Verifica (tutta derivata dal disco, salvo dove detto) |
|---|------|--------------------------------------------------------|
| 1 | `input_validato` | `brief_completo` attuale (`</body>` + conteggio ≥ `MIN_STORIES`) **e** impronta del contenuto analizzato registrata in `_state.json` |
| 2 | `dati_pronti` | esiste almeno una riga `prices` con `fetched_at` che inizia per la data di oggi **e** nessuna segnalazione `[freschezza]` su ticker con `assets.source != 'computed'` |
| 3 | `triage_completato` | l'insieme dei `#` delle righe della tabella Triage == l'insieme dei numeri delle notizie nel briefing; ogni riga ha `✅` o `✖` nella colonna Decisione; la sezione `## Sintesi di sessione` non contiene più il segnaposto e non è vuota |
| 4 | `schede_validate` | per ogni riga `✅`: la `news_NN.md` linkata esiste, non è vuota, e contiene le intestazioni `### Risultati` (dentro `## Event study`) e `## Provenance` |
| 5 | `html_prodotto` | `report.html` esiste, `mtime` ≥ di quello di `_index.md` e di ogni `news_*.md` presente, e contiene un'ancora `doc-news_NN` per ogni scheda linkata |
| 6 | `consegna_confermata` | ricevuta in `_state.json`: esito, artefatti spediti, impronta del `report.html` spedito |

Note di merito, verificate sui dati veri e non dedotte:

- **Il caso «indice vuoto» muore sulla fase 3.** Un file vuoto ha zero righe di triage, il
  briefing ne ha venti: il confronto fra insiemi fallisce. È la verifica che oggi manca.
- **`assets.source = 'computed'`** distingue già le due serie derivate
  (`BTP_BUND_SPREAD`, `CRACK_321`): non serve alcuna lista scritta a mano nel codice.
  Hanno una procedura di aggiornamento manuale documentata
  (`references/serie_derivate.md`), quindi la loro staleness resta un **warning**.
  ⚠ Senza questa esclusione l'analisi sarebbe bloccata oggi stesso: verificalo prima di
  implementare con
  `sqlite3 -readonly market_data/market_data.db "SELECT ticker, source, MAX(date) FROM prices WHERE ticker='BTP_BUND_SPREAD' GROUP BY ticker;"`
- **`fetched_at` ha due formati** nel DB: `2026-09-15T15:53:59` (yfinance) e
  `2026-09-15 15:53:59` (derived). Confronto **per prefisso di data**, mai `==`.
- **Il consolidamento è reale:** più righe di triage possono linkare la stessa scheda
  (il 14/09 le righe 02, 03, 04, 05 e 08 puntano tutte a `news_01.md`). Ogni verifica e
  ogni impronta che riguarda una scheda lavora quindi sull'**insieme** delle righe che la
  linkano, mai su una sola.
- Le verifiche 3, 4 e 5 riusano i marcatori del template di `PHASE5_RUNBOOK.md`. Come già
  scritto in `index_completo`: **se cambiano lì, vanno cambiati anche qui.**

## 2. `_state.json` — cosa contiene e cosa no

Vive in `daily_analysis/<data>/_state.json`. Tiene **solo** ciò che non è ricostruibile
dal disco:

- `briefing`: impronta del contenuto analizzato del briefing (identità dell'input)
- `items`: impronta per notizia, chiave = il numero della notizia
- `consegna`: ricevuta dell'invio (quando, quali artefatti, esito, impronta del
  `report.html` spedito, se era `--parziale`)

Non contiene lo stato delle fasi: quello si calcola. Un `_state.json` assente non è un
errore — significa solo che l'input non è ancora stato registrato e che la consegna è
**sconosciuta**, non fallita.

**Giornate già archiviate:** non hanno `_state.json` e non lo avranno. Nessuna migrazione,
nessun backfill. Per loro le fasi 1–5 si calcolano comunque dal disco e la fase 6 risulta
«consegna sconosciuta». Non trattarle come fallite.

## 3. Dove sta il calcolo

**File nuovo: `news_impact_pipeline/stato_giornata.py`.** Non un sottocomando di
`pipeline_tools.py`: quello è l'utensile dell'**agente** (assets, match, new-card, digest)
ed è già a ~500 righe; questo serve al **wrapper**. Pubblici diversi, file diversi.

Interfaccia minima:

```
stato_giornata.py --date AAAA-MM-GG          # stampa la prima fase incompleta e il perché
stato_giornata.py --date AAAA-MM-GG --json   # stessa cosa in JSON, per il wrapper
```

Il flag `--json` serve al wrapper; l'uscita leggibile serve a Riccardo, che deve poter
chiedere a mano «a che punto è la giornata, e perché si è fermata lì» senza leggere lo
shell. È il requisito «niente scatole nere» applicato qui: il giudizio automatico resta
ispezionabile.

**Flag nuovo: `parse_briefing.py --impronte`** — emette l'impronta complessiva del briefing
e quella per notizia (titolo + corpo + fonti, spazi normalizzati). Sullo stesso parser che
il Run 3 ha già reso l'unica fonte di verità del conteggio: non se ne aggiunge un secondo.

## 4. `run_daily_analysis.sh` — le modifiche

**a) Sparisce l'uscita anticipata su `index_completo`** (oggi riga ~99). Al suo posto una
sola domanda a `stato_giornata.py` e un ramo per risposta:

| Prima fase incompleta | Cosa fa il run |
|---|---|
| nessuna (tutto fatto) | `SKIP`, esce 0 — l'idempotenza di oggi, ma vera |
| `input_validato` | attende / esce come già fa oggi |
| `dati_pronti` | vedi punto (b) |
| `triage_completato` o `schede_validate` | lancia `claude -p` (unico ramo che costa) |
| `html_prodotto` | **solo** render + consegna, senza ripagare Claude |
| `consegna_confermata` | **solo** invio |

Questi ultimi due rami sono la riparazione che l'11/09 mancava: oggi il ritentativo delle
09:15 esce alla riga 99 prima di arrivarci.

**b) Il controllo prezzi e la corsa di `WatchPaths`.** Il briefing delle 07:30 fa scattare
l'analisi prima dell'aggiornamento prezzi delle 08:00. `WAIT_MAX` è 600s: un'attesa secca
scadrebbe alle 07:41, prima che i prezzi esistano, e suonerebbe l'allarme ogni mattina.
Quindi due regimi, separati da una soglia oraria:

- **prima** di `DATI_PRONTI_ENTRO` (nuova costante, default `08:30`, sovrascrivibile come
  `MIN_STORIES` e `WAIT_MAX` per la suite) e dati non pronti → riga di log e **uscita
  silenziosa, codice 0**. Ci pensa il run di calendario delle 08:15.
- **dopo** quella soglia e dati non pronti → attesa fino a `WAIT_MAX`, poi **ERROR +
  notifica + uscita ≠0**, esattamente come già fa col briefing incompleto.

Il commento accanto alla costante deve dire che il valore dipende dall'orario in
`launchd/com.riccardo.newsimpact.marketdata-update.plist` (08:00), che resta la fonte.

**c) Riuso delle schede al ritentativo.** Oggi i residui finiscono **tutti** in
`_interrotto_<ora>/` e si rifà da capo: l'11/09 significava buttare 6 schede su 20 già
pagate. Nuova regola:

1. Se l'impronta del briefing in `_state.json` **non** coincide con quella attuale
   (brief rigenerato, o giorno ripreso da un input diverso) → si archivia tutto in
   `_interrotto_<ora>/` e si rifà da capo, come oggi. È la ragione per cui lo stato è
   legato all'identità dell'input e non alla data.
2. Se coincide → una scheda **resta al suo posto** se tutte le righe di triage che la
   linkano sono `✅`, le impronte di quelle notizie coincidono con `_state.json`, e la
   scheda passa la verifica della fase 4. `_index.md` **non** viene archiviato: contiene
   le decisioni di triage già prese.
3. Tutto il resto (schede non valide, schede orfane) → archiviato.

**d) Il prompt diventa dinamico.** Quando ci sono schede riusate, il prompt elenca quali
esistono già e da quali righe `⏳` ripartire, invece di chiedere il triage completo.
Attenzione: la sezione «ECONOMIA DEL RUN» del prompt e il runbook restano invariati —
questo non è il momento di toccarli.

**e) Render e consegna smettono di essere `|| WARN`.** Il loro esito entra nello stato:
un render fallito lascia la giornata in `html_prodotto` e il ritentativo successivo la
riprende. La ricevuta di consegna si scrive in `_state.json` **solo** se
`send_telegram.sh` esce 0 — cosa che dal Run 1 significa già «tutti gli artefatti attesi
sono partiti e Telegram ha risposto `"ok":true`».

## 5. Il check runnabile

`news_impact_pipeline/tests/test_stato_giornata.py`, da aggiungere a `run_tests.sh`.
`assert`, nessun framework, nessuna fixture. Copre le sei fasi su cartelle sintetiche in
`tmp`, più i tre casi veri che hanno fatto danno:

- `_index.md` **vuoto** → si ferma su `triage_completato` (oggi passa);
- `_index.md` a metà con una parte delle schede prodotte → si ferma su
  `schede_validate`, e le schede valide risultano riusabili;
- `report.html` reso ma consegna mai confermata → si ferma su `consegna_confermata`, e
  il ramo corrispondente non richiede l'agente.

Più un caso negativo: **impronta del briefing diversa** → nessuna scheda riusabile,
anche se i file ci sono tutti.

## 6. Fuori perimetro, di proposito

- Nessuna macchina a stati generica, nessun registro dei run, nessuna astrazione
  riutilizzabile dalle altre fasi (brief, scorecard, mensile). Se servirà, sarà un altro
  run.
- **Nessuna modifica ai plist.** `WatchPaths` resta dov'è e diventa innocuo grazie alla
  fase 2.
- Il controllo «un solo scheduler proprietario per fase» è un **passo di verifica
  manuale** del Run 4b, non codice — configurato, abilitato e caricato sono tre cose
  diverse:
  ```bash
  launchctl print-disabled gui/$(id -u) | rg newsimpact
  launchctl list | rg newsimpact
  diff <(ls ~/Library/LaunchAgents | rg newsimpact) <(ls news_impact_pipeline/launchd)
  ```
- La descrizione mensile/FRED di `BTP_BUND_SPREAD` in `assets.description` è sbagliata,
  ma è **materia del Run 9**: non toccarla qui.
- La telemetria di questi nuovi stati è **materia del Run 10**.

## 7. Verifica di chiusura del Run 4b

Il blocco Verifica standard del piano, più:

```bash
cd /Users/riccardo/Claude/mercati_finanza
V=news_impact_pipeline/venv/bin/python
PYTHONDONTWRITEBYTECODE=1 $V news_impact_pipeline/tests/test_stato_giornata.py
# regressione sulle giornate reali in archivio: nessuna deve risultare "fallita"
# per la sola assenza di _state.json
for d in daily_analysis/2026-[0-9][0-9]-[0-9][0-9]; do   # solo cartelle-data, niente *_backup
  $V news_impact_pipeline/stato_giornata.py --date "${d:t}"
done
cd news_impact_pipeline && ./run_tests.sh briefing && ./run_tests.sh analisi
```

⚠ **Non lanciare la routine vera, non spedire su Telegram, non scaricare prezzi** senza
che Riccardo lo chieda esplicitamente.
