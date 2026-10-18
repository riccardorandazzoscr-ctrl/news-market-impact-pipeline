#!/bin/zsh
# run_weekly_preview.sh — wrapper launchd dell'anteprima settimanale.
# Gira ogni ora (StartInterval + RunAtLoad), ma lavora solo quando `target-week` dà un
# lunedì: domenica dalle 18:00 per la settimana dopo, lunedì e martedì per quella in
# corso (ripresa a Mac spento). Numeri da weekly_preview.py, testo da Claude headless,
# poi validazione, render e invio Telegram. Idempotente: un'anteprima valida non si rifà.
# Spec: docs/superpowers/specs/2026-10-17-anteprima-settimanale-design.md

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

MODEL="claude-opus-5-5"
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
WP="$PIPE/weekly_preview.py"
LOGDIR="$PIPE/logs"
CLAUDE="/opt/homebrew/bin/claude"
mkdir -p "$LOGDIR"

MONDAY=$("$PY" "$WP" target-week) || exit 1
[[ -z "$MONDAY" ]] && exit 0      # fuori finestra: giro a vuoto, nessun log

WEEK=$("$PY" -c "from datetime import date; y,w,_=date.fromisoformat('$MONDAY').isocalendar(); print(f'{y}-W{w:02d}')")
WEEKDIR="$NEWSDIR/weekly_preview/$WEEK"
LOG="$LOGDIR/weeklypreview-${WEEK}.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Un solo tentativo a settimana: con un testo non valido il report è già uscito con le sole
# tabelle, e rilanciare il modello ogni ora fino a martedì costerebbe un run a giro.
# Per rifarla a mano: cancellare anteprima.html della settimana.
[[ -f "$WEEKDIR/anteprima.html" ]] && exit 0

LOCK="$LOGDIR/.lock_weeklypreview"
# Un run vero dura al massimo ~20 minuti (rete + modello): un lock di oltre 3 ore è rimasto
# da un Mac spento o da un kill, e senza questa pulizia il job uscirebbe in silenzio per sempre.
if [[ -d "$LOCK" && -n "$(find "$LOCK" -maxdepth 0 -mmin +180)" ]]; then
  rmdir "$LOCK" && log "Lock orfano rimosso (più vecchio di 3 ore)."
fi
mkdir "$LOCK" 2>/dev/null || { log "SKIP: altro run in corso (lock presente)."; exit 0; }
trap 'if [[ -n "${RAW:-}" && -f "${RAW:-}" ]]; then
        "$PY" "$PIPE/record_claude_usage.py" "$RAW" "$LOG" "$LOGDIR/usage_weeklypreview.csv" \
          "$WEEK" weeklypreview "$MODEL" interrotto 2>/dev/null
        /bin/rm -f "$RAW"
      fi
      rmdir "$LOCK" 2>/dev/null' EXIT

source <(grep -E '^TELEGRAM_(BOT_TOKEN|CHAT_ID)=' "$PROJECT/.env" 2>/dev/null)
API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN:-}"
CURL=(curl -s --retry 4 --retry-delay 5 --retry-all-errors --max-time 90)
tg_ok() { [[ "$1" == *'"ok":true'* ]] }

log "START anteprima $WEEK (lunedì $MONDAY)."
RETE_URL=https://api.stlouisfed.org /bin/zsh "$PIPE/attendi_rete.sh" >/dev/null || {
  log "SKIP: rete assente dopo l'attesa, riprovo al giro dopo."; exit 0; }

AVVISO=$("$PY" "$WP" check-calendar 2>>"$LOG")
if [[ -n "$AVVISO" ]]; then
  tg_ok "$("${CURL[@]}" -d chat_id="${TELEGRAM_CHAT_ID:-}" --data-urlencode text="$AVVISO" "$API/sendMessage")" \
    && log "Avviso calendario inviato." || log "WARN: avviso calendario non inviato."
fi

cd "$NEWSDIR"
"$PY" "$WP" build --week-of "$(date -j -v-1d -f %Y-%m-%d "$MONDAY" +%Y-%m-%d)" \
  --as-of "$(date +%Y-%m-%d)" >> "$LOG" 2>&1 || { log "ERROR: build fallita."; exit 1; }

N_OK=$("$PY" -c "import json; print(sum(e['status']=='ok' for e in json.load(open('$WEEKDIR/tabelle.json'))['events']))")
N_ALL=$("$PY" -c "import json; print(len(json.load(open('$WEEKDIR/tabelle.json'))['events']))")
NOTA=""
if (( N_OK > 0 )); then
  PROMPT=$(awk '/^=== PROMPT START ===$/{p=1;next} /^=== PROMPT END ===$/{p=0} p' \
    "$PIPE/weekly_preview_prompt.md" | sed "s|{{WEEK_DIR}}|$WEEKDIR|g")
  RAW="$LOGDIR/.raw_weeklypreview_${WEEK}.json"
  rm -f "$WEEKDIR/testo.md"
  "$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions \
    --output-format json </dev/null > "$RAW" 2>>"$LOG"
  log "Claude exit code $?."
  "$PY" "$PIPE/record_claude_usage.py" "$RAW" "$LOG" "$LOGDIR/usage_weeklypreview.csv" \
    "$WEEK" weeklypreview "$MODEL" || log "WARN: parsing usage fallito."
  rm -f "$RAW"
  "$PY" "$WP" validate "$WEEKDIR" >> "$LOG" 2>&1 || { log "WARN: testo non valido, report con le sole tabelle."; NOTA=" — solo tabelle"; }
else
  log "Nessun evento con analoghi sufficienti: niente run del modello."
  NOTA=" — nessun evento con analoghi sufficienti"
fi

# Grafici deterministici (nessun modello): prima del render, che li incorpora nell'HTML.
"$PY" "$WP" charts "$WEEKDIR" >> "$LOG" 2>&1 || log "WARN: grafici non prodotti, il report esce senza."
"$PY" "$WP" render "$WEEKDIR" >> "$LOG" 2>&1 || { log "ERROR: render fallito."; exit 1; }
CAPTION="Anteprima $WEEK: $N_ALL eventi, $N_OK con analoghi$NOTA"
if tg_ok "$("${CURL[@]}" -F chat_id="${TELEGRAM_CHAT_ID:-}" -F "document=@$WEEKDIR/anteprima.html;filename=anteprima-$WEEK.html" \
     -F caption="$CAPTION" "$API/sendDocument")"; then
  log "DONE: $CAPTION (inviato)."
else
  log "WARN: $CAPTION, ma invio Telegram fallito."
fi
# I grafici come file (non foto): Telegram comprime le foto, per LinkedIn serve l'originale.
for PNG in "$WEEKDIR"/grafico-*.png(N); do
  tg_ok "$("${CURL[@]}" -F chat_id="${TELEGRAM_CHAT_ID:-}" -F "document=@$PNG;filename=${WEEK}-${PNG:t}" \
       -F caption="Grafico per il post: ${PNG:t:r}" "$API/sendDocument")" || log "WARN: grafico ${PNG:t} non inviato."
done
