#!/bin/zsh
# run_daily_analysis.sh — wrapper lanciato da launchd (Fase 5).
#
# Lanciato sia alle 08:15 (StartCalendarInterval) sia ad ogni nuovo file
# nella cartella dei briefing (WatchPaths). È idempotente e auto-protetto:
#   - se l'analisi di oggi è già fatta (_index.md esiste) → esce
#   - se il briefing di oggi non è ancora arrivato → esce (sarà ri-triggerato
#     da WatchPaths appena il file atterra)
#   - se il briefing c'è ma è ancora a metà scrittura → aspetta che si completi,
#     e se non si completa fallisce ad alta voce invece di analizzare il vuoto
#   - lock per evitare run concorrenti (calendario + watchpath sovrapposti)
#   - ricostruisce il DB mercati se risulta incompleto
# Poi lancia Claude Code headless sul runbook.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# --- Configurazione --------------------------------------------------------
MODEL="claude-opus-5"   # modello per il run headless (Opus 5)

# Integrità del briefing (guasto del 2026-09-07, vedi la funzione brief_completo).
# MIN_STORIES=20 non è una stima: è un'invariante misurata su tutti i 138 briefing
# in archivio, che ne hanno esattamente 20 — nessuno ne ha mai avuti meno.
# Sovrascrivibili dall'ambiente solo perché la suite in tests/ possa verificare
# l'attesa senza restare ferma dieci minuti: launchd non le imposta.
MIN_STORIES=${MIN_STORIES:-20}
WAIT_MAX=${WAIT_MAX:-600}       # attesa massima del completamento, in secondi
WAIT_STEP=${WAIT_STEP:-15}      # ogni quanto ricontrollare
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

# Quante notizie contiene il briefing. Stessa definizione usata dal parser
# (`parse_briefing.py` cerca gli elementi con class="story"): se cambia il
# layout del briefing vanno aggiornati entrambi, non solo questo.
conta_story() { grep -o 'class="story"' "$BRIEF" 2>/dev/null | wc -l | tr -d ' '; }

# Il briefing è FINITO di essere scritto?
#
# ⚠ `WatchPaths` sorveglia la CARTELLA, quindi il job scatta quando il file viene
# creato — non quando il generatore ha finito di scriverlo. Il 2026-09-07 alle
# 09:15:42 il run è partito su un file di 2.833 byte con la sola intestazione HTML;
# quello completo (33.947 byte, 20 notizie) è arrivato un minuto dopo. Il digest sul
# file parziale ha prodotto ZERO notizie *senza errore*, con START e DB ok regolari a
# log: senza un controllo umano il run sarebbe finito con un `_index.md` vuoto e
# nessun segnale di guasto — la classe di guasto silenzioso di `quando_si_rompe.md`.
#
# Il solo `-f` non basta: servono due segni che la scrittura sia conclusa, il tag di
# chiusura e il conteggio delle notizie. Entrambi verificati su 138 briefing su 138.
brief_completo() {
  [[ -f "$BRIEF" ]]                          || return 1
  grep -q '</body>' "$BRIEF" 2>/dev/null     || return 1
  [[ "$(conta_story)" -ge "$MIN_STORIES" ]]
}

# L'ANALISI è finita di essere scritta? (guasto dell'11/09/2026)
#
# ⚠ Stessa classe di guasto del briefing a metà, un piano più in là: `_index.md`
# nasce come SCHELETRO di triage (tutte le righe a ⏳) e viene riempito alla fine,
# quindi la sua esistenza non dice che il run sia arrivato in fondo. L'11/09 Claude
# ha esaurito il limite di sessione dopo 6 schede su 20: lo scheletro c'era, il ramo
# di fallimento qui sotto l'ha preso per un successo e ha spedito su Telegram una
# tabella tutta ⏳, senza un ERROR a log né una notifica. Stesso esito il 31/07
# (limite di sessione) e il 19/07 (connection closed): tre run monchi, tre report
# partiti in silenzio, e in tutti e tre i casi l'intervento a mano.
#
# I due segni non sono una stima: su 105 `_index.md` in archivio i 102 sani non hanno
# né righe ⏳ né il segnaposto della Sintesi; i 3 rotti hanno entrambi. Sono i marcatori
# del template stesso (`PHASE5_RUNBOOK.md`): se cambiano lì, vanno cambiati anche qui.
index_completo() {
  [[ -f "$INDEX" ]]                                  || return 1
  ! grep -q '⏳' "$INDEX" 2>/dev/null                 || return 1
  ! grep -q 'Da compilare dopo il triage' "$INDEX" 2>/dev/null
}

