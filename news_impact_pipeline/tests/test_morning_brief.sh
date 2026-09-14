#!/bin/zsh
# test_morning_brief.sh — guardiano sul job che PRODUCE il briefing (07:30).
#
# Perché esiste: fino al 15/09/2026 questo passo non aveva uno script — era una
# routine cloud, poi un task dell'app ChatGPT — quindi non aveva neppure un test.
# Ora gira da solo ogni mattina, prima di tutto il resto: se fallisce in silenzio
# non esce il brief, e senza brief alle 08:15 non c'è analisi. È la testa della
# catena, ed è il posto dove un guasto muto costa di più.
#
# Copre cinque cose:
#   1. idempotenza — briefing già presente e completo → SKIP, nessun doppione
#   2. successo — file pubblicato → DONE, lock rilasciato, .raw ripulito
#   3. fallimento — il modello non pubblica nulla → ERROR ad alta voce, exit ≠0
#   4. briefing scritto a metà → trattato da assente, non accettato per buono
#   5. il prompt viene estratto dal blocco canonico, senza le note italiane
#
# Non distruttivo: tutto dentro una HOME finta in una cartella temporanea.

set -u
PIPE="${0:A:h:h}"
SCRIPT="$PIPE/run_morning_brief.sh"
PASS=0; FAIL=0

# ⚠ Guardia, non un test: senza la sostituzione di $CLAUDE ogni caso qui sotto
# lancerebbe il binario VERO con --permission-mode bypassPermissions — cioè una
# ricerca web a pagamento per ogni run della suite.
if ! grep -q 'CLAUDE=${CLAUDE:-' "$SCRIPT"; then
  print -r -- "ABORT: run_morning_brief.sh non permette di sostituire \$CLAUDE."
  print -r -- "       Senza quella sostituzione questa suite lancerebbe il claude vero."
  exit 1
fi

ok()  { print -r -- "  ✓ $1"; PASS=$((PASS+1)); }
ko()  { print -r -- "  ✗ $1"; print -r -- "      $2"; FAIL=$((FAIL+1)); }
check() { if eval "$1"; then ok "$2"; else ko "$2" "${3:-condizione non soddisfatta: $1}"; fi }

GIORNO="2026-09-15"

setup() {
  SANDBOX=$(mktemp -d)
  FAKE_HOME="$SANDBOX/home"
  BDIR="$FAKE_HOME/Claude/morning brief"
  FPIPE="$FAKE_HOME/Claude/mercati_finanza/news_impact_pipeline"
  mkdir -p "$BDIR" "$FPIPE/logs" "$FPIPE/venv/bin"

  BRIEF="$BDIR/${GIORNO}-morning-briefing.html"
  LOG="$FPIPE/logs/brief-${GIORNO}.log"
  LOCK="$FPIPE/logs/.lock_brief"
  RAW="$FPIPE/logs/.raw_brief_${GIORNO}.json"
  VISTO="$SANDBOX/prompt_visto.txt"

  cp "$SCRIPT" "$FPIPE/run.sh"
  cp "$PIPE/news_research_prompt.md" "$FPIPE/news_research_prompt.md"
  cp "$PIPE/record_claude_usage.py" "$FPIPE/record_claude_usage.py"
  # Il venv finto è solo un passacarte al python di sistema: al parser dei
  # consumi non serve nessuna dipendenza esterna.
  { print -r -- '#!/bin/zsh'; print -r -- 'exec /usr/bin/python3 "$@"' } > "$FPIPE/venv/bin/python"
  chmod +x "$FPIPE/venv/bin/python"

  # --- finto `claude -p`, pilotato da variabili d'ambiente ---
  # Salva il prompt ricevuto (caso 4) e pubblica o no il file (casi 2 e 3).
  cat > "$SANDBOX/claude_finto" <<'FAKE'
#!/bin/zsh
# l'ultimo argomento non-flag dopo -p è il prompt
print -r -- "$2" > "$FAKE_VISTO"
if [[ -n "${FAKE_PUBBLICA:-}" ]]; then
  { print -r -- "<html><body>"
    for i in 1 2 3; do
      print -r -- "<h2>International</h2><div class=\"story\"><h3>N$i</h3><p>T.</p></div>"
    done
    print -r -- "</body></html>" } > "$FAKE_BRIEF"
fi
print -r -- '{"result":"fatto","num_turns":3,"total_cost_usd":1.5,"duration_ms":1000,"usage":{"input_tokens":10,"output_tokens":20,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}'
exit ${FAKE_RC:-0}
FAKE
  chmod +x "$SANDBOX/claude_finto"
}

