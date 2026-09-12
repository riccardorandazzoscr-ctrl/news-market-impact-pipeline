# Quando si rompe

**Quando aprire questo file:** il report giornaliero non è uscito, il database sembra
vuoto, o qualcosa fallisce senza dirlo.

## ⚠ Il guasto silenzioso 1: login scaduto (401)

**È già successo: dal 25 al 27 giugno 2026 il report non è stato prodotto per tre
giorni, e nessuno se n'è accorto.**

La pipeline girava benissimo — database, analoghi, indice tutti a posto. A fallire era
solo la chiamata `claude -p` headless, con `401 Invalid authentication credentials`.

**Causa:** il token OAuth nel Keychain di macOS (voce `Claude Code-credentials`, account
`riccardo`/`bimbum1227`) era scaduto il 24 giugno, e **nei run launchd headless non si
rinnova da solo.**

**Come si risolve:** Riccardo rifà `claude /login` **dal proprio terminale**.

⚠ **Da dentro una sessione Claude Code il login non si verifica in modo affidabile**:
la sessione ha `ANTHROPIC_BASE_URL` impostato, quindi usa un percorso di autenticazione
diverso da quello di launchd. Può sembrare tutto a posto mentre il job automatico è
fermo.

**Protezioni già applicate a `run_daily_analysis.sh`:**
1. Se l'uscita è diversa da zero o manca `_index.md` → riga `ERROR` nel log **e notifica
   sul desktop** (riconosce il 401 e dice di rifare il login). Basta col guasto muto che
   dura giorni.
2. Accetta una **data come primo argomento** (`TODAY=${1:-$(date +%Y-%m-%d)}`) per
   recuperare a mano i giorni saltati.

**Se ricapita spesso**, l'opzione strutturale è una API key dedicata passata via
variabile d'ambiente nel plist: più stabile di OAuth per l'automazione.

## ⚠ Il guasto silenzioso 2: briefing letto a metà (2026-09-07)

**Il 7 settembre il run è partito su un briefing ancora in scrittura e non se n'è
accorto.** Alle 09:15:42 il file conteneva **solo l'intestazione HTML** — 2.833 byte,
zero notizie; quello completo (33.947 byte, 20 notizie) è arrivato circa un minuto dopo.

Il punto che rende il guasto insidioso: il `digest` sul file parziale ha prodotto una
tabella **vuota senza errore**, e a log comparivano `START` e `DB ok` del tutto regolari.
Solo un controllo umano ha evitato un `_index.md` vuoto spacciato per run riuscito.

**Causa.** `WatchPaths` nel plist sorveglia la **cartella** dei briefing, quindi il job
scatta quando il file *compare*, non quando il generatore ha finito di scriverlo. Lo
script controllava solo `-f "$BRIEF"`, cioè l'esistenza.

⚠ Uscire e aspettare un nuovo trigger **non** funziona: le scritture successive sullo
stesso file non modificano la cartella, e infatti nel log del 07/09 non c'è nessun terzo
trigger dopo quello sul file parziale. Il run di quel giorno non sarebbe più ripartito.

**Protezione applicata** (`run_daily_analysis.sh`, funzione `brief_completo`): il file è
accettato solo se contiene `</body>` **e** almeno 20 blocchi `class="story"` — invariante
verificata su tutti i 138 briefing in archivio, che ne hanno esattamente 20. Se è
incompleto lo script **attende dentro il processo** fino a 10 minuti, ricontrollando ogni
15 secondi; se allo scadere non si è completato, fallisce con `ERROR`, notifica desktop
ed `exit 1` — nessuna analisi invece di un'analisi vuota.

- L'attesa avviene **dopo** il lock, così un trigger sovrapposto esce subito invece di
  mettersi in coda ad aspettare anche lui.
- Se cambia il layout del briefing, `class="story"` va aggiornato **sia** qui **sia** in
  `parse_briefing.py`, che usa la stessa definizione per contare le notizie.
- Test: `./run_tests.sh briefing` (34 controlli, inclusa la corsa riprodotta davvero).

## ⚠ Il guasto silenzioso 3: analisi interrotta a metà (2026-09-11)

**L'11 settembre il run si è fermato a metà e ha spedito lo stesso il report, senza un
allarme.** Alle 09:24 Claude ha esaurito il **limite di sessione** (`You've hit your
session limit · resets 12:40pm`) dopo 6 schede su 20, uscendo con codice 1.

Il punto insidioso è che la protezione del guasto 1 si è **ritorta contro**: quella regola
dice "se `_index.md` c'è, il lavoro è stato scritto, non buttare via il giorno". Ma
`_index.md` nasce come **scheletro** di triage (tutte le righe a ⏳) e viene compilato
alla fine — quindi esiste fin dal primo minuto. Risultato: `WARN` invece di `ERROR`,
nessuna notifica, e su Telegram un'analisi con la tabella vuota che sembrava normale.