# --- Idempotenza -----------------------------------------------------------
# Si esce solo davanti a un'analisi COMPLETA. Con il vecchio controllo di sola
# esistenza, uno scheletro lasciato da un run interrotto bloccava per sempre i
# tentativi successivi: l'11/09 alle 10:07 il ri-trigger ha loggato "SKIP" su
# un'analisi mai finita, e l'unico modo di rifarla era cancellare i file a mano.
if index_completo; then
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

# --- Il briefing è completo? (guasto del 2026-09-07) -----------------------
# Si ASPETTA dentro il processo invece di uscire e contare su un nuovo trigger:
# `WatchPaths` sorveglia la cartella e scatta quando il file compare, ma le
# scritture successive sullo stesso file non la modificano — nel log del 07/09 non
# c'è infatti nessun terzo trigger dopo quello sul file parziale. Uscendo qui, il
# run di quel giorno non sarebbe più ripartito da solo. L'attesa avviene DOPO il
# lock, così un trigger sovrapposto esce subito invece di mettersi ad aspettare
# anche lui.
if ! brief_completo; then
  log "PARZIALE: briefing incompleto ($(stat -f%z "$BRIEF" 2>/dev/null) byte, $(conta_story)/$MIN_STORIES notizie). Attendo il completamento (max ${WAIT_MAX}s)."
  waited=0
  while (( waited < WAIT_MAX )); do
    sleep "$WAIT_STEP"
    waited=$(( waited + WAIT_STEP ))
    if brief_completo; then
      log "OK: briefing completo dopo ${waited}s ($(conta_story) notizie)."
      break
    fi
  done
fi

# Scaduta l'attesa senza completamento è un guasto vero, e va detto ad alta voce:
# meglio nessuna analisi con un allarme che un'analisi vuota in silenzio.
if ! brief_completo; then
  MSG="briefing $TODAY incompleto dopo ${WAIT_MAX}s ($(conta_story)/$MIN_STORIES notizie): analisi NON eseguita. Controlla il generatore del brief, poi rilancia: run_daily_analysis.sh $TODAY"
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  exit 1
fi

