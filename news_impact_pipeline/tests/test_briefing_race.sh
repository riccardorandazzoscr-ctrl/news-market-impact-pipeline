#!/bin/zsh
# Test del guardiano sull'integrità del briefing in run_daily_analysis.sh
# (guasto del 2026-09-07: run partito su un briefing scritto a metà).
#
#   ./tests/test_briefing_race.sh
#
# COME FUNZIONA, e cosa NON copre.
# Lo script sotto test viene copiato in un $HOME finto e TRONCATO subito dopo la
# riga `log "START..."`: tutto ciò che verifichiamo — controllo di esistenza,
# lock, attesa del completamento, fallimento rumoroso — sta sopra quel punto,
# mentre sotto ci sono il controllo del DB e il lancio di Claude headless, che
# costano soldi e riscriverebbero l'analisi del giorno. La parte troncata NON è
# quindi coperta da questi test; la sua integrità sintattica è verificata a parte
# con `zsh -n` sul file INTERO (caso 0).
# Le costanti di attesa vengono ridotte via ambiente per non stare fermi 10 minuti.

set -u
PIPE="${0:A:h:h}"
SCRIPT="$PIPE/run_daily_analysis.sh"
BRIEF_REALI="$HOME/Claude/morning brief"
PASS=0; FAIL=0
MIN_STORIES_ATTESA=20   # invariante attesa, usata solo nei messaggi

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
  mkdir -p "$BDIR" "$DAILY" "$FPIPE/logs"
  # copia troncata dopo lo START: vedi nota in testa
  awk '/^log "START/ { print; print "exit 0"; exit } { print }' \
      "$SCRIPT" > "$FPIPE/run.sh"
  chmod +x "$FPIPE/run.sh"
  GIORNO="2026-09-07"
  BRIEF="$BDIR/${GIORNO}-morning-briefing.html"
  LOG="$FPIPE/logs/${GIORNO}.log"
}
teardown() { [[ -n "${SANDBOX:-}" ]] && rm -rf "$SANDBOX"; }

# esegue lo script nella sandbox; le attese sono compresse
run_sut() {
  ( HOME="$FAKE_HOME" MIN_STORIES=20 WAIT_MAX="${1:-2}" WAIT_STEP="${2:-1}" \
    /bin/zsh "$FPIPE/run.sh" "$GIORNO" >/dev/null 2>&1 )
  echo $?
}

# briefing finto con N notizie; $2=chiuso|aperto
scrivi_brief() {
  local n=$1 chiusura=${2:-chiuso}
  { print -r -- "<html><head><title>Morning Briefing</title></head><body>"
    for i in $(seq 1 $n); do
      print -r -- "<section><h2>World</h2><div class=\"story\"><h3>Notizia $i</h3><p>Testo.</p></div></section>"
    done
    [[ "$chiusura" == "chiuso" ]] && print -r -- "</body></html>"
  } > "$BRIEF"
}

print -r -- "=============================================================="
print -r -- "TEST — guardiano sull'integrità del briefing"
print -r -- "=============================================================="

# ---------------------------------------------------------------- 0. sintassi
print -- "\n0. Sintassi dello script INTERO (non solo la parte testata)"
if zsh -n "$SCRIPT" 2>/dev/null; then ok "run_daily_analysis.sh: sintassi valida"
else ko "run_daily_analysis.sh: sintassi valida" "zsh -n fallisce"; fi

# ---------------------------------------------------------------- 1. briefing assente
print -- "\n1. Briefing non ancora arrivato (caso normale delle 08:15)"
setup
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "esce con 0 senza fare nulla" "rc=$RC"
check "grep -q 'WAIT: briefing' '$LOG'" "logga WAIT"
check "! grep -q 'START' '$LOG'" "non avvia l'analisi"
check "[[ ! -d '$FPIPE/logs/.lock' ]]" "non lascia lock appesi"
teardown

# ---------------------------------------------------------------- 2. briefing completo
print -- "\n2. Briefing completo (caso felice)"
setup
scrivi_brief 20
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "esce con 0" "rc=$RC"
check "grep -q 'START' '$LOG'" "arriva ad avviare l'analisi"
check "! grep -q 'PARZIALE' '$LOG'" "non segnala attesa inutile"
check "[[ ! -d '$FPIPE/logs/.lock' ]]" "rilascia il lock"
teardown

# ---------------------------------------------------------------- 3. LA CORSA
print -- "\n3. Briefing parziale che si completa durante l'attesa (il guasto del 07/09)"
setup
scrivi_brief 0            # solo intestazione, come il file da 2.833 byte
( sleep 2; scrivi_brief 20 ) &   # il generatore finisce dopo 2s
COMPLETER=$!
RC=$(run_sut 20 1)
wait $COMPLETER 2>/dev/null
check "[[ $RC -eq 0 ]]" "esce con 0 dopo aver atteso" "rc=$RC"
check "grep -q 'PARZIALE' '$LOG'" "riconosce il file incompleto"
check "grep -q 'OK: briefing completo dopo' '$LOG'" "rileva il completamento"
check "grep -q 'START' '$LOG'" "prosegue con l'analisi"
check "! grep -q 'ERROR' '$LOG'" "non segnala errori"
teardown

