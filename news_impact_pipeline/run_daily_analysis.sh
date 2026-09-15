#!/bin/zsh
# run_daily_analysis.sh — wrapper lanciato da launchd (Fase 5).
#
# Lanciato sia alle 08:15 (StartCalendarInterval) sia ad ogni nuovo file
# nella cartella dei briefing (WatchPaths). È idempotente e auto-protetto:
#   - se l'analisi di oggi è già fatta (_index.md esiste) → esce
#   - se il briefing di oggi non è ancora arrivato → esce (sarà ri-triggerato
#     da WatchPaths appena il file atterra)
#   - se il briefing c'è ma è ancora a metà scrittura → aspetta che si completi,
#     e se non si completa fallisce ad alta voce invece di analizzare il vuoto
#   - lock per evitare run concorrenti (calendario + watchpath sovrapposti)
#   - ricostruisce il DB mercati se risulta incompleto
# Poi lancia Claude Code headless sul runbook.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# --- Configurazione --------------------------------------------------------
MODEL="claude-opus-5"   # analisi giornaliera: qualità elevata su molte schede

# Integrità del briefing (guasto del 2026-09-07, vedi la fase input_validato).
# Un briefing pubblicato può essere parziale: contiene tutte e sole le notizie nuove
# e verificabili disponibili al momento del run. La soglia minima distingue quindi
# un briefing valido da un file vuoto o scritto a metà; il tag </body> resta il segno
# di pubblicazione atomica. Sovrascrivibile per le prove della suite.
MIN_STORIES=${MIN_STORIES:-1}
WAIT_MAX=${WAIT_MAX:-600}       # attesa massima del completamento, in secondi
WAIT_STEP=${WAIT_STEP:-15}      # ogni quanto ricontrollare

# Ora entro cui i prezzi del giorno devono essere aggiornati (HH:MM, confronto fra
# stringhe: tenere lo zero iniziale). Prima di quest'ora un run innescato da
# `WatchPaths` esce in silenzio invece di allarmarsi; dopo, il ritardo è un guasto.
# ⚠ Il valore dipende dall'orario del job dei prezzi, che è la fonte:
# launchd/com.riccardo.newsimpact.marketdata-update.plist (08:00).
DATI_PRONTI_ENTRO=${DATI_PRONTI_ENTRO:-08:30}

# Tetto di durata del run headless (guasto del 2026-08-05, vedi il watchdog più sotto).
# Come MIN_STORIES non è una stima: su 104 run in archivio la mediana è 19,4 minuti,
# il p90 25,8 e il secondo massimo 37,2. Il massimo vero — 410,9 minuti — È il guasto,
# non un run lungo. 3600s sta 1,6 volte sopra il run legittimo più lungo mai visto, e
# sui 104 in archivio sarebbe scattato solo su quello.
RUN_MAX=${RUN_MAX:-3600}               # durata massima di `claude -p`, in secondi
RUN_KILL_GRACE=${RUN_KILL_GRACE:-20}   # quanto si aspetta fra il TERM e il KILL
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
BRIEF_DIR="$PROJECT/morning brief"
DAILY="$NEWSDIR/daily_analysis"
LOGDIR="$PIPE/logs"
# Sovrascrivibile per la stessa ragione di MIN_STORIES e WAIT_MAX: la suite in
# tests/ deve poter mettere al suo posto un finto `claude`. launchd non la imposta.
CLAUDE=${CLAUDE:-/opt/homebrew/bin/claude}

mkdir -p "$LOGDIR"
# Data del run: di default oggi. Si può passare una data ISO come primo argomento
# per rigenerare a mano un giorno saltato (backfill), es. dopo un guasto di auth:
#   run_daily_analysis.sh 2026-06-25
# L'idempotenza vale comunque: se _index.md di quel giorno esiste già, esce.
TODAY=${1:-$(date +%Y-%m-%d)}
BRIEF="$BRIEF_DIR/${TODAY}-morning-briefing.html"
INDEX="$DAILY/$TODAY/_index.md"
LOG="$LOGDIR/${TODAY}.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Quante notizie contiene il briefing — il parser VERO (`parse_briefing.py --count`),
# non un grep su `class="story"`: un HTML senza il contenitore <section> richiesto
# dal parser passava il vecchio controllo grep pur estraendo zero notizie davvero.
conta_story() { "$PY" "$PIPE/parse_briefing.py" --file "$BRIEF" --count 2>/dev/null || echo 0; }