# --- Ripresa di un run interrotto ------------------------------------------
# Arrivati qui l'analisi di oggi o non esiste o è monca. Se è monca, i residui non
# si sovrascrivono e non si cancellano: si spostano in un `_interrotto_<ora>/`, così
# il giorno riparte da una cartella pulita e il parziale resta consultabile. Il
# prefisso `_` non è estetico — `render_report.py` e `analogues.py` fanno glob NON
# ricorsivo su `news_*.md`, quindi una scheda lasciata lì finirebbe due volte nel
# report e nella libreria episodi.
#
# ⚠ Sta DOPO il lock di proposito: un trigger sovrapposto a un run in corso vedrebbe
# anche lui un'analisi incompleta — quella che l'agente sta scrivendo in quel momento —
# e senza lock gli sposterebbe i file da sotto i piedi.
RESIDUI=("$DAILY/$TODAY"/_index.md(N) "$DAILY/$TODAY"/news_*.md(N))
if (( ${#RESIDUI} )); then
  ARCH="$DAILY/$TODAY/_interrotto_$(date +%H%M%S)"
  mkdir -p "$ARCH" && mv "${RESIDUI[@]}" "$ARCH"/ \
    && log "RIPRESA: analisi di $TODAY interrotta a metà (${#RESIDUI} file). Parziale in ${ARCH:t}/, rifaccio da capo." \
    || log "WARN: analisi di $TODAY incompleta ma archiviazione del parziale fallita."
fi

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
   (verifica in category_asset_map.yaml, NON a memoria — leggilo UNA volta sola
   qui) e hanno un analogo storico plausibile;
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

ECONOMIA DEL RUN (vincolante, sezione omonima del runbook): il costo cresce col
QUADRATO dei turni. Quindi: raccogli TUTTO prima di scrivere (pool potato, event
study, match KB, sezione 5-bis della scorecard) e scrivi ogni file in UN SOLO
passaggio; per le correzioni usa Edit chirurgico, mai un heredoc che rigenera il
corpo; non rileggere ciò che hai appena scritto; non lanciare --help (i flag sono
nel runbook, sezione "Riferimento comandi"). Questo non deve accorciare né
impoverire le schede: stesso contenuto, meno giri.

Output finale in chat: riepilogo con quante notizie tenute/scartate e i temi
delle schede prodotte. Lavora in $DAILY/$TODAY/.
EOF

log "Lancio Claude Code headless (model=$MODEL)."
cd "$NEWSDIR"
# --output-format json: oltre al testo finale restituisce turni, token e costo.
# Senza questo il consumo del run non è misurabile (diagnosi del 2026-08-21: si
# poteva ricostruire solo scavando nei transcript di ~/.claude/projects/).
RAW="$LOGDIR/.raw_${TODAY}.json"
"$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions \
  --output-format json > "$RAW" 2>>"$LOG"
RC=$?
log "Claude exit code $RC."

# Estrae il testo finale (nel log, come prima) e accoda una riga al CSV dei consumi.
"$PY" - "$RAW" "$LOG" "$LOGDIR/usage.csv" "$TODAY" <<'PY' || log "WARN: parsing usage fallito."
import json, sys, os, csv
raw, logf, csvf, day = sys.argv[1:5]
try:
    d = json.load(open(raw))
except Exception:
    # JSON malformato (crash, auth scaduta): riversa il grezzo nel log e basta.
    with open(logf, 'a') as f:
        f.write(open(raw, errors='replace').read())
    raise SystemExit(0)

u = d.get('usage') or {}
cr = u.get('cache_read_input_tokens', 0)
cw = u.get('cache_creation_input_tokens', 0)
ti = u.get('input_tokens', 0)
to = u.get('output_tokens', 0)
turns = d.get('num_turns', 0)
cost = d.get('total_cost_usd', 0.0)

with open(logf, 'a') as f:
    f.write((d.get('result') or '') + '\n')
    f.write(f"[usage] turni={turns} input={ti} cache_write={cw} "
            f"cache_read={cr} output={to} costo=${cost:.2f}\n")

new = not os.path.exists(csvf)
with open(csvf, 'a', newline='') as f:
    w = csv.writer(f)
    if new:
        w.writerow(['date', 'turns', 'input', 'cache_write', 'cache_read',
                    'output', 'cost_usd', 'duration_ms'])
    w.writerow([day, turns, ti, cw, cr, to, f"{cost:.4f}",
                d.get('duration_ms', 0)])
PY
rm -f "$RAW"

# --- Allarme su fallimento del run headless -------------------------------
# Tre esiti, non due. Il segnale di successo non è che _index.md esista, ma che sia
# COMPILATO (v. index_completo):
#   assente   → fallimento pieno (tipico: 401 login scaduto) → ERROR + notifica + stop
#   monco     → run interrotto a metà (limite di sessione, connessione caduta): le
#               schede già prodotte si tengono e si spediscono, ma il giorno è marcato
#               INCOMPLETO ad alta voce e lo script esce ≠0. Era il buco dell'11/09.
#   compilato → successo, anche con exit ≠0 (errore finale non fatale a lavoro già
#               scritto: successo il 2026-07-10) → WARN e si prosegue.
INCOMPLETA=0
if [[ ! -f "$INDEX" ]]; then
  MSG="run $TODAY FALLITO (exit $RC, _index.md assente)."
  if grep -qi "Invalid authentication\|401\|Not logged in\|Please run /login" "$LOG" 2>/dev/null; then
    MSG="login Claude scaduto: esegui 'claude /login'. Run $TODAY non prodotto."
  elif grep -qi "session limit\|usage limit" "$LOG" 2>/dev/null; then
    MSG="limite di sessione Claude: run $TODAY non prodotto. Rilancia dopo il reset: run_daily_analysis.sh $TODAY"
  elif grep -qi "529\|Overloaded\|rate.limit\|500 Internal\|503" "$LOG" 2>/dev/null; then
    MSG="API sovraccarica (529/5xx): run $TODAY non prodotto. Rilancia: run_daily_analysis.sh $TODAY"
  fi
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
  # Anche senza analisi, il briefing grezzo va spedito: il 2026-08-24 un 529 ha
  # fatto uscire lo script qui, e il risultato è stato silenzio totale su Telegram
  # (nessun brief, nessuna analisi) — indistinguibile da "il job non è partito".
  log "Invio su Telegram del solo briefing (analisi assente)."
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" >> "$LOG" 2>&1 || log "WARN: invio Telegram fallito."
  exit 1
elif ! index_completo; then
  INCOMPLETA=1
  PARZIALI=("$DAILY/$TODAY"/news_*.md(N))
  PENDENTI=$(grep -c '⏳' "$INDEX" 2>/dev/null)
  MSG="analisi $TODAY INCOMPLETA (exit $RC): ${#PARZIALI} schede prodotte, $PENDENTI notizie non triate. Rilancia: run_daily_analysis.sh $TODAY"
  # L'ora di reset la scrive Claude stesso nell'ultima riga utile del log
  # ("You've hit your session limit · resets 12:40pm (Europe/Rome)"): riportarla
  # evita il rilancio a vuoto prima che il limite si sia azzerato.
  if grep -qi "session limit\|usage limit" "$LOG" 2>/dev/null; then
    RESET=$(grep -o 'resets [0-9:apm]*' "$LOG" 2>/dev/null | tail -1)
    MSG="limite di sessione Claude a metà run: analisi $TODAY INCOMPLETA (${#PARZIALI} schede, $PENDENTI notizie non triate). Rilancia${RESET:+ dopo le ${RESET#resets }}: run_daily_analysis.sh $TODAY"
  fi
  log "ERROR: $MSG"
  /usr/bin/osascript -e "display notification \"$MSG\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null
elif [[ $RC -ne 0 ]]; then
  log "WARN: Claude exit $RC ma _index.md compilato → procedo comunque con render + invio."
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
#
# Su run monco passa `--parziale`, che cambia la didascalia dell'analisi. Serve
# perché il guasto si legge dal telefono, dove la notifica desktop non arriva: senza,
# un'analisi a metà atterrerebbe con la stessa faccia di una completa — che è
# esattamente come l'11/09 è passata inosservata.
log "Invio su Telegram."
if (( INCOMPLETA )); then
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" --parziale >> "$LOG" 2>&1 || log "WARN: invio Telegram fallito."
else
  /bin/zsh "$PIPE/send_telegram.sh" "$TODAY" >> "$LOG" 2>&1 || log "WARN: invio Telegram fallito."
fi

# Un run monco non è "DONE": esce ≠0 così launchd e chi legge il log lo distinguono
# da un giorno andato a buon fine.
if (( INCOMPLETA )); then
  log "FINE: run $TODAY PARZIALE (vedi ERROR sopra)."
  exit 1
fi

log "DONE."
exit 0
