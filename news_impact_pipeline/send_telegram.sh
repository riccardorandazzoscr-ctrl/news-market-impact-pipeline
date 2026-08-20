#!/bin/zsh
# send_telegram.sh — invia brief + analisi del giorno su Telegram (lettura da telefono).
# Uso: send_telegram.sh [YYYY-MM-DD]   (default: oggi)
# Credenziali in ~/Claude/.env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
# Idempotenza leggera: se un file non esiste, lo salta senza errore.
set -u
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"

source <(grep -E '^TELEGRAM_(BOT_TOKEN|CHAT_ID)=' "$PROJECT/.env" 2>/dev/null)
TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT="${TELEGRAM_CHAT_ID:-}"
if [[ -z "$TOKEN" || -z "$CHAT" ]]; then
  echo "[telegram] credenziali mancanti in .env"; exit 1
fi

D="${1:-$(date +%Y-%m-%d)}"
API="https://api.telegram.org/bot${TOKEN}"
BRIEF="$PROJECT/morning brief/${D}-morning-briefing.html"
REPORT="$NEWSDIR/daily_analysis/$D/report.html"

sent=0
# --retry rende l'invio resistente ai blip di rete transitori (es. 2026-07-19,
# in cui un "connection closed" fece fallire l'invio pur con i file su disco).
CURL=(curl -s --retry 4 --retry-delay 5 --retry-all-errors --max-time 90)
if [[ -f "$BRIEF" ]]; then
  "${CURL[@]}" -F chat_id="$CHAT" \
    -F "document=@${BRIEF};filename=brief-${D}.html" \
    -F caption="📰 Morning brief ${D}" "$API/sendDocument" >/dev/null && sent=$((sent+1))
fi
if [[ -f "$REPORT" ]]; then
  "${CURL[@]}" -F chat_id="$CHAT" \
    -F "document=@${REPORT};filename=analisi-${D}.html" \
    -F caption="📊 Analisi del giorno ${D}" "$API/sendDocument" >/dev/null && sent=$((sent+1))
fi

echo "[telegram] inviati $sent file per $D"
[[ $sent -gt 0 ]]
