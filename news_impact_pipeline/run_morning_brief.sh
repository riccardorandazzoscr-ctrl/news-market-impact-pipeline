#!/bin/zsh
# run_morning_brief.sh — produce il morning briefing HTML del giorno (07:30).
#
# Fino al 2026-09-15 questo passo NON aveva uno script: era una routine cloud
# (Claude), poi un'attività locale dell'app ChatGPT. Entrambe dipendevano da
# un'app aperta. Qui è un job launchd come gli altri cinque: al Mac basta
# essere sveglio.
#
# Il prompt NON è duplicato qui: si estrae dal blocco `=== PROMPT START/END ===`
# di news_research_prompt.md, che resta la copia canonica e versionata.
#
# È idempotente e auto-protetto, per le stesse ragioni del run giornaliero:
#   - se il briefing di oggi esiste ed è completo → esce (nessun doppione)
#   - lock per evitare run concorrenti (calendario + rilancio a mano)
#   - watchdog: un run appeso viene ucciso invece di occupare il lock per ore
#   - se il file non esce, lo dice ad alta voce (notifica) invece di tacere

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# --- Configurazione --------------------------------------------------------
MODEL="claude-opus-5"   # ricerca web + sintesi: stesso modello del run giornaliero

# Tetto di durata. Il brief è una ricerca web, non un'analisi su molte schede:
# i 138 briefing in archivio sono usciti fra le 07:45 e le 07:51 partendo dalle
# 07:30, cioè 15-21 minuti. 1800s sta comodamente sopra, e resta ben dentro la
# finestra prima dell'analisi delle 08:15.
RUN_MAX=${RUN_MAX:-1800}
RUN_KILL_GRACE=${RUN_KILL_GRACE:-20}

PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
BRIEF_DIR="$PROJECT/morning brief"
LOGDIR="$PIPE/logs"
PROMPT_FILE="$PIPE/news_research_prompt.md"
# Sovrascrivibile perché la suite in tests/ possa metterci un finto `claude`.
# launchd non la imposta.
CLAUDE=${CLAUDE:-/opt/homebrew/bin/claude}

mkdir -p "$LOGDIR" "$BRIEF_DIR"
# Come run_daily_analysis.sh: si può passare una data ISO per rigenerare a mano
# un giorno saltato. L'idempotenza vale comunque.
TODAY=${1:-$(date +%Y-%m-%d)}
BRIEF="$BRIEF_DIR/${TODAY}-morning-briefing.html"
LOG="$LOGDIR/brief-${TODAY}.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Stessa definizione di "briefing finito" usata da run_daily_analysis.sh:
# il tag di chiusura è il segno della pubblicazione atomica, il conteggio
# distingue un file valido da uno vuoto o scritto a metà.
brief_completo() {
  [[ -f "$BRIEF" ]] || return 1
  grep -q '</body>' "$BRIEF" 2>/dev/null || return 1
  local n
  n=$(grep -o 'class="story"' "$BRIEF" 2>/dev/null | wc -l | tr -d ' ')
  (( n >= 1 ))
}

if brief_completo; then
  log "SKIP: briefing $TODAY già presente e completo."
  exit 0
fi

LOCK="$LOGDIR/.lock_brief"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP: altro run del briefing in corso (lock presente)."
  exit 0
fi
PID_HEADLESS=""; PID_GUARDIANO=""
# Il trap ripulisce anche i figli: un kill dello script non deve lasciare in giro
# né il lock né un processo headless orfano.
trap '[[ -n "$PID_GUARDIANO" ]] && kill "$PID_GUARDIANO" 2>/dev/null
      [[ -n "$PID_HEADLESS" ]] && kill "$PID_HEADLESS" 2>/dev/null
      rmdir "$LOCK" 2>/dev/null' EXIT INT TERM

log "START briefing $TODAY."

if [[ ! -f "$PROMPT_FILE" ]]; then
  log "ERROR: prompt non trovato ($PROMPT_FILE)."
  exit 1
fi

# Solo il blocco fra i marcatori: le note di changelog sopra non fanno parte
# del prompt e ne sporcherebbero il senso (sono in italiano, il brief è in inglese).
PROMPT=$(awk '/^=== PROMPT START ===$/{p=1;next} /^=== PROMPT END ===$/{p=0} p' "$PROMPT_FILE")
if [[ -z "$PROMPT" ]]; then
  log "ERROR: blocco === PROMPT START/END === non trovato in $PROMPT_FILE."
  exit 1
fi
# La data la fissa lo script, non il modello: `date` nel prompt evita che un run
# di backfill scriva il file di oggi al posto di quello del giorno richiesto.
PROMPT="Today's date is $TODAY (Europe/Rome). Use exactly this date for the briefing
title and for the output filename.

$PROMPT"

log "Lancio Claude Code headless (model=$MODEL, tetto ${RUN_MAX}s)."
cd "$NEWSDIR"
RAW="$LOGDIR/.raw_brief_${TODAY}.json"
SCADUTO="$LOGDIR/.timeout_brief_${TODAY}"
/bin/rm -f "$SCADUTO"

# Stesso watchdog del run giornaliero (guasto del 2026-08-05): controlla ogni
# secondo e si spegne da sé appena il figlio finisce, invece di dormire in un
# colpo solo e restare appeso per mezz'ora dopo ogni run riuscito.
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

"$PY" "$PIPE/record_claude_usage.py" "$RAW" "$LOG" "$LOGDIR/usage_brief.csv" "$TODAY" \
  || log "WARN: parsing usage fallito."
rm -f "$RAW"

# --- Esito -----------------------------------------------------------------
# Il segnale di successo NON è l'exit code ma il file pubblicato: il prompt
# prevede esplicitamente il caso "nessuna notizia nuova verificabile → non
# pubblicare", che esce 0 senza file. Va distinto da un guasto, ma nessuno dei
# due deve passare in silenzio: senza brief, alle 08:15 non c'è analisi.
if ! brief_completo; then
  MSG="briefing $TODAY NON prodotto (exit $RC)."
  if grep -q "TIMEOUT:" "$LOG" 2>/dev/null; then
    MSG="Claude appeso oltre ${RUN_MAX}s e ucciso dal watchdog: briefing $TODAY non prodotto. Rilancia: run_morning_brief.sh $TODAY"
  elif grep -qi "Invalid authentication\|401\|Not logged in\|Please run /login" "$LOG" 2>/dev/null; then
    MSG="login Claude scaduto: esegui 'claude /login'. Briefing $TODAY non prodotto."
  elif grep -qi "session limit\|usage limit" "$LOG" 2>/dev/null; then
    MSG="limite di sessione Claude: briefing $TODAY non prodotto. Rilancia dopo il reset: run_morning_brief.sh $TODAY"
  elif grep -qi "529\|Overloaded\|rate.limit\|500 Internal\|503" "$LOG" 2>/dev/null; then
    MSG="API sovraccarica (529/5xx): briefing $TODAY non prodotto. Rilancia: run_morning_brief.sh $TODAY"
  fi
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"Morning Briefing\" sound name \"Basso\"" 2>/dev/null
  exit 1
fi

STORIE=$(grep -o 'class="story"' "$BRIEF" | wc -l | tr -d ' ')
log "DONE briefing $TODAY pubblicato ($STORIE notizie): $BRIEF"
# Non serve avvisare l'analisi: il job daily ha WatchPaths sulla cartella dei
# briefing e parte da sé appena il file atterra.
exit 0