teardown() { [[ -n "${SANDBOX:-}" ]] && rm -rf "$SANDBOX"; }

esegui() {
  ( HOME="$FAKE_HOME" CLAUDE="$SANDBOX/claude_finto" \
    FAKE_VISTO="$VISTO" FAKE_BRIEF="$BRIEF" \
    FAKE_PUBBLICA="${1:-}" FAKE_RC="${2:-0}" \
    /bin/zsh "$FPIPE/run.sh" "$GIORNO" >/dev/null 2>&1 )
  echo $?
}

scrivi_brief_completo() {
  { print -r -- "<html><body>"
    print -r -- "<div class=\"story\"><h3>Vecchia</h3></div>"
    print -r -- "</body></html>" } > "$BRIEF"
}

print -- "\n1. Briefing già presente e completo → SKIP, niente doppioni"
setup
scrivi_brief_completo
PRIMA=$(md5 -q "$BRIEF")
RC=$(esegui pubblica)
check "[[ $RC -eq 0 ]]" "esce 0" "rc=$RC"
check "grep -q 'SKIP' '$LOG'" "logga SKIP"
check "[[ \$(md5 -q '$BRIEF') == '$PRIMA' ]]" "NON riscrive il briefing esistente"
check "[[ ! -f '$VISTO' ]]" "non chiama nemmeno il modello (nessuna spesa a vuoto)"
teardown

print -- "\n2. Nessun briefing → lo produce e lo dichiara"
setup
RC=$(esegui pubblica)
check "[[ $RC -eq 0 ]]" "esce 0" "rc=$RC"
check "[[ -f '$BRIEF' ]]" "il briefing è sul disco"
check "grep -q 'DONE briefing' '$LOG'" "logga DONE"
check "grep -q '3 notizie' '$LOG'" "conta le notizie pubblicate" "$(tail -3 $LOG 2>/dev/null)"
check "[[ ! -d '$LOCK' ]]" "il lock è rilasciato"
check "[[ ! -f '$RAW' ]]" "il .raw temporaneo non resta indietro"
check "grep -q '\[usage\]' '$LOG'" "il consumo del run è registrato"
check "[[ -f '$FPIPE/logs/usage_brief.csv' ]]" "la riga finisce nel CSV dei consumi"
teardown

print -- "\n3. Il modello non pubblica nulla → ERROR, non silenzio"
setup
RC=$(esegui "" 0)
check "[[ $RC -ne 0 ]]" "esce ≠0 anche se il modello è uscito 0" "rc=$RC"
check "grep -q 'ERROR' '$LOG'" "logga ERROR"
check "grep -q 'NON prodotto' '$LOG'" "dice esattamente cosa manca"
check "[[ ! -d '$LOCK' ]]" "il lock è rilasciato anche sul fallimento"
teardown

print -- "\n4. Briefing scritto a metà (niente </body>) → trattato da assente"
setup
print -r -- "<html><body><div class=\"story\">" > "$BRIEF"   # nessuna chiusura
RC=$(esegui "" 0)
check "[[ $RC -ne 0 ]]" "non lo accetta come valido" "rc=$RC"
check "[[ -f '$VISTO' ]]" "riprova a produrlo invece di uscire con SKIP"
teardown

print -- "\n5. Il prompt passato è il blocco canonico, non il file intero"
setup
RC=$(esegui pubblica)
check "[[ -f '$VISTO' ]]" "il modello ha ricevuto un prompt"
check "grep -q 'Use web search' '$VISTO'" "contiene il corpo del prompt"
check "grep -q '$GIORNO' '$VISTO'" "la data la fissa lo script, non il modello"
check "! grep -q 'PROMPT START' '$VISTO'" "i marcatori restano fuori"
check "! grep -q 'Changelog' '$VISTO'" "le note italiane di testata restano fuori"
teardown

print -- "\n$(printf '=%.0s' {1..60})"
print -r -- "morning brief: $PASS passati, $FAIL falliti"
print -r -- "$(printf '=%.0s' {1..60})"
exit $(( FAIL > 0 ))
