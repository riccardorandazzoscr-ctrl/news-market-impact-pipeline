#!/bin/zsh
# Test del WATCHDOG e del LOCK di run_daily_analysis.sh
# (guasto del 05/08/2026: `claude -p` appeso 410,9 minuti — 6h50m — con il report
# uscito alle 14:36 invece che alle 08:05, nessun allarme, e il lock tenuto per
# tutte quelle ore, così ogni ri-trigger ha loggato SKIP).
#
#   ./tests/test_watchdog.sh
#
# COME FUNZIONA, e cosa NON copre.
# Qui gira lo script VERO — non una copia troncata come nelle altre due suite —
# dentro un $HOME finto: tutti i percorsi derivano da $HOME, quindi il run non
# esce mai dalla sandbox. L'unica sostituzione è `claude` stesso, un finto
# pilotabile da variabili d'ambiente ($CLAUDE è sovrascrivibile apposta).
# Sotto test ci sono i tempi e la terminazione, non il contenuto dell'analisi:
# venv, index_studies.sh, render_report.py e send_telegram.sh restano stub.
#
# ⚠ I casi di timeout e di interruzione fanno comparire DAVVERO una notifica sul
# desktop: `osascript` è chiamato per percorso assoluto e non si può sostituire.
# È il comportamento sotto test, non un effetto collaterale.
#
# ⚠ La suite dura ~40 secondi: i casi di attesa usano RUN_MAX di pochi secondi,
# ma restano attese reali — è l'unico modo di provare che il tetto scatti davvero.

set -u
PIPE="${0:A:h:h}"
SCRIPT="$PIPE/run_daily_analysis.sh"
PASS=0; FAIL=0

# ⚠ Guardia, non un test: se lo script non onorasse $CLAUDE, ogni caso qui sotto
# lancerebbe il binario VERO con --permission-mode bypassPermissions su una sandbox.
# Meglio non partire affatto che scoprirlo dai consumi.
if ! grep -q 'CLAUDE=${CLAUDE:-' "$SCRIPT"; then
  print -r -- "ABORT: run_daily_analysis.sh non permette di sostituire \$CLAUDE."
  print -r -- "       Senza quella sostituzione questa suite lancerebbe il claude vero."
  exit 1
fi

ok()  { print -r -- "  ✓ $1"; PASS=$((PASS+1)); }
ko()  { print -r -- "  ✗ $1"; print -r -- "      $2"; FAIL=$((FAIL+1)); }
check() { if eval "$1"; then ok "$2"; else ko "$2" "${3:-condizione non soddisfatta: $1}"; fi }

# ---------------------------------------------------------------- ambiente finto
setup() {
  SANDBOX=$(mktemp -d)
  export FAKE_HOME="$SANDBOX/home"
  BDIR="$FAKE_HOME/Claude/morning brief"
  DAILY="$FAKE_HOME/Claude/mercati_finanza/daily_analysis"
  FPIPE="$FAKE_HOME/Claude/mercati_finanza/news_impact_pipeline"
  mkdir -p "$BDIR" "$DAILY" "$FPIPE/logs" "$FPIPE/venv/bin"

  GIORNO="2026-08-05"                      # il giorno del guasto vero
  BRIEF="$BDIR/${GIORNO}-morning-briefing.html"
  LOG="$FPIPE/logs/${GIORNO}.log"
  GIORNODIR="$DAILY/$GIORNO"
  TELEGRAM="$FPIPE/logs/telegram.txt"
  LOCK="$FPIPE/logs/.lock"
  RAW="$FPIPE/logs/.raw_${GIORNO}.json"
  PIDFILE="$SANDBOX/claude.pid"

  # --- finto `claude -p`, pilotato da variabili d'ambiente ---
  # Scrive PRIMA il lavoro parziale e resta appeso DOPO: è l'ordine reale, e
  # serve a verificare che un run ucciso conservi le schede già prodotte.
  cat > "$SANDBOX/claude_finto" <<'FAKE'
#!/bin/zsh
print -r -- $$ > "$FAKE_PIDFILE"
D="$FAKE_DAILY/$FAKE_GIORNO"
mkdir -p "$D"
[[ -n "${FAKE_INDEX:-}" ]] && cp "$FAKE_INDEX" "$D/_index.md"
for n in $(seq 1 ${FAKE_SCHEDE:-0}); do print -r -- "# scheda finta $n" > "$D/news_0$n.md"; done
[[ -n "${FAKE_SLEEP:-}" ]] && sleep "$FAKE_SLEEP"
print -r -- '{"result":"finto","num_turns":3,"total_cost_usd":0.01,"duration_ms":1000,"usage":{}}'
exit ${FAKE_RC:-0}
FAKE

  # --- dipendenze finte (come nelle altre due suite) ---
  cat > "$FPIPE/venv/bin/python" <<'PYSTUB'
#!/bin/zsh
case "$*" in
  *render_report.py*)
    R="$HOME/Claude/mercati_finanza/daily_analysis/$3"
    mkdir -p "$R"; print -r -- "<html>report finto $3</html>" > "$R/report.html" ;;
  -) print 99 ;;          # controllo salute DB (heredoc su stdin)
  *) : ;;                 # analogues.py build, parsing usage & co.
