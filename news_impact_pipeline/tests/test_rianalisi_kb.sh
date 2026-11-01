#!/bin/zsh
# Test di run_rianalisi_kb.sh: cancelli, dati congelati al mattino, perimetro, invio.
#
#   ./tests/test_rianalisi_kb.sh
#
# Gira lo script VERO dentro un $HOME finto (tutti i percorsi derivano da $HOME).
# `claude` è un finto pilotato da FAKE_MODO; venv/bin/python è uno stub che registra
# le chiamate ai tool e delega a python3 solo i `-c`; send_telegram.sh scrive su file.
# Sotto test c'è il flusso della shell, non il contenuto delle schede.

set -u
PIPE="${0:A:h:h}"
SCRIPT="$PIPE/run_rianalisi_kb.sh"
PASS=0; FAIL=0
grep -q 'CLAUDE=${CLAUDE:-' "$SCRIPT" || { print "ABORT: \$CLAUDE non sostituibile"; exit 1; }

ok()  { print -r -- "  ✓ $1"; PASS=$((PASS+1)); }
ko()  { print -r -- "  ✗ $1"; FAIL=$((FAIL+1)); }
check() { if eval "$1"; then ok "$2"; else ko "$2"; fi }

setup() {
  SANDBOX=$(mktemp -d)
  FAKE_HOME="$SANDBOX/home"
  N="$FAKE_HOME/Claude/mercati_finanza"
  FPIPE="$N/news_impact_pipeline"
  OGGI=$(date +%Y-%m-%d)
  DAY="$N/daily_analysis/$OGGI"
  CALLS="$SANDBOX/calls.txt"
  mkdir -p "$FPIPE/logs" "$FPIPE/venv/bin" "$DAY" "$N/market_data/_mattino"
  print "# Scheda del mattino" > "$DAY/news_01.md"
  print "foto" > "$N/market_data/_mattino/$OGGI.db"
  print "{\"db\": \"$N/market_data/_mattino/$OGGI.db\", \"scorecard\": \"/x/2026-W44.md\", \"ora\": \"t\"}" > "$DAY/_mattino.json"
  cat > "$FPIPE/venv/bin/python" <<EOF
#!/bin/zsh
[[ "\$1" == "-c" ]] && exec python3 "\$@"
print -r -- "\${1:t} \${*:2}" >> "$CALLS"
[[ "\${1:t}" == stato_giornata.py && "\$*" == *--fase* ]] && print -r -- "\${FAKE_FASE:-completa}"
exit 0
EOF
  print '#!/bin/zsh\nexit 0' > "$FPIPE/attendi_rete.sh"
  print "#!/bin/zsh\nprint -r -- \"\$2\" > $SANDBOX/telegram.txt" > "$FPIPE/send_telegram.sh"
  cat > "$SANDBOX/claude" <<EOF
#!/bin/zsh
print -r -- "NEWSIMPACT_DB=\$NEWSIMPACT_DB ARGS=\$*" > "$SANDBOX/claude.txt"
if [[ "\${FAKE_MODO:-nuova}" == nuova ]]; then
  print "# Midterm USA, pool nuovo" > "$DAY/news_02.md"
  print "Riassunto per il telefono" > "$DAY/_rianalisi_\$(date +rev%H%M).md"
fi
print '{"result":"ok"}'
EOF
  chmod +x "$FPIPE/venv/bin/python" "$SANDBOX/claude"
}
run() { HOME="$FAKE_HOME" CLAUDE="$SANDBOX/claude" zsh "$SCRIPT" "Studio X/Studio X.md" >/dev/null 2>&1; }

print "1. giornata non consegnata → esce, niente agente"
setup; FAKE_FASE=schede_validate run
check '[[ ! -f $SANDBOX/claude.txt ]]' "claude non lanciato"
check 'grep -q "SKIP: giornata" $FPIPE/logs/rianalisi-$OGGI.log' "SKIP a log"
rm -rf "$SANDBOX"

print "2. senza fotografia del mattino → esce"
setup; rm "$DAY/_mattino.json"; run
check '[[ ! -f $SANDBOX/claude.txt ]]' "claude non lanciato"
check 'grep -q "fotografia del mattino" $FPIPE/logs/rianalisi-$OGGI.log' "motivo a log"
rm -rf "$SANDBOX"

print "3. scheda nuova → dati congelati, registrazione rivista, messaggio breve"
setup; run
check 'grep -q "NEWSIMPACT_DB=$N/market_data/_mattino/$OGGI.db" $SANDBOX/claude.txt' "prezzi = copia del mattino"
check 'grep -q -- "--strict-mcp-config" $SANDBOX/claude.txt && grep -q "WebSearch WebFetch" $SANDBOX/claude.txt' "niente MCP né web"
check 'grep -q "2026-W44.md" $SANDBOX/claude.txt' "scorecard del mattino nel prompt"
check 'grep -q "forecast_tracking.py register --date $OGGI --revisione rev" $CALLS' "ledger: versione rivista"
check 'grep -q "nuova news_02.md: Midterm USA, pool nuovo" $SANDBOX/telegram.txt' "messaggio con la scheda nuova"
check 'grep -q "Riassunto per il telefono" $SANDBOX/telegram.txt' "messaggio con il riassunto"
check 'grep -q "registra-consegna ok" $CALLS' "ricevuta riallineata"
check '[[ ! -d $FPIPE/logs/.lock ]]' "lock rilasciato"
rm -rf "$SANDBOX"

print "4. lo studio non serve nessuna notizia → niente registrazione né invio"
setup; FAKE_MODO=niente run
check '! grep -q "forecast_tracking.py" $CALLS' "ledger intatto"
check '[[ ! -f $SANDBOX/telegram.txt ]]' "nessun messaggio"
check 'grep -q "nessuna scheda toccata" $FPIPE/logs/rianalisi-$OGGI.log' "esito a log"
rm -rf "$SANDBOX"

print "\n$PASS ok, $FAIL falliti"
(( FAIL == 0 ))
