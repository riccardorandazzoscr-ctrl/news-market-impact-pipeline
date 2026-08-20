#!/bin/zsh
# run_daily_analysis.sh — wrapper lanciato da launchd (Fase 5).
#
# Lanciato sia alle 08:15 (StartCalendarInterval) sia ad ogni nuovo file
# nella cartella dei briefing (WatchPaths). È idempotente e auto-protetto:
#   - se l'analisi di oggi è già fatta (_index.md esiste) → esce
#   - se il briefing di oggi non è ancora arrivato → esce (sarà ri-triggerato
#     da WatchPaths appena il file atterra)
#   - lock per evitare run concorrenti (calendario + watchpath sovrapposti)
#   - ricostruisce il DB mercati se risulta incompleto
# Poi lancia Claude Code headless sul runbook.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# --- Configurazione --------------------------------------------------------
MODEL="claude-opus-5"   # modello per il run headless (Opus 5)
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
BRIEF_DIR="$PROJECT/morning brief"
DAILY="$NEWSDIR/daily_analysis"
LOGDIR="$PIPE/logs"
CLAUDE="/opt/homebrew/bin/claude"

mkdir -p "$LOGDIR"
# Data del run: di default oggi. Si può passare una data ISO come primo argomento
# per rigenerare a mano un giorno saltato (backfill), es. dopo un guasto di auth:
#   run_daily_analysis.sh 2026-06-25
# L'idempotenza vale comunque: se _index.md di quel giorno esiste già, esce.
TODAY=${1:-$(date +%Y-%m-%d)}
BRIEF="$BRIEF_DIR/${TODAY}-morning-briefing.html"
INDEX="$DAILY/$TODAY/_index.md"
LOG="$LOGDIR/${TODAY}.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# --- Idempotenza -----------------------------------------------------------
if [[ -f "$INDEX" ]]; then
  log "SKIP: analisi di $TODAY già presente ($INDEX)."
  exit 0
fi

# --- Briefing arrivato? ----------------------------------------------------
if [[ ! -f "$BRIEF" ]]; then
  log "WAIT: briefing $TODAY non ancora presente. Esco (ri-trigger all'arrivo)."
  exit 0
fi

# --- Lock (evita doppio run calendario+watchpath) --------------------------
LOCK="$LOGDIR/.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP: altro run in corso (lock presente)."
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "START: briefing $TODAY trovato, avvio analisi."

# --- Salute DB: ricostruisci se incompleto ---------------------------------
DBCHECK=$("$PY" - <<'PY'
import sqlite3, os
p = os.path.expanduser('~/Claude/mercati_finanza/market_data/market_data.db')
try:
    c = sqlite3.connect(p)
    t = c.execute("SELECT COUNT(DISTINCT ticker) FROM prices").fetchone()[0]
    print(t)
except Exception:
    print(0)
PY
)
if [[ "${DBCHECK:-0}" -lt 44 ]]; then
  log "DB incompleto (ticker=$DBCHECK<44). Ricostruisco (bootstrap + spread daily)."
  "$PY" "$PIPE/bootstrap_market_data.py" >> "$LOG" 2>&1
  "$PY" "$PIPE/fetch_daily_spread.py"     >> "$LOG" 2>&1 || \
    "$PY" "$PIPE/fetch_fred_data.py"      >> "$LOG" 2>&1
else
  log "DB ok (ticker=$DBCHECK)."
fi

# --- Backstop indicizzazione KB (Variante A) -------------------------------
# I WatchPaths su knowledge_base/ gestiscono il caso "nuova sottocartella", ma
# non sempre l'aggiunta di un file dentro una cartella già esistente. Qui
# garantiamo che ogni studio non indicizzato lo sia prima del match del giorno.
# index_studies.sh è idempotente: no-op se non c'è nulla da indicizzare.
log "Backstop: controllo studi KB non indicizzati."
/bin/zsh "$PIPE/index_studies.sh" >> "$LOG" 2>&1

# Rinfresca la libreria di episodi (Opzione B): include le schede prodotte finora,
# così l'event study di oggi può pescare un pool ampio di analoghi invece di 5 a mano.
log "Refresh libreria episodi (analogues)."
"$PY" "$PIPE/analogues.py" build >> "$LOG" 2>&1