esac
exit 0
PYSTUB
  cat > "$FPIPE/index_studies.sh" <<'IDX'
#!/bin/zsh
exit 0
IDX
  cat > "$FPIPE/send_telegram.sh" <<'TG'
#!/bin/zsh
print -r -- "TELEGRAM $*" >> "$HOME/Claude/mercati_finanza/news_impact_pipeline/logs/telegram.txt"
exit 0
TG
  chmod +x "$SANDBOX/claude_finto" "$FPIPE/venv/bin/python" \
           "$FPIPE/index_studies.sh" "$FPIPE/send_telegram.sh"

  scrivi_brief 20
}
teardown() {
  [[ -f "${PIDFILE:-}" ]] && kill -KILL "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
  [[ -n "${SANDBOX:-}" ]] && rm -rf "$SANDBOX"
  return 0
}

scrivi_brief() {
  { print -r -- "<html><head><title>Morning Briefing</title></head><body>"
    for i in $(seq 1 ${1:-20}); do
      print -r -- "<div class=\"story\"><h3>Notizia $i</h3></div>"
    done
    print -r -- "</body></html>"
  } > "$BRIEF"
}

scrivi_index() {   # gli stessi due stati usati dalla suite sull'analisi
  case "$1" in
    scheletro)
      { print -r -- "# Daily Analysis — $GIORNO"
        for i in $(seq 1 20); do print -r -- "| 0$i | fin | Notizia $i | ⏳ | | |"; done
        print -r -- "## Sintesi di sessione"
        print -r -- "_(nota dell'analista: temi dominanti. Da compilare dopo il triage.)_"
      } > "$SANDBOX/scheletro.md" ;;
    completo)
      { print -r -- "# Daily Analysis — $GIORNO"
        print -r -- "| 01 | fin | Notizia | ✅ | inflazione | news_01.md |"
        print -r -- "## Sintesi di sessione"
        print -r -- "Il tema dominante del giorno è stato l'inflazione."
      } > "$SANDBOX/completo.md" ;;
  esac
}

# Lancia lo script VERO con il finto claude. Restituisce il codice di uscita.
run_sut() {   # run_sut <run_max> [FAKE_SLEEP] [FAKE_INDEX] [FAKE_SCHEDE] [FAKE_RC]
  ( HOME="$FAKE_HOME" CLAUDE="$SANDBOX/claude_finto" \
    RUN_MAX="${1:-5}" RUN_KILL_GRACE=2 WAIT_MAX=1 WAIT_STEP=1 \
    FAKE_PIDFILE="$PIDFILE" FAKE_DAILY="$DAILY" FAKE_GIORNO="$GIORNO" \
    FAKE_SLEEP="${2:-}" FAKE_INDEX="${3:-}" FAKE_SCHEDE="${4:-0}" FAKE_RC="${5:-0}" \
    /bin/zsh "$SCRIPT" "$GIORNO" >/dev/null 2>&1 ); echo $?
}

