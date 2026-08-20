#!/bin/zsh
# run_monthly_report.sh — wrapper launchd (Fase 6 / Layer 6).
# Una volta al mese (1° del mese) produce il Report Strategico Mensile del mese
# appena concluso: genera la bozza aggregata, lancia Claude headless per compilare
# le sezioni (PHASE6_RUNBOOK.md), poi rende l'HTML. Idempotente (sentinella .done).

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

MODEL="claude-opus-5"
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
MONTHLY="$NEWSDIR/daily_analysis/_monthly"
LOGDIR="$PIPE/logs"
CLAUDE="/opt/homebrew/bin/claude"

mkdir -p "$LOGDIR" "$MONTHLY"
MONTH=$(date -v-1m +%Y-%m)          # mese appena concluso (BSD date, macOS)
LOG="$LOGDIR/monthly-${MONTH}.log"
DONE="$MONTHLY/.done-${MONTH}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

if [[ -f "$DONE" ]]; then
  log "SKIP: report $MONTH già prodotto."
  exit 0
fi

LOCK="$LOGDIR/.lock_monthly"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP: altro run mensile in corso (lock presente)."
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "START report mensile $MONTH."

# 1) Bozza aggregata (input per l'agente).
"$PY" "$PIPE/monthly_digest.py" --month "$MONTH" --force >> "$LOG" 2>&1

# 2) Compilazione sezioni via Claude headless.
read -r -d '' PROMPT <<EOF
Produci il Report Strategico Mensile per $MONTH seguendo ESATTAMENTE il runbook
$PIPE/PHASE6_RUNBOOK.md. La bozza aggregata è già in
$MONTHLY/$MONTH.md (NON modificare la sezione "Materiale aggregato"). Compila via
Edit le 6 sezioni: 1) regimi attivi 2) bilancio rischi cross-asset 3) calendario
catalizzatori 4) scenari condizionali 5) lettura pesata dalla scorecard 6) 3-4
previsioni falsificabili (tabella). Apri con un breve consuntivo delle previsioni
falsificabili del mese precedente se esiste. Rispetta lo stile (espandi le sigle,
spiega i meccanismi, interpreta i numeri a parole) e la disciplina della scorecard:
dai peso ai temi con edge e NIENTE magnitudo sui temi a IC negativo (es. AI/
structural_themes → lettura qualitativa). Output in chat: regimi dominanti + le
previsioni falsificabili.
EOF

cd "$NEWSDIR"
"$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions >> "$LOG" 2>&1
log "Claude exit code $?."

# 3) Render HTML del report compilato.
"$PY" "$PIPE/monthly_digest.py" --month "$MONTH" --render-only >> "$LOG" 2>&1 \
  && log "HTML report mensile generato: $MONTHLY/$MONTH.html" \
  || log "WARN: render-only fallito."

touch "$DONE"
log "DONE report mensile $MONTH."
exit 0