# ---------------------------------------------------------------- 4. mai completato
print -- "\n4. Briefing che resta incompleto (fallimento che DEVE farsi sentire)"
setup
scrivi_brief 0
RC=$(run_sut 2 1)
check "[[ $RC -eq 1 ]]" "esce con codice 1" "rc=$RC"
check "grep -q 'ERROR' '$LOG'" "logga ERROR"
check "grep -q 'analisi NON eseguita' '$LOG'" "dice chiaramente cosa non è stato fatto"
check "grep -q 'run_daily_analysis.sh $GIORNO' '$LOG'" "suggerisce come rilanciare"
check "! grep -q 'START' '$LOG'" "NON avvia l'analisi sul vuoto"
check "[[ ! -d '$FPIPE/logs/.lock' ]]" "rilascia il lock anche fallendo"
teardown

# ------------------------------------------------- 5. forme di incompletezza
print -- "\n5. Le varie forme di file a metà"
setup
scrivi_brief 20 aperto     # 20 notizie ma senza </body>
RC=$(run_sut 1 1)
check "[[ $RC -eq 1 ]]" "20 notizie ma tag non chiuso → incompleto" "rc=$RC"
teardown
setup
scrivi_brief 9             # troncato a metà elenco
RC=$(run_sut 1 1)
check "[[ $RC -eq 1 ]]" "9 notizie su 20 → incompleto" "rc=$RC"
teardown
setup
: > "$BRIEF"               # file vuoto (0 byte)
RC=$(run_sut 1 1)
check "[[ $RC -eq 1 ]]" "file vuoto → incompleto" "rc=$RC"
teardown

# ---------------------------------------------------------------- 6. idempotenza
print -- "\n6. Idempotenza e lock"
setup
scrivi_brief 20
mkdir -p "$DAILY/$GIORNO"; print -r -- "# già fatto" > "$DAILY/$GIORNO/_index.md"
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "analisi già presente → esce subito" "rc=$RC"
check "grep -q 'SKIP: analisi' '$LOG'" "logga SKIP"
teardown
setup
scrivi_brief 0
mkdir -p "$FPIPE/logs/.lock"     # lock di un altro run
RC=$(run_sut 1 1)
check "[[ $RC -eq 0 ]]" "lock presente → esce senza aspettare" "rc=$RC"
check "grep -q 'SKIP: altro run' '$LOG'" "logga SKIP per il lock"
check "! grep -q 'PARZIALE' '$LOG'" "non si mette in attesa in parallelo"
teardown

# ------------------------------------------- 7. regressione sui briefing veri
print -- "\n7. Regressione: i 138 briefing reali sono tutti riconosciuti completi"
# Ogni file passa per lo SCRIPT VERO, non per una ri-scrittura del controllo:
# un test che ricopia la condizione verificherebbe la mia assunzione, non il codice.
setup
tot=0; accettati=0; storie_min=999; respinti=()
for f in "$BRIEF_REALI"/*.html(N); do
  cp "$f" "$BRIEF"
  rm -f "$LOG"
  n=$(grep -o 'class="story"' "$BRIEF" | wc -l | tr -d ' ')
  (( n < storie_min )) && storie_min=$n
  tot=$((tot+1))
  # WAIT_MAX=0 → nessuna attesa: o è completo subito, o viene respinto
  if [[ "$(run_sut 0 1)" -eq 0 ]] && grep -q 'START' "$LOG"; then
    accettati=$((accettati+1))
  else
    respinti+=("${f:t} (story=$n)")
  fi
done
check "[[ $tot -gt 100 ]]" "archivio trovato ($tot file)"
check "[[ $accettati -eq $tot ]]" "tutti accettati dallo script vero ($accettati/$tot)" \
      "respinti per errore: ${respinti[*]}"
check "[[ $storie_min -ge 20 ]]" "minimo storico di notizie = $storie_min (soglia $MIN_STORIES_ATTESA)"
teardown

# un briefing reale, passato per intero allo script
print -- "\n8. Un briefing reale, dentro lo script"
setup
cp "$(ls -1t "$BRIEF_REALI"/*.html | head -1)" "$BRIEF"
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "briefing reale accettato" "rc=$RC"
check "grep -q 'START' '$LOG'" "arriva ad avviare l'analisi"
check "! grep -q 'PARZIALE\|ERROR' '$LOG'" "nessun falso allarme"
teardown

print -- "\n=============================================================="
print -r -- "PASSATI: $PASS   ·   FALLITI: $FAIL"
print -r -- "=============================================================="
exit $(( FAIL > 0 ? 1 : 0 ))