vivo() { [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null }

print -r -- "=============================================================="
print -r -- "TEST — watchdog sul run appeso e lock a prova di kill"
print -r -- "=============================================================="

# ---------------------------------------------------------------- 0. sintassi
print -- "\n0. Sintassi e agganci che le altre suite danno per buoni"
setup
if zsh -n "$SCRIPT" 2>/dev/null; then ok "run_daily_analysis.sh: sintassi valida"
else ko "run_daily_analysis.sh: sintassi valida" "zsh -n fallisce"; fi
# test_index_incompleto.sh ritaglia il blocco della chiamata a Claude fra questi
# due marcatori: se il watchdog li duplicasse, quella suite taglierebbe a caso.
check "grep -c '^log \"Lancio Claude Code headless' '$SCRIPT' | grep -q '^1$'" \
      "resta UN solo marcatore di apertura (^log \"Lancio...)"
check "grep -c '^rm -f ' '$SCRIPT' | grep -q '^1$'" \
      "resta UN solo marcatore di chiusura (^rm -f)"
check "grep -q 'CLAUDE=\${CLAUDE:-' '$SCRIPT'" \
      "il binario claude è sovrascrivibile (serve a questa suite)"
check "grep -q 'RUN_MAX=\${RUN_MAX:-' '$SCRIPT'" "il tetto è sovrascrivibile da ambiente"
teardown

# ------------------------------------------------ 1. il guasto dell'05/08: hang
print -- "\n1. Claude si appende oltre il tetto → ucciso e dichiarato, non atteso"
setup
scrivi_index scheletro
INIZIO=$SECONDS
RC=$(run_sut 4 60 "$SANDBOX/scheletro.md" 3)
DURATA=$(( SECONDS - INIZIO ))
check "[[ $RC -ne 0 ]]" "esce con codice ≠0" "rc=$RC"
check "[[ $DURATA -lt 30 ]]" "si ferma al tetto invece di aspettare (${DURATA}s, finto sleep=60s)"
check "grep -q 'TIMEOUT' '$LOG'" "logga TIMEOUT"
check "grep -q 'ERROR' '$LOG'" "logga ERROR"
check "! vivo" "il processo claude è stato ucciso, non lasciato orfano"
check "! grep -q 'DONE' '$LOG'" "NON si dichiara completato"
teardown

# --------------------------------------- 2. il parziale di un run scaduto si tiene
print -- "\n2. Timeout con schede già prodotte → parziale tenuto, spedito e dichiarato"
setup
scrivi_index scheletro
RC=$(run_sut 4 60 "$SANDBOX/scheletro.md" 4)
check "grep -q 'INCOMPLETA' '$LOG'" "cade nel ramo del run monco che esisteva già"
check "grep -q '4 schede' '$LOG'" "conta le schede salvate"
check "[[ -f '$GIORNODIR/report.html' ]]" "il lavoro parziale viene renderizzato"
check "grep -q -- '--parziale' '$TELEGRAM'" "Telegram avvisa che è incompleto"
check "grep -q 'run_daily_analysis.sh $GIORNO' '$LOG'" "dice come rilanciare"
teardown

# ------------------------------------------------- 3. nessun falso allarme sotto il tetto
print -- "\n3. Run normale sotto il tetto → nessun falso allarme, niente residui"
setup
scrivi_index completo
RC=$(run_sut 30 "" "$SANDBOX/completo.md" 3)
check "[[ $RC -eq 0 ]]" "esce con 0" "rc=$RC"
check "grep -q 'DONE' '$LOG'" "logga DONE"
check "! grep -q 'TIMEOUT\|ERROR\|INTERROTTO' '$LOG'" "il watchdog non scatta"
check "[[ ! -e '$RAW' ]]" "il .raw temporaneo non resta indietro"
check "[[ ! -d '$LOCK' ]]" "il lock è rilasciato"
teardown

# ------------------------------------------- 4. terminazione esterna (il buco dell'11/09)
print -- "\n4. Segnale TERM durante il run → ERROR a log, non un buco silenzioso"
setup
scrivi_index scheletro
( HOME="$FAKE_HOME" CLAUDE="$SANDBOX/claude_finto" \
  RUN_MAX=60 RUN_KILL_GRACE=2 WAIT_MAX=1 WAIT_STEP=1 \
  FAKE_PIDFILE="$PIDFILE" FAKE_DAILY="$DAILY" FAKE_GIORNO="$GIORNO" \
  FAKE_SLEEP=60 FAKE_INDEX="$SANDBOX/scheletro.md" FAKE_SCHEDE=2 \
  /bin/zsh "$SCRIPT" "$GIORNO" >/dev/null 2>&1 ) &
SUT=$!
for _ in {1..40}; do vivo && break; sleep 0.25; done   # aspetta che claude sia partito
kill -TERM "$SUT" 2>/dev/null
wait "$SUT"; RC=$?
check "[[ $RC -ne 0 ]]" "esce con codice ≠0" "rc=$RC"
check "grep -q 'INTERROTTO' '$LOG'" "logga l'interruzione (prima non lasciava traccia)"
check "grep -q 'ERROR' '$LOG'" "la segna come ERROR"
check "! vivo" "si porta dietro il processo claude invece di lasciarlo orfano"
check "[[ ! -d '$LOCK' ]]" "rilascia comunque il lock"
check "[[ ! -e '$RAW' ]]" "non lascia il .raw indietro (era l'impronta dell'11/09)"
teardown

# ------------------------------------------------------------ 5. lock di un morto
print -- "\n5. Lock di un processo morto (kill -9, corrente staccata) → rilevato"
setup
sleep 0.1 & MORTO=$!; wait $MORTO 2>/dev/null   # un PID sicuramente non più vivo
mkdir -p "$LOCK"; print -r -- "$MORTO" > "$LOCK/pid"
scrivi_index completo
RC=$(run_sut 30 "" "$SANDBOX/completo.md" 2)
check "[[ $RC -eq 0 ]]" "il run parte invece di arrendersi" "rc=$RC"
check "grep -q 'STANTIO' '$LOG'" "dichiara il lock stantio"
check "grep -q 'START' '$LOG'" "prosegue con l'analisi"
check "! grep -q 'SKIP: altro run' '$LOG'" "NON si blocca per sempre come prima"
teardown

# -------------------------------------------------------- 6. lock di un vivo: SKIP
print -- "\n6. Lock di un processo VIVO → SKIP, esattamente come prima"
setup
sleep 30 & VIVO=$!
mkdir -p "$LOCK"; print -r -- "$VIVO" > "$LOCK/pid"
RC=$(run_sut 10 "" "" 0)
check "[[ $RC -eq 0 ]]" "esce con 0" "rc=$RC"
check "grep -q 'SKIP: altro run in corso' '$LOG'" "logga SKIP"
check "! grep -q 'START' '$LOG'" "non si mette a girare in parallelo"
check "[[ -d '$LOCK' ]]" "non ruba il lock a chi lo sta usando"
check "[[ \"\$(cat '$LOCK/pid')\" == '$VIVO' ]]" "il pid nel lock resta quello del vivo"
kill "$VIVO" 2>/dev/null; wait "$VIVO" 2>/dev/null
teardown

# ------------------------------------------------ 7. lock vecchio formato, senza pid
print -- "\n7. Lock del vecchio formato (nessun pid dentro) → trattato da stantio"
setup
mkdir -p "$LOCK"                                  # com'era prima di questa modifica
scrivi_index completo
RC=$(run_sut 30 "" "$SANDBOX/completo.md" 2)
check "grep -q 'STANTIO' '$LOG'" "lo riconosce e lo rileva"
check "grep -q 'DONE' '$LOG'" "il giorno arriva in fondo"
teardown

# ------------------------------- 8. l'incidente del 12/09: uccidere un PID non nostro
# L'app Claude Code esporta CLAUDE_PID nell'ambiente dei processi che lancia, col PID
# dell'APP. La prima versione del watchdog chiamava la sua variabile allo stesso modo e
# la leggeva senza averla mai assegnata: a ogni uscita anticipata la pulizia spediva
# SIGTERM a quel PID ereditato, cioè all'applicazione dell'utente (che moriva con 143).
# Qui una sentinella innocua prende il posto dell'app: deve sopravvivere in ogni caso.
print -- "\n8. PID omonimi nell'ambiente → la pulizia non tocca processi non suoi"
setup
scrivi_index completo
sleep 25 & SENTINELLA=$!
ostile() {   # lancia lo script con l'ambiente avvelenato, come fa l'app vera
  ( HOME="$FAKE_HOME" CLAUDE="$SANDBOX/claude_finto" \
    CLAUDE_PID="$SENTINELLA" PID_HEADLESS="$SENTINELLA" PID_GUARDIANO="$SENTINELLA" \
    RUN_MAX=30 RUN_KILL_GRACE=2 WAIT_MAX=1 WAIT_STEP=1 \
    FAKE_PIDFILE="$PIDFILE" FAKE_DAILY="$DAILY" FAKE_GIORNO="$GIORNO" \
    FAKE_INDEX="${1:-}" FAKE_SCHEDE=2 \
    /bin/zsh "$SCRIPT" "$GIORNO" >/dev/null 2>&1 ); echo $?
}
RC=$(ostile "$SANDBOX/completo.md")
check "kill -0 $SENTINELLA 2>/dev/null" \
      "run completo: la sentinella è viva (era il SIGTERM all'app)" "sentinella uccisa"
check "[[ $RC -eq 0 ]]" "il run resta un successo" "rc=$RC"

# Il caso che faceva davvero il danno: si esce PRIMA di aver lanciato Claude, quindi
# la variabile non è mai stata assegnata da noi. Un briefing monco esce proprio lì.
scrivi_brief 5
rm -rf "$GIORNODIR"
RC=$(ostile "")
check "kill -0 $SENTINELLA 2>/dev/null" \
      "uscita anticipata (briefing monco): la sentinella è ancora viva" "sentinella uccisa"
check "[[ $RC -ne 0 ]]" "l'uscita anticipata resta un errore" "rc=$RC"
kill "$SENTINELLA" 2>/dev/null; wait "$SENTINELLA" 2>/dev/null
teardown

# --------------------------------- 9. nessuna variabile letta prima di essere scritta
print -- "\n9. Nessun kill su variabile non inizializzata (la classe del guasto)"
setup
check "grep -q '^PID_HEADLESS=\"\"' '$SCRIPT'" "PID_HEADLESS è azzerata esplicitamente"
check "grep -q '^PID_GUARDIANO=\"\"' '$SCRIPT'" "PID_GUARDIANO è azzerata esplicitamente"
# L'azzeramento deve stare PRIMA dei trap, o il trap può scattare su un valore ereditato.
AZZ=$(grep -n '^PID_HEADLESS=""' "$SCRIPT" | cut -d: -f1)
TRAP=$(grep -n "^trap 'pulisci' EXIT" "$SCRIPT" | cut -d: -f1)
check "[[ $AZZ -lt $TRAP ]]" "l'azzeramento precede l'installazione dei trap" "azz=$AZZ trap=$TRAP"
# Solo il codice eseguibile: il commento che racconta l'incidente cita la riga colpevole.
check "! grep -v '^[[:space:]]*#' '$SCRIPT' | grep -q 'kill \"\$CLAUDE_PID\"'" \
      "nessun kill su CLAUDE_PID nel codice (nome esportato dall'app)"
teardown

print -- "\n=============================================================="
print -r -- "PASSATI: $PASS   ·   FALLITI: $FAIL"
print -r -- "=============================================================="
exit $(( FAIL > 0 ? 1 : 0 ))
