#!/bin/zsh
# run_scorecard.sh — feedback-loop settimanale del News Impact Pipeline.
# Lanciato da launchd (com.newsimpact.scorecard) ogni lunedì mattina.
# Esegue forecast_tracking.py run = backfill + evaluate + scorecard:
#   - backfill: accoda al ledger le previsioni delle schede della settimana
#   - evaluate: riempie col realizzato (dal DB) le previsioni ormai mature
#   - scorecard: rigenera daily_analysis/_scorecard/AAAA-Www.md
# Maturazione ROLLING: ciò che non è ancora maturo (es. T+10) viene raccolto
# alle esecuzioni successive. Puramente deterministico: nessuna chiamata API.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

PIPE="$HOME/Claude/mercati_finanza/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
LOGDIR="$PIPE/logs"
mkdir -p "$LOGDIR"
LOG="$LOGDIR/scorecard.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Lock anti-concorrenza (run manuale + launchd).
LOCK="$LOGDIR/.lock_scorecard"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP: altro run scorecard in corso (lock presente)."
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "START run_scorecard."
cd "$PIPE"
"$PY" forecast_tracking.py run >> "$LOG" 2>&1
RC=$?

# Invio su Telegram (dal 2026-08-24): prima la scorecard veniva rigenerata ma
# restava solo su disco, quindi era indistinguibile da un job non partito.
if [[ $RC -eq 0 ]]; then
  /bin/zsh "$PIPE/send_telegram.sh" --scorecard >> "$LOG" 2>&1 \
    || log "WARN: invio Telegram della scorecard fallito."
fi

log "DONE run_scorecard (rc=$RC)."
exit 0