# --- Prompt per l'agente ---------------------------------------------------
read -r -d '' PROMPT <<EOF
Processa il morning briefing di oggi ($TODAY) seguendo ESATTAMENTE il runbook
$PIPE/PHASE5_RUNBOOK.md. Passi:
1) Genera il digest di triage: pipeline_tools.py digest --date $TODAY
2) Tria le 20 notizie con scope "subset triato": scheda completa SOLO per
   notizie che mappano su uno degli asset dell'universo corrente in DB
   (verifica nell'elenco aggiornato category_asset_map.yaml, NON a memoria:
   include ora anche AI/semis ^NDX/SOXX, rame HG=F, credito HYG/^VIX, EM EEM,
   uranio/litio URA/LIT, dollaro DX-Y.NYB) e hanno un analogo storico plausibile;
   consolida notizie sullo stesso tema in un'unica scheda; scarta il resto con
   una riga di motivazione. Compila la tabella di _index.md.
3) Per ogni notizia tenuta esegui il flusso completo (assets, match, new-card).
   Per gli episodi analoghi usa la LIBRERIA (Opzione B): analogues.py find --theme
   <theme> --subtheme <tok> --direction <pos|neg|neutral> --before <data notizia> →
   usa quel pool per --events di event_study.py. Passa SEMPRE --direction e, sui temi
   larghi (geopolitical, commodity_energy), anche --subtheme (senza filtri il pool
   diluisce il segnale). La libreria applica già un tetto di recency (30 più recenti).
   Puoi potare i non pertinenti; integra a mano solo se il pool è piccolo. Poi compila
   via Edit tutte le sezioni qualitative. Se min(N)<10 la scheda riporta "INDICATIVE ONLY".
   PRIMA di scrivere la lettura direzionale leggi la scorecard più recente in
   $DAILY/_scorecard/ sezione "5-bis" (per-asset): sugli asset marcati ❌ controproducente
   (IC storicamente negativo) NON trarre una direzione attesa — riporta l'event study ma
   dichiara che il segno storico è inaffidabile. Rileggi l'elenco lì, non a memoria.
4) Compila la "Sintesi di sessione" in _index.md.
Output finale in chat: riepilogo con quante notizie tenute/scartate e i temi
delle schede prodotte. Lavora in $DAILY/$TODAY/.
EOF

log "Lancio Claude Code headless (model=$MODEL)."
cd "$NEWSDIR"
"$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions >> "$LOG" 2>&1
RC=$?
log "Claude exit code $RC."

# --- Allarme su fallimento del run headless -------------------------------
# Il vero segnale di successo è che _index.md sia stato prodotto. Se manca è un
# fallimento reale (tipico: 401 login scaduto) → ERROR + notifica desktop + stop.
# MA se _index.md c'è e Claude è comunque uscito con codice ≠0 (errore finale non
# fatale dopo aver già scritto tutto — successo il 2026-07-10), NON buttiamo via il
# giorno: logghiamo un WARN e proseguiamo col render + invio Telegram.
if [[ ! -f "$DAILY/$TODAY/_index.md" ]]; then
  MSG="run $TODAY FALLITO (exit $RC, _index.md assente)."
  if grep -qi "Invalid authentication\|401\|Not logged in\|Please run /login" "$LOG" 2>/dev/null; then
    MSG="login Claude scaduto: esegui 'claude /login'. Run $TODAY non prodotto."
  fi
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  exit 1
elif [[ $RC -ne 0 ]]; then
  log "WARN: Claude exit $RC ma _index.md prodotto → procedo comunque con render + invio."
fi

# Render HTML del report (apribile con doppio clic nel browser).
if [[ -f "$DAILY/$TODAY/_index.md" ]]; then
  "$PY" "$PIPE/render_report.py" --date "$TODAY" >> "$LOG" 2>&1 \
    && log "Report HTML generato: $DAILY/$TODAY/report.html" \
    || log "WARN: render_report.py fallito."
else
  log "WARN: _index.md assente, salto il render HTML."
fi

# --- Invio su Telegram (lettura push da telefono) --------------------------
# Canale primario su telefono (indipendente da iCloud): manda brief + analisi
# in chat col bot. Credenziali in .env. Non blocca il run se fallisce.
log "Invio su Telegram."
/bin/zsh "$PIPE/send_telegram.sh" "$TODAY" >> "$LOG" 2>&1 || log "WARN: invio Telegram fallito."

log "DONE."
exit 0