# ⚠ Il briefing è FINITO di essere scritto? Non c'è più una funzione qui: i due
# segni — il tag `</body>` e il conteggio delle notizie — sono la fase
# `input_validato` di `stato_giornata.py`, così il wrapper e il controllo a mano
# danno per forza la stessa risposta.
#
# `WatchPaths` sorveglia la CARTELLA, quindi il job scatta quando il file viene
# creato — non quando il generatore ha finito di scriverlo. Il 2026-09-07 alle
# 09:15:42 il run è partito su un file di 2.833 byte con la sola intestazione HTML;
# quello completo (33.947 byte, 20 notizie) è arrivato un minuto dopo. Il digest sul
# file parziale ha prodotto ZERO notizie *senza errore*, con START e DB ok regolari a
# log: senza un controllo umano il run sarebbe finito con un `_index.md` vuoto e
# nessun segnale di guasto — la classe di guasto silenzioso di `quando_si_rompe.md`.

# A CHE PUNTO è la giornata? (R07, revisione del 2026-09-15)
#
# Prima qui c'era `index_completo`, che guardava solo se `_index.md` avesse ancora
# righe ⏳ o il segnaposto della Sintesi. Erano due stati in tutto — compilato o no —
# e coprivano solo il tratto centrale della catena: un file VUOTO li superava
# entrambi, e un render o un invio falliti (ridotti a WARN più sotto) restavano
# invisibili, tanto che il ritentativo usciva da qui prima di poterli riparare.
#
# `stato_giornata.py` risponde invece con la PRIMA FASE INCOMPLETA fra sei —
# input_validato, dati_pronti, triage_completato, schede_validate, html_prodotto,
# consegna_confermata — rileggendo ogni volta il disco. Lanciato a mano senza
# `--fase` spiega anche PERCHÉ si è fermato lì.
#
# Interrogarlo costa ~1s (legge briefing, indice, schede, report e database), quindi
# lo si chiama quando lo stato può essere CAMBIATO, non a ogni riga: `leggi_stato`
# prende tutto in una volta, `fase` è la versione breve per le attese.
fase() { "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --fase 2>>"$LOG"; }

# Tutto ciò che serve al wrapper, in una sola lettura. `input_riconosciuto` = il
# briefing sul disco è lo stesso di cui è registrata l'impronta; `RIUSABILI` =
# schede le cui righe di triage sono tutte tenute e il cui testo di partenza non è
# cambiato (vedi stato_giornata.schede_riusabili).
#
# ⚠ Le variabili si inizializzano PRIMA dell'eval: lo script gira con `set -u`, e se
# stato_giornata.py non stampasse nulla (venv rotto, errore interno) resterebbero
# non definite e il primo `(( RICONOSCIUTO ))` ucciderebbe il run. Il default
# prudente è "non riconosco niente": si archivia e si rifà, come prima.
FASE=""
RICONOSCIUTO=0
REGISTRATO=0
RIUSABILI=()
leggi_stato() {
  eval "$("$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --json 2>>"$LOG" | "$PY" -c '
import json, shlex, sys
s = json.load(sys.stdin)
print("FASE=" + shlex.quote(s["fase"] or "completa"))
print("RICONOSCIUTO=" + ("1" if s["input_riconosciuto"] else "0"))
print("REGISTRATO=" + ("1" if s["impronta_registrata"] else "0"))
print("RIUSABILI=(" + " ".join(shlex.quote(x) for x in s["schede_riusabili"]) + ")")
')"
}

# --- Idempotenza -----------------------------------------------------------
# Si esce solo davanti a una giornata COMPLETA fino alla consegna. Con il vecchio
# controllo di sola esistenza, uno scheletro lasciato da un run interrotto bloccava
# per sempre i tentativi successivi: l'11/09 alle 10:07 il ri-trigger ha loggato
# "SKIP" su un'analisi mai finita, e l'unico modo di rifarla era cancellare i file
# a mano.
leggi_stato
if [[ "$FASE" == "completa" ]]; then
  log "SKIP: giornata $TODAY già completa (analisi resa e consegnata)."
  exit 0
fi

# --- Briefing arrivato? ----------------------------------------------------
if [[ ! -f "$BRIEF" ]]; then
  log "WAIT: briefing $TODAY non ancora presente. Esco (ri-trigger all'arrivo)."
  exit 0
fi

# --- Lock (evita doppio run calendario+watchpath) --------------------------
# Il lock si porta dentro il PID di chi lo tiene. Senza, un processo ucciso di netto
# — `kill -9`, corrente staccata: i casi in cui il trap di pulizia NON gira — lasciava
# la cartella lì per sempre, e da quel momento OGNI run successivo sarebbe uscito con
# "SKIP: altro run in corso": la pipeline ferma in silenzio e senza scadenza.
#
# ⚠ `kill -0` non distingue un PID riciclato dall'originale. È un rischio accettato:
# la finestra è quella di un riavvio, e sbagliare di qua costa un doppio run
# improbabile, mentre sbagliare di là costa la pipeline bloccata a tempo indefinito.
LOCK="$LOGDIR/.lock"

# ⚠ I due PID si azzerano QUI, prima di ogni trap, e non si chiamano CLAUDE_PID.
# Incidente del 2026-09-12: la pulizia faceva `kill "$CLAUDE_PID"` fidandosi che la
# variabile fosse vuota finché non l'avevamo riempita noi. Ma l'app Claude Code
# esporta `CLAUDE_PID` nell'ambiente dei processi che lancia, col PID dell'app
# stessa: la pulizia ereditava quel numero e spediva SIGTERM all'applicazione
# dell'utente — che moriva con codice 143 — ogni volta che il run usciva prima di
# aver avviato Claude, per esempio durante i dieci minuti di attesa del briefing.
# Un nome proprio non basta da solo: senza l'azzeramento esplicito, qualunque
# variabile d'ambiente omonima tornerebbe a puntare un processo che non è nostro.
PID_HEADLESS=""
PID_GUARDIANO=""

pulisci() {
  [[ -n "$PID_GUARDIANO" ]] && kill "$PID_GUARDIANO" 2>/dev/null
  [[ -n "$PID_HEADLESS" ]]  && kill "$PID_HEADLESS" 2>/dev/null
  [[ -n "${RAW:-}" ]]          && /bin/rm -f "$RAW"
  [[ -n "${SCADUTO:-}" ]]      && /bin/rm -f "$SCADUTO"
  /bin/rm -f "$LOCK/pid" 2>/dev/null
  rmdir "$LOCK" 2>/dev/null
  return 0
}

# Terminazione esterna: Ctrl-C di chi lancia a mano, `launchctl kill`, logout,
# spegnimento. Prima il trap toglieva il lock e basta — nel log non restava NIENTE e
# sul telefono nemmeno, quindi un run ucciso era indistinguibile da un job mai
# partito. L'unico modo di accorgersene era notare il `.raw_<data>.json` rimasto.
interrotto() {
  log "ERROR: run $TODAY INTERROTTO dal segnale $1 (analisi non completata). Rilancia: run_daily_analysis.sh $TODAY"
  /usr/bin/osascript -e "display notification \"run $TODAY interrotto ($1): analisi non completata.\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  exit 1
}

prendi_lock() {
  if mkdir "$LOCK" 2>/dev/null; then
    print -r -- $$ > "$LOCK/pid"
    return 0
  fi
  local pid=$(cat "$LOCK/pid" 2>/dev/null)
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    return 1                     # c'è davvero un run in corso
  fi
  # Nessun pid (lock del vecchio formato) o pid di un processo morto: è un relitto.
  log "STANTIO: lock di un processo non più vivo (pid=${pid:-assente}). Lo rilevo."
  print -r -- $$ > "$LOCK/pid"
  # Riletto: se due trigger ravvicinati trovano lo stesso relitto vince chi scrive
  # per ultimo, e l'altro esce invece di mettersi a girare in parallelo.
  [[ "$(cat "$LOCK/pid" 2>/dev/null)" == "$$" ]]
}

if ! prendi_lock; then
  log "SKIP: altro run in corso (lock presente)."
  exit 0
fi
trap 'pulisci' EXIT
trap 'interrotto TERM' TERM
trap 'interrotto INT'  INT
trap 'interrotto HUP'  HUP

# --- Il briefing è completo? (guasto del 2026-09-07) -----------------------
# Si ASPETTA dentro il processo invece di uscire e contare su un nuovo trigger:
# `WatchPaths` sorveglia la cartella e scatta quando il file compare, ma le
# scritture successive sullo stesso file non la modificano — nel log del 07/09 non
# c'è infatti nessun terzo trigger dopo quello sul file parziale. Uscendo qui, il
# run di quel giorno non sarebbe più ripartito da solo. L'attesa avviene DOPO il
# lock, così un trigger sovrapposto esce subito invece di mettersi ad aspettare
# anche lui.
if [[ "$FASE" == "input_validato" ]]; then
  log "PARZIALE: briefing incompleto ($(stat -f%z "$BRIEF" 2>/dev/null) byte, $(conta_story)/$MIN_STORIES notizie). Attendo il completamento (max ${WAIT_MAX}s)."
  waited=0
  while (( waited < WAIT_MAX )); do
    sleep "$WAIT_STEP"
    waited=$(( waited + WAIT_STEP ))
    FASE=$(fase)
    if [[ "$FASE" != "input_validato" ]]; then
      log "OK: briefing completo dopo ${waited}s ($(conta_story) notizie)."
      break
    fi
  done
fi

# Scaduta l'attesa senza completamento è un guasto vero, e va detto ad alta voce:
# meglio nessuna analisi con un allarme che un'analisi vuota in silenzio.
if [[ "$FASE" == "input_validato" ]]; then
  MSG="briefing $TODAY incompleto dopo ${WAIT_MAX}s ($(conta_story)/$MIN_STORIES notizie): analisi NON eseguita. Controlla il generatore del brief, poi rilancia: run_daily_analysis.sh $TODAY"
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  exit 1
fi

# --- I dati di mercato sono pronti? (R07) ----------------------------------
# `WatchPaths` sorveglia la cartella dei briefing: il brief delle 07:30 fa scattare
# l'analisi PRIMA dell'aggiornamento prezzi delle 08:00. Un'attesa secca qui
# scadrebbe alle 07:41 — WAIT_MAX è 600s — e suonerebbe l'allarme ogni mattina su
# un ritardo che non è un guasto. Quindi due regimi separati da un'ora di soglia:
# prima si esce in silenzio e ci pensa il run di calendario delle 08:15; dopo, il
# ritardo è un guasto vero e si urla.
#
# Non c'è nessun flag per scavalcare il controllo: se la fonte prezzi si rompe si
# ripara il dato (`update_market_data.py` a mano), non si aggira la guardia.
# Decisione esplicita di Riccardo nel piano del Run 4a.
if [[ "$FASE" == "dati_pronti" ]]; then
  if [[ "$(date +%H:%M)" < "$DATI_PRONTI_ENTRO" ]]; then
    log "ATTESA: prezzi non ancora aggiornati e sono le $(date +%H:%M) (soglia $DATI_PRONTI_ENTRO). Esco: ci pensa il run di calendario."
    exit 0
  fi
  log "PARZIALE: prezzi non pronti oltre le $DATI_PRONTI_ENTRO. Attendo (max ${WAIT_MAX}s)."
  waited=0
  while (( waited < WAIT_MAX )); do
    sleep "$WAIT_STEP"
    waited=$(( waited + WAIT_STEP ))
    FASE=$(fase)
    [[ "$FASE" != "dati_pronti" ]] && { log "OK: prezzi pronti dopo ${waited}s."; break; }
  done
fi
if [[ "$FASE" == "dati_pronti" ]]; then
  MSG="prezzi di $TODAY non aggiornati: analisi NON eseguita. Dettaglio: stato_giornata.py --date $TODAY. Ripara i dati (update_market_data.py), poi rilancia: run_daily_analysis.sh $TODAY"
  log "ERROR: $MSG"
  "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" >> "$LOG" 2>&1
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  exit 1
fi

# Tutti i cancelli in ingresso sono passati: briefing completo, prezzi aggiornati.
# ⚠ Riga a livello BASE, fuori da ogni `if`: `tests/test_briefing_race.sh` tronca
# qui lo script per provare i cancelli senza eseguire il resto.
log "PRONTO: briefing $TODAY completo e prezzi aggiornati."

# --- Serve l'agente, o basta riparare la coda? (R07) -----------------------
# Triage e schede li scrive Claude e costano; render e consegna no. Prima si usciva
# alla prima riga di questo script davanti a un indice compilato, quindi un render o
# un invio falliti — ridotti a WARN più sotto — non venivano MAI riparati dai
# ritentativi delle 09:15 e 10:15. Ora si riprende dalla fase ferma, e solo quella.
SERVE_AGENTE=0
[[ "$FASE" == "triage_completato" || "$FASE" == "schede_validate" ]] && SERVE_AGENTE=1
INCOMPLETA=0

# --- Ripresa di un run interrotto ------------------------------------------
# Arrivati qui l'analisi di oggi o non esiste o è monca. Le schede ancora valide
# restano al loro posto; i residui non si sovrascrivono e non si cancellano, si
# spostano in un `_interrotto_<ora>/`, così il giorno riparte pulito e il parziale
# resta consultabile. Il prefisso `_` non è estetico — `render_report.py` e
# `analogues.py` fanno glob NON ricorsivo su `news_*.md`, quindi una scheda lasciata
# lì finirebbe due volte nel report e nella libreria episodi.
#
# ⚠ Tutto questo SOLO se l'agente dovrà riscrivere qualcosa: una giornata ferma su
# render o consegna ha le schede a posto, e archiviarle per rispedire un file su
# Telegram sarebbe un danno — capiterebbe su ogni giornata senza impronta registrata.
#
# ⚠ Sta DOPO il lock di proposito: un trigger sovrapposto a un run in corso vedrebbe
# anche lui un'analisi incompleta — quella che l'agente sta scrivendo in quel momento —
# e senza lock gli sposterebbe i file da sotto i piedi.
if (( SERVE_AGENTE )); then

# ⚠ Si rilegge lo stato: la lettura in testa allo script può essere avvenuta mentre
# il briefing era ancora a metà scrittura, e l'impronta di un file a metà non è
# quella del file finito — tutte le schede risulterebbero non riusabili proprio nel
# caso che il riuso deve coprire. Qui il briefing è completo e i prezzi ci sono.
leggi_stato

if (( RICONOSCIUTO )); then
  # Si tengono le schede valide e `_index.md`, che porta le decisioni di triage già
  # prese; si archivia il resto. L'11/09 il ritentativo buttava via anche le 6 schede
  # su 20 già prodotte e pagate: qui riparte dalle righe ancora ⏳.
  TIENI=("$DAILY/$TODAY/_index.md" ${RIUSABILI[@]/#/$DAILY/$TODAY/})
else
  TIENI=()
  (( REGISTRATO )) && log "INPUT CAMBIATO: il briefing di $TODAY non è quello registrato. Nessun riuso, rifaccio da capo."
fi

RESIDUI=()
for f in "$DAILY/$TODAY"/_index.md(N) "$DAILY/$TODAY"/news_*.md(N); do
  (( ${TIENI[(I)$f]} )) || RESIDUI+=("$f")
done
if (( ${#RESIDUI} )); then
  ARCH="$DAILY/$TODAY/_interrotto_$(date +%H%M%S)"
  mkdir -p "$ARCH" && mv "${RESIDUI[@]}" "$ARCH"/ \
    && log "RIPRESA: analisi di $TODAY interrotta a metà. ${#RESIDUI} file in ${ARCH:t}/, ${#RIUSABILI} schede riusate." \
    || log "WARN: analisi di $TODAY incompleta ma archiviazione del parziale fallita."
fi

# L'identità dell'input si registra DOPO aver deciso cosa tenere: registrarla prima
# cancellerebbe l'impronta con cui si confrontano le schede già in cartella.
"$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --registra-input >> "$LOG" 2>&1 \
  || log "WARN: impronta del briefing non registrata (niente riuso al prossimo tentativo)."

fi   # fine della ripresa

# ⚠ Riga a livello BASE agganciata da `tests/test_index_incompleto.sh`, che tronca
# QUI per provare idempotenza, ripresa e archiviazione del parziale: deve restare
# dopo il blocco di ripresa qui sopra e fuori da ogni `if`.
log "START: avvio lavoro su $TODAY (prima fase incompleta: $FASE)."

if (( SERVE_AGENTE )); then   # ⬇⬇ da qui a "fine del tratto con l'agente" ⬇⬇

# --- Salute DB: ricostruisci se incompleto ---------------------------------
DBCHECK=$("$PY" - <<'PY'
import sqlite3, os
p = os.path.expanduser('~/Claude/mercati_finanza/market_data/market_data.db')
try:
    c = sqlite3.connect(p)
    t = c.execute("SELECT COUNT(DISTINCT ticker) FROM prices").fetchone()[0]
    print(t)
except Exception:
    print(0)
PY
)
if [[ "${DBCHECK:-0}" -lt 44 ]]; then
  log "DB incompleto (ticker=$DBCHECK<44). Ricostruisco (bootstrap + spread daily)."
  "$PY" "$PIPE/bootstrap_market_data.py" >> "$LOG" 2>&1
  "$PY" "$PIPE/fetch_daily_spread.py"     >> "$LOG" 2>&1 || \
    "$PY" "$PIPE/fetch_fred_data.py"      >> "$LOG" 2>&1
else
  log "DB ok (ticker=$DBCHECK)."
fi

# Il conteggio dei ticker qui sopra dice solo che i ticker ci sono: una serie
# ferma da tre settimane e una riga senza prezzo passano lo stesso. --check
# guarda freschezza, buchi e barre rimaste provvisorie. Non scarica nulla e non
# blocca l'analisi: segnala, la decisione resta a mano.
if ! "$PY" "$PIPE/update_market_data.py" --check >> "$LOG" 2>&1; then
  log "WARN: serie prezzi con anomalie (freschezza/copertura). Dettaglio nel log."
fi

# --- Backstop indicizzazione KB (Variante A) -------------------------------
# I WatchPaths su knowledge_base/ gestiscono il caso "nuova sottocartella", ma
# non sempre l'aggiunta di un file dentro una cartella già esistente. Qui
# garantiamo che ogni studio non indicizzato lo sia prima del match del giorno.
# index_studies.sh è idempotente: no-op se non c'è nulla da indicizzare.
log "Backstop: controllo studi KB non indicizzati."
/bin/zsh "$PIPE/index_studies.sh" >> "$LOG" 2>&1

# Rinfresca la libreria di episodi (Opzione B): include le schede prodotte finora,
# così l'event study di oggi può pescare un pool ampio di analoghi invece di 5 a mano.
log "Refresh libreria episodi (analogues)."
"$PY" "$PIPE/analogues.py" build >> "$LOG" 2>&1

# --- Prompt per l'agente ---------------------------------------------------
# Su una ripresa il prompt dice cosa c'è già e da dove ripartire, invece di far
# rifare il triage da zero: l'11/09 il ritentativo ripagava anche le 6 schede su 20
# già prodotte. ⚠ Il passo 1 va saltato: `digest` senza --force si rifiuta di
# sovrascrivere un _index.md esistente, e CON --force cancellerebbe le decisioni di
# triage già prese.
# La condizione è "l'indice è sopravvissuto all'archiviazione", non "ci sono schede
# da riusare": un indice tenuto senza nemmeno una scheda valida è comunque una
# ripresa, e mandare l'agente a rifare `digest` lo farebbe sbattere contro il
# rifiuto di sovrascrivere.
RIPRESA_NOTA=""
if [[ -f "$INDEX" ]]; then
  RIPRESA_NOTA="
⚠ RIPRESA DI UN RUN INTERROTTO. $DAILY/$TODAY/_index.md esiste GIÀ e porta le
decisioni di triage prese finora. NON rigenerare il digest (salta il passo 1):
lo sovrascriverebbe e perderesti quelle decisioni. Riparti dalle sole righe ancora
⏳ della tabella, poi ricompila la Sintesi di sessione."
  (( ${#RIUSABILI} )) && RIPRESA_NOTA="$RIPRESA_NOTA
Queste schede sono già complete e VALIDE, non riscriverle: ${RIUSABILI}."
  RIPRESA_NOTA="$RIPRESA_NOTA
"
fi

read -r -d '' PROMPT <<EOF
Processa il morning briefing di oggi ($TODAY) seguendo ESATTAMENTE il runbook
$PIPE/PHASE5_RUNBOOK.md.
$RIPRESA_NOTA
Passi:
1) Genera il digest di triage: pipeline_tools.py digest --date $TODAY
2) Tria tutte le $(conta_story) notizie del briefing con scope "subset triato": scheda completa SOLO per
   notizie che mappano su uno degli asset dell'universo corrente in DB
   (verifica in category_asset_map.yaml, NON a memoria — leggilo UNA volta sola
   qui) e hanno un analogo storico plausibile;
   consolida notizie sullo stesso tema in un'unica scheda; scarta il resto con
   una riga di motivazione. Compila la tabella di _index.md.
3) Per ogni notizia tenuta esegui il flusso completo (assets, match, new-card).
   Per gli episodi analoghi usa la LIBRERIA (Opzione B): analogues.py find --theme
   <theme> --subtheme <tok> --direction <pos|neg|neutral> --direction-reference <ticker> --before <data notizia> →
   usa quel pool per --events di event_study.py. Verso indica pressione sul prezzo
   del ticker (non evento buono/cattivo né rendimento ex post). Compila nella scheda
   direction_reference come da template. Legacy e conflitti sono esclusi: se N è
   piccolo integra a mano, non forzare il segno. Passa SEMPRE --direction e --direction-reference e, sui temi
   larghi (geopolitical, commodity_energy), anche --subtheme (senza filtri il pool
   diluisce il segnale). La libreria applica già un tetto di recency (30 più recenti).
   Puoi potare i non pertinenti; integra a mano solo se il pool è piccolo. Poi compila
   via Edit tutte le sezioni qualitative. Se min(N)<10 la scheda riporta "INDICATIVE ONLY".
   PRIMA di scrivere la lettura direzionale leggi la scorecard più recente in
   $DAILY/_scorecard/ sezione "5-bis" (per-asset): hit-rate e IC sono metriche
   diverse (possono divergere) e nella tabella NON c'è più un giudizio automatico —
   leggi i due numeri dell'asset toccato dalla scheda e giudica tu; se appaiono
   deboli o incoerenti fra loro riporta l'event study ma dichiara esplicitamente
   che il segno storico è inaffidabile, invece di trarne una direzione attesa.
   Rileggi i numeri lì, non a memoria.
4) Compila la "Sintesi di sessione" in _index.md.

ECONOMIA DEL RUN (vincolante, sezione omonima del runbook): il costo cresce col
QUADRATO dei turni. Quindi: raccogli TUTTO prima di scrivere (pool potato, event
study, match KB, sezione 5-bis della scorecard) e scrivi ogni file in UN SOLO
passaggio; per le correzioni usa Edit chirurgico, mai un heredoc che rigenera il
corpo; non rileggere ciò che hai appena scritto; non lanciare --help (i flag sono
nel runbook, sezione "Riferimento comandi"). Questo non deve accorciare né
impoverire le schede: stesso contenuto, meno giri.

Output finale in chat: riepilogo con quante notizie tenute/scartate e i temi
delle schede prodotte. Lavora in $DAILY/$TODAY/.
EOF

log "Lancio Claude Code headless (model=$MODEL, tetto ${RUN_MAX}s)."
cd "$NEWSDIR"
# --output-format json: oltre al testo finale restituisce turni, token e costo.
# Senza questo il consumo del run non è misurabile (diagnosi del 2026-08-21: si
# poteva ricostruire solo scavando nei transcript di ~/.claude/projects/).
RAW="$LOGDIR/.raw_${TODAY}.json"
SCADUTO="$LOGDIR/.timeout_${TODAY}"
/bin/rm -f "$SCADUTO"

# ⚠ Watchdog (guasto del 2026-08-05). Quel giorno `claude -p` è rimasto appeso
# 410,9 minuti: il report è uscito alle 14:36 invece che alle 08:05, il lock è restato
# occupato per tutte e sette le ore — ogni ri-trigger a log come SKIP — e non è partito
# un solo allarme. Una chiamata sincrona senza tetto non ha modo di distinguere
# "sta lavorando" da "non tornerà mai": è il terzo guasto muto della stessa famiglia.
#
# Il guardiano NON dorme in un colpo solo. Controlla ogni secondo se Claude è ancora
# vivo e si spegne da sé appena finisce: un singolo `sleep $RUN_MAX` lascerebbe un
# processo addormentato per un'ora dopo OGNI run riuscito.
# ⚠ Uccide il processo figlio, non tutto il suo albero: in uno script i job non hanno
# un process group proprio, quindi un kill di gruppo porterebbe via anche noi.
"$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions \
  --output-format json </dev/null > "$RAW" 2>>"$LOG" &
PID_HEADLESS=$!
( trascorso=0
  while (( trascorso < RUN_MAX )); do
    sleep 1; trascorso=$(( trascorso + 1 ))
    kill -0 "$PID_HEADLESS" 2>/dev/null || exit 0
  done
  print -r -- "$RUN_MAX" > "$SCADUTO"
  kill -TERM "$PID_HEADLESS" 2>/dev/null
  sleep "$RUN_KILL_GRACE"
  kill -KILL "$PID_HEADLESS" 2>/dev/null ) &
PID_GUARDIANO=$!
wait "$PID_HEADLESS"
RC=$?
kill "$PID_GUARDIANO" 2>/dev/null
PID_GUARDIANO=""; PID_HEADLESS=""
if [[ -f "$SCADUTO" ]]; then
  log "TIMEOUT: Claude non è tornato entro ${RUN_MAX}s, processo ucciso."
  /bin/rm -f "$SCADUTO"
fi
log "Claude exit code $RC."

# Estrae il testo finale (nel log, come prima) e accoda una riga al CSV dei consumi.
"$PY" "$PIPE/record_claude_usage.py" "$RAW" "$LOG" "$LOGDIR/usage.csv" "$TODAY" \
  || log "WARN: parsing usage fallito."
rm -f "$RAW"

# --- Allarme su fallimento del run headless -------------------------------
# Tre esiti, non due. Il segnale di successo non è che _index.md esista, ma che le
# fasi di triage e schede siano davvero chiuse (v. stato_giornata.py):
#   assente   → fallimento pieno (tipico: 401 login scaduto) → ERROR + notifica + stop
#   monco     → run interrotto a metà (limite di sessione, connessione caduta): le
#               schede già prodotte si tengono e si spediscono, ma il giorno è marcato
#               INCOMPLETO ad alta voce e lo script esce ≠0. Era il buco dell'11/09.
#   compilato → successo, anche con exit ≠0 (errore finale non fatale a lavoro già
#               scritto: successo il 2026-07-10) → WARN e si prosegue.
if [[ ! -f "$INDEX" ]]; then
  MSG="run $TODAY FALLITO (exit $RC, _index.md assente)."
  if grep -q "TIMEOUT:" "$LOG" 2>/dev/null; then
    MSG="Claude appeso oltre ${RUN_MAX}s e ucciso dal watchdog senza aver scritto nulla: run $TODAY non prodotto. Rilancia: run_daily_analysis.sh $TODAY"
  elif grep -qi "Invalid authentication\|401\|Not logged in\|Please run /login" "$LOG" 2>/dev/null; then
    MSG="login Claude scaduto: esegui 'claude /login'. Run $TODAY non prodotto."
  elif grep -qi "session limit\|usage limit" "$LOG" 2>/dev/null; then
    MSG="limite di sessione Claude: run $TODAY non prodotto. Rilancia dopo il reset: run_daily_analysis.sh $TODAY"
  elif grep -qi "529\|Overloaded\|rate.limit\|500 Internal\|503" "$LOG" 2>/dev/null; then
    MSG="API sovraccarica (529/5xx): run $TODAY non prodotto. Rilancia: run_daily_analysis.sh $TODAY"
  fi
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  # Anche senza analisi, il briefing grezzo va spedito: il 2026-08-24 un 529 ha
  # fatto uscire lo script qui, e il risultato è stato silenzio totale su Telegram
  # (nessun brief, nessuna analisi) — indistinguibile da "il job non è partito".
  log "Invio su Telegram del solo briefing (analisi assente)."
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" >> "$LOG" 2>&1 || log "WARN: invio Telegram fallito."
  exit 1
else
  FASE=$(fase)
fi
if [[ "$FASE" == "triage_completato" || "$FASE" == "schede_validate" ]]; then
  INCOMPLETA=1
  PARZIALI=("$DAILY/$TODAY"/news_*.md(N))
  PENDENTI=$(grep -c '⏳' "$INDEX" 2>/dev/null)
  MSG="analisi $TODAY INCOMPLETA (exit $RC): ${#PARZIALI} schede prodotte, $PENDENTI notizie non triate. Rilancia: run_daily_analysis.sh $TODAY"
  # L'ora di reset la scrive Claude stesso nell'ultima riga utile del log
  # ("You've hit your session limit · resets 12:40pm (Europe/Rome)"): riportarla
  # evita il rilancio a vuoto prima che il limite si sia azzerato.
  if grep -q "TIMEOUT:" "$LOG" 2>/dev/null; then
    MSG="watchdog: Claude appeso oltre ${RUN_MAX}s, ucciso a metà run. Analisi $TODAY INCOMPLETA (${#PARZIALI} schede prodotte, $PENDENTI notizie non triate). Rilancia: run_daily_analysis.sh $TODAY"
  elif grep -qi "session limit\|usage limit" "$LOG" 2>/dev/null; then
    RESET=$(grep -o 'resets [0-9:apm]*' "$LOG" 2>/dev/null | tail -1)
    MSG="limite di sessione Claude a metà run: analisi $TODAY INCOMPLETA (${#PARZIALI} schede, $PENDENTI notizie non triate). Rilancia${RESET:+ dopo le ${RESET#resets }}: run_daily_analysis.sh $TODAY"
  fi
  log "ERROR: $MSG"
  "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" >> "$LOG" 2>&1
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
elif [[ $RC -ne 0 ]]; then
  log "WARN: Claude exit $RC ma triage e schede sono chiusi → procedo comunque con render + invio."
fi

fi   # ⬆⬆ fine del tratto con l'agente (SERVE_AGENTE) ⬆⬆
if (( ! SERVE_AGENTE )); then
  log "RIPARAZIONE: giornata $TODAY ferma su $FASE. Triage e schede sono a posto: riprendo da lì senza richiamare l'agente."
fi

# Render HTML del report (apribile con doppio clic nel browser).
if [[ -f "$DAILY/$TODAY/_index.md" ]]; then
  "$PY" "$PIPE/render_report.py" --date "$TODAY" >> "$LOG" 2>&1 \
    && log "Report HTML generato: $DAILY/$TODAY/report.html" \
    || log "WARN: render_report.py fallito."
else
  log "WARN: _index.md assente, salto il render HTML."
fi

# --- Invio su Telegram (lettura push da telefono) --------------------------
# Canale primario su telefono (indipendente da iCloud): manda brief + analisi
# in chat col bot. Credenziali in .env. Non blocca il run se fallisce.
#
# Su run monco passa `--parziale`, che cambia la didascalia dell'analisi. Serve
# perché il guasto si legge dal telefono, dove la notifica desktop non arriva: senza,
# un'analisi a metà atterrerebbe con la stessa faccia di una completa — che è
# esattamente come l'11/09 è passata inosservata.
log "Invio su Telegram."
if (( INCOMPLETA )); then
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" --parziale >> "$LOG" 2>&1
else
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" >> "$LOG" 2>&1
fi
INVIO=$?

# La ricevuta è l'unico pezzo di stato che il disco non sa da solo: senza, un invio
# fallito era indistinguibile da uno riuscito e nessun ritentativo lo riprendeva.
# `send_telegram.sh` esce 0 solo se TUTTI gli artefatti attesi sono partiti e
# Telegram ha risposto "ok":true (Run 1 della revisione).
if (( INVIO == 0 )); then
  PARZ=()
  (( INCOMPLETA )) && PARZ=(--parziale)
  "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --registra-consegna ok \
    "${PARZ[@]}" >> "$LOG" 2>&1
else
  log "WARN: invio Telegram fallito."
  "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --registra-consegna fallita >> "$LOG" 2>&1
fi

# Un run monco non è "DONE": esce ≠0 così launchd e chi legge il log lo distinguono
# da un giorno andato a buon fine. Ora il verdetto lo dà lo stato della giornata,
# non la sola variabile del ramo dell'agente: anche un render o un invio falliti
# lasciano la giornata incompleta, ed è il ritentativo successivo a riprenderla.
FASE=$(fase)
if [[ "$FASE" != "completa" ]]; then
  log "FINE: run $TODAY INCOMPLETO, fermo su $FASE. Il prossimo tentativo riparte da lì."
  exit 1
fi

log "DONE."
exit 0
