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

API="https://api.telegram.org/bot${TOKEN}"
# --retry rende l'invio resistente ai blip di rete transitori (es. 2026-07-19,
# in cui un "connection closed" fece fallire l'invio pur con i file su disco).
CURL=(curl -s --retry 4 --retry-delay 5 --retry-all-errors --max-time 90)

# send_doc: invia un documento e verifica sia l'HTTP status sia il campo JSON
# "ok" della risposta Telegram — un curl "riuscito" (retry compreso) può
# comunque restituire {"ok":false,...} su es. token scaduto o chat_id errato.
# Stampa una ricevuta per l'artefatto e ritorna 0/1 di conseguenza.
send_doc() {
  local file="$1" fname="$2" caption="$3" resp http body
  resp=$("${CURL[@]}" -w $'\n%{http_code}' -F chat_id="$CHAT" \
    -F "document=@${file};filename=${fname}" \
    -F caption="$caption" "$API/sendDocument")
  http="${resp##*$'\n'}"
  body="${resp%$'\n'*}"
  if [[ "$http" == "200" && "$body" == *'"ok":true'* ]]; then
    echo "[telegram] OK: ${fname}"
    return 0
  fi
  echo "[telegram] FALLITO: ${fname} (http=${http}) ${body:0:200}"
  return 1
}

# Modalità scorecard: send_telegram.sh --scorecard [AAAA-Www]
# Chiamata da run_scorecard.sh. Prima del 2026-08-24 la scorecard settimanale
# veniva rigenerata correttamente ma non spediva nulla: restava invisibile in
# daily_analysis/_scorecard/ e sembrava che il job non fosse partito.
if [[ "${1:-}" == "--scorecard" ]]; then
  W="${2:-$(date +%G-W%V)}"
  SC="$NEWSDIR/daily_analysis/_scorecard/${W}.html"
  if [[ -f "$SC" ]]; then
    if send_doc "$SC" "scorecard-${W}.html" "🎯 Scorecard settimanale ${W}"; then
      exit 0
    fi
    echo "[telegram] invio scorecard $W fallito"; exit 1
  fi
  echo "[telegram] scorecard $W non trovata ($SC)"; exit 1
fi

D="${1:-$(date +%Y-%m-%d)}"
BRIEF="$PROJECT/morning brief/${D}-morning-briefing.html"
REPORT="$NEWSDIR/daily_analysis/$D/report.html"

# send_telegram.sh AAAA-MM-GG --parziale → didascalia d'allarme sull'analisi.
# La passa run_daily_analysis.sh quando il run si è interrotto a metà: il report
# contiene le schede fatte fino a lì, ma il triage è rimasto in sospeso e la
# differenza deve vedersi dal telefono, non solo nel log sul Mac.
CAP_ANALISI="📊 Analisi del giorno ${D}"
if [[ "${2:-}" == "--parziale" ]]; then
  CAP_ANALISI="⚠️ Analisi ${D} INCOMPLETA — run interrotto a metà: triage in sospeso, schede parziali. Da rifare."
fi

expected=0
sent=0
if [[ -f "$BRIEF" ]]; then
  expected=$((expected+1))
  send_doc "$BRIEF" "brief-${D}.html" "📰 Morning brief ${D}" && sent=$((sent+1))
fi
if [[ -f "$REPORT" ]]; then
  expected=$((expected+1))
  send_doc "$REPORT" "analisi-${D}.html" "$CAP_ANALISI" && sent=$((sent+1))
fi

echo "[telegram] inviati $sent/$expected file per $D"
[[ $expected -gt 0 && $sent -eq $expected ]]