Stessa dinamica il **31/07** (limite di sessione) e il **19/07** (`connection closed`):
tre run monchi, tre report partiti in silenzio.

**Secondo effetto, peggiore del primo:** l'idempotenza guardava anch'essa la sola
esistenza del file, quindi lo scheletro **bloccava i tentativi successivi**. Alle 10:07
il ri-trigger ha loggato `SKIP: analisi già presente` su un'analisi mai finita: senza
cancellare i file a mano, quel giorno non sarebbe più ripartito.

**Protezioni applicate** (`run_daily_analysis.sh`, funzione `index_completo`):

1. Il segnale di successo non è più che `_index.md` **esista**, ma che sia **compilato**:
   nessuna riga ⏳ e nessun segnaposto "Da compilare dopo il triage". Invariante misurata
   su 105 `_index.md` in archivio — i 102 sani non hanno né l'uno né l'altro, i 3 rotti
   hanno entrambi. Sono i marcatori del template in `PHASE5_RUNBOOK.md`: **se cambiano lì,
   vanno cambiati anche qui.**
2. Gli esiti diventano tre invece di due: assente → fallimento pieno; **monco → `ERROR` +
   notifica + didascalia Telegram d'allarme + `exit 1`**, ma le schede prodotte si tengono
   e si spediscono; compilato → successo, anche con exit ≠0 (resta il caso del 10/07).
3. L'idempotenza esce solo davanti a un'analisi **completa**: un giorno monco riparte da
   solo al trigger successivo. Il parziale non si sovrascrive e non si cancella — finisce
   in `_interrotto_<ora>/`, che il prefisso `_` tiene fuori dal glob di `render_report.py`
   e `analogues.py` (altrimenti quelle schede entrerebbero due volte in report e libreria).
4. L'allarme riporta **l'ora di reset del limite**, così il rilancio non è a vuoto.

- Test: `./run_tests.sh analisi` (45 controlli, inclusa la regressione su tutti gli
  `_index.md` in archivio: i 3 giorni rotti noti riconosciuti, i 102 sani accettati).
- ⚠ Il limite di sessione è **esterno**: il codice non può evitarlo, può solo smettere di
  spacciarlo per un successo. Se ricapita spesso, le leve vere sono spostare il run dove
  la finestra di utilizzo è libera, o ridurre il costo del run
  ([economia_del_run.md](economia_del_run.md)).

## ⚠ Il guasto silenzioso 4: il run appeso che non torna più (2026-08-05)

**Il 5 agosto `claude -p` è rimasto appeso 410,9 minuti — sei ore e cinquanta — e il
report è uscito alle 14:36 invece che alle 08:05.** Nessun errore, nessuna notifica:
alla fine il processo è persino tornato con codice 0.

Il danno non è solo il ritardo. Per tutte e sette le ore il **lock è rimasto occupato**,
quindi ogni ri-trigger di `WatchPaths` ha loggato `SKIP: altro run in corso` — il giorno
non poteva ripartire nemmeno volendo, e dall'esterno la pipeline sembrava semplicemente
ferma.

**Causa.** La chiamata era sincrona e senza tetto: uno script che aspetta non ha modo di
distinguere "sta lavorando" da "non tornerà mai". È la stessa famiglia dei guasti 2 e 3
— il codice accetta per buono un segnale che non significa quello che sembra.

**Protezioni applicate** (`run_daily_analysis.sh`):

1. **Tetto di durata** (`RUN_MAX`, 3600s). Come `MIN_STORIES` non è una stima: su 104 run
   in archivio la mediana è 19,4 minuti, il p90 25,8 e il secondo massimo 37,2. Il massimo
   vero, 410,9, **è** il guasto. 3600s sta 1,6 volte sopra il run legittimo più lungo mai
   visto e sui 104 in archivio sarebbe scattato solo sull'05/08. Allo scadere Claude viene
   terminato e il giorno cade nel ramo **INCOMPLETA che esisteva già** (guasto 3): ERROR,
   notifica, Telegram con `--parziale`, `exit 1`, schede prodotte tenute.
2. **Allarme sulla terminazione esterna.** Ctrl-C, `launchctl kill`, logout, spegnimento:
   prima il trap toglieva il lock e basta, quindi un run ucciso non lasciava **niente** a
   log ed era indistinguibile da un job mai partito. Ora scrive `ERROR: ... INTERROTTO dal
   segnale X` e notifica.
3. **Lock a prova di `kill -9`.** Il lock si porta dentro il PID di chi lo tiene. Prima,
   un processo ucciso di netto — i casi in cui il trap di pulizia **non** gira — lasciava
   la cartella lì per sempre: da quel momento ogni run successivo sarebbe uscito con
   `SKIP`, e la pipeline si sarebbe fermata in silenzio e senza scadenza. Un lock il cui
   PID non è più vivo (o che non ne ha, formato vecchio) viene dichiarato `STANTIO` e
   rilevato.

- Test: `./run_tests.sh watchdog` (46 controlli: hang oltre il tetto, parziale tenuto e
  spedito, nessun falso allarme sotto il tetto, TERM a metà run, lock di un morto, lock di
  un vivo, lock senza PID).
- ⚠ Il watchdog uccide il **processo figlio**, non tutto il suo albero: in uno script i job
  non hanno un process group proprio, e un kill di gruppo porterebbe via anche lo script.
- ⚠ `kill -0` non distingue un PID **riciclato** dall'originale. È un rischio accettato: la
  finestra è quella di un riavvio, e sbagliare di qua costa un doppio run improbabile,
  mentre sbagliare di là costa la pipeline bloccata a tempo indefinito.

### ⚠ Trappola per chi tocca questo script: `CLAUDE_PID` non è tua

Scrivendo il watchdog (12/09/2026) la variabile del PID si chiamava `CLAUDE_PID` e veniva
letta nella pulizia **senza essere mai stata azzerata**. Ma l'app Claude Code **esporta
`CLAUDE_PID` nell'ambiente dei processi che lancia**, col PID dell'applicazione stessa:
la pulizia ereditava quel numero e spediva `SIGTERM` all'app dell'utente — che moriva con
codice 143 — a ogni uscita anticipata, per esempio durante i dieci minuti di attesa del
briefing. Si è manifestato come test che venivano uccisi a metà senza spiegazione.

Regola che ne segue: **ogni variabile che finisce dentro un `kill` va azzerata
esplicitamente prima dei trap**, e non deve portare un nome che l'ambiente possa già
usare. Qui si chiamano `PID_HEADLESS` e `PID_GUARDIANO`, azzerate sopra le `trap`.
I casi 8 e 9 di `./run_tests.sh watchdog` tengono ferma sia la sostanza (una sentinella
innocua deve sopravvivere al run) sia la forma (l'azzeramento precede i trap).

## Certificati SSL su Mac

Python 3.12 installato da python.org richiede di lanciare **una volta**:

```
/Applications/Python 3.12/Install Certificates.command
```

Senza, la verifica dei certificati fallisce e **tutte** le chiamate HTTPS si bloccano,
FRED compreso.

## Ricostruire il database dei prezzi

⚠ **`market_data.db` non ha backup** ed è già stato azzerato una volta (29 maggio 2026,
durante una riorganizzazione di file: sovrascritto con un file vuoto da 0 byte).

Non è un dramma: è un artefatto **rigenerabile**, non una fonte primaria. Perderlo costa
tempo di ri-scaricamento, non dati irrecuperabili.

**Come accorgersene:** il file è a 0 byte, oppure mancano le tabelle `assets` e `prices`.

**Procedura:**

```bash
V=news_impact_pipeline/venv/bin/python

# 1. carico storico completo (~15 anni, tutti gli asset di ASSETS via yfinance)
$V news_impact_pipeline/bootstrap_market_data.py

# 2. verifica
sqlite3 market_data/market_data.db "SELECT COUNT(*) FROM assets;"
```

⚠ **Le due serie derivate non tornano da sole:**
- `CRACK_321` si ricalcola al primo `update_market_data.py`, perché parte da ticker già
  in DB. Nessun problema.
- `BTP_BUND_SPREAD` **va ricostruito a mano**: il download automatico da Stooq non
  funziona più. Procedura in [serie_derivate.md](serie_derivate.md).

⚠ **Non usare `fetch_fred_data.py`** per ricostruire lo spread: è la fonte **legacy** e
darebbe una serie **mensile** al posto di quella giornaliera, senza segnalarlo.

**Protezione mai implementata** (resta una buona idea): un dump CSV periodico, o una
copia `.db.bak` **fuori** dalla cartella di lavoro, così uno spostamento di file non
può azzerarla.

## La regola sul database, ogni volta che si sposta qualcosa

Ogni volta che si sposta o riorganizza qualcosa in `~/Claude`, il database va verificato
**prima e dopo**, esplicitamente. Mai un `mv` "a occhio": è così che è sparito la prima
volta. Nel trasloco del 29 luglio la verifica è stata fatta (md5 invariato) ed è andata
bene.
