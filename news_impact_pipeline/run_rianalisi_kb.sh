#!/bin/zsh
# run_rianalisi_kb.sh — rifà le schede di OGGI toccate da una research appena indicizzata
# o da versi appena rivisti.
#
# Uso: run_rianalisi_kb.sh "<source_file dello studio, relativo a knowledge_base/>" [...]
#      run_rianalisi_kb.sh --versi "<knowledge_base/_recupero/<proposta>.yaml>" [...]
# Lo lancia index_studies.sh dopo aver indicizzato uno studio nuovo, e recupero.py
# promuovi dopo aver portato nel registro versi approvati; a mano va bene uguale.
# Con --versi (decisione del maintainer, 2026-11-03) l'unica cosa nuova sono le voci
# promosse della proposta: si rifanno solo le schede del loro tema che citano il loro
# asset, e nella scheda cambia solo ciò che quelle voci cambiano.
#
# La domanda a cui risponde (decisione del maintainer, 2026-11-01): che cosa avrebbe
# scritto il run del mattino se lo studio fosse già esistito? Quindi tutto è fermo al
# brief e l'unica cosa nuova è la research:
#   - prezzi: la copia salvata dal run del mattino (NEWSIMPACT_DB), non il DB vivo;
#   - scorecard: quella che il mattino aveva come più recente (_mattino.json);
#   - niente web né MCP: l'agente legge solo brief, KB e prezzi congelati;
#   - perimetro: solo le notizie di oggi che lo studio serve; il resto non si tocca.
# Le schede rifatte entrano nel ledger come versione rivista accanto all'originale
# (forecast_tracking.py register --revisione), così la scorecard misura se la
# research migliora davvero le stime. Su Telegram parte un messaggio breve.
#
# Solo la giornata in corso: riaprire un giorno passato con uno studio scritto dopo
# userebbe informazione che allora non c'era. Se la giornata non è ancora consegnata
# esce: lo studio lo userà il run normale.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

MODEL="claude-opus-5-5"
EFFORT="high"
RUN_MAX=${RUN_MAX:-1800}
NEWSDIR="$HOME/Claude/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
DAILY="$NEWSDIR/daily_analysis"
LOGDIR="$PIPE/logs"
CLAUDE=${CLAUDE:-/opt/homebrew/bin/claude}
TODAY=$(date +%Y-%m-%d)
DAY="$DAILY/$TODAY"
LOG="$LOGDIR/rianalisi-${TODAY}.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }
avvisa() { /usr/bin/osascript -e "display notification \"$1\" with title \"News-Impact Pipeline\" sound name \"Basso\"" 2>/dev/null; }

MODO=kb
[[ "${1:-}" == --versi ]] && { MODO=versi; shift; }
(( $# )) || { echo "uso: run_rianalisi_kb.sh [--versi] <studio|proposta> [...]"; exit 2; }
mkdir -p "$LOGDIR"
log "START: rianalisi ($MODO) per: $*"

# --- Cancelli --------------------------------------------------------------
# Consegnata con lo stesso brief e ritoccata dopo l'invio (una lacuna annotata, una
# correzione a mano) conta come consegnata: è la regola del run giornaliero. Il
# 2026-11-02 una precisazione in _index.md ha fatto saltare la rianalisi BCE.
FASE=$("$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --json 2>>"$LOG" | "$PY" -c '
import json, sys
s = json.load(sys.stdin)
f = s["fase"] or "completa"
dopo_invio = f in ("html_prodotto", "consegna_confermata") and s["input_riconosciuto"] and s.get("consegnato")
print("completa" if dopo_invio else f)' 2>>"$LOG")
if [[ "$FASE" != "completa" ]]; then
  log "SKIP: giornata $TODAY non consegnata (ferma su ${FASE:-?}): lo studio entra nel run normale."
  exit 0
fi
FOTO=$("$PY" -c 'import json,sys; m=json.load(open(sys.argv[1])); print(m["db"]); print(m["scorecard"])' \
  "$DAY/_mattino.json" 2>>"$LOG")
DBM="${FOTO%%$'\n'*}"; SCORECARD="${FOTO#*$'\n'}"
if [[ -z "$FOTO" || ! -f "$DBM" ]]; then
  log "SKIP: manca la fotografia del mattino di $TODAY (_mattino.json o copia dei prezzi): niente rianalisi senza dati congelati."
  exit 0
fi

# Stesso lock del run giornaliero: i due non scrivono mai insieme nella giornata.
LOCK="$LOGDIR/.lock"
for i in {1..60}; do
  pid=$(cat "$LOCK/pid" 2>/dev/null)
  # Relitto di un processo morto (o lock senza pid): si toglie, come fa il giornaliero.
  [[ -d "$LOCK" ]] && { [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null } && rm -rf "$LOCK"
  mkdir "$LOCK" 2>/dev/null && break
  (( i == 60 )) && { log "SKIP: run giornaliero ancora in corso dopo 10 minuti."; exit 1; }
  sleep 10
done
print -r -- $$ > "$LOCK/pid"
# L'etichetta si prende DOPO il lock: due promozioni di fila lanciano due rianalisi
# nello stesso minuto, e con l'etichetta presa prima la seconda sovrascriveva il
# riassunto della prima (2026-11-04).
TAG="rev$(date +%H%M)"
log "Etichetta $TAG."
trap 'rm -rf "$LOCK"' EXIT

# --- Libreria con il nuovo studio, impronte prima -------------------------
"$PY" "$PIPE/analogues.py" build >> "$LOG" 2>&1 || { log "ERROR: analogues build fallito."; exit 1; }
typeset -A PRIMA
for f in "$DAY"/news_*.md(N); do PRIMA[${f:t}]=$(shasum "$f" | cut -c1-12); done

if [[ $MODO == versi ]]; then
  # Voci promosse (data, tema, asset, verso) e schede di oggi dello stesso tema che
  # citano l'asset: il perimetro si decide qui, non lo sceglie l'agente.
  VOCI=$("$PY" "$PIPE/recupero.py" voci "$@" 2>>"$LOG")
  SCHEDE=$("$PY" "$PIPE/recupero.py" schede "$DAY" "$@" 2>>"$LOG")
  if [[ -z "$SCHEDE" ]]; then
    log "DONE: nessuna scheda di oggi usa i versi rivisti."
    exit 0
  fi
  log "Perimetro versi: ${(j:, :)${(f)SCHEDE}}."
  read -r -d '' TESTA <<EOF
RIANALISI DOPO UNA REVISIONE DEI VERSI — giornata $TODAY, già analizzata e consegnata stamattina.

Nel registro _direction_reviews.yaml sono appena entrate, approvate dal maintainer,
queste dichiarazioni (data tema asset: verso; "escluso" toglie la coppia dai pool):
$VOCI

Domanda: che cosa avrebbe scritto il run di stamattina se queste dichiarazioni fossero
già state nel registro? L'unica cosa nuova sono loro: tutto il resto della scheda
(classificazione, KB, regime, scenari, considerazioni qualitative, caveat) resta com'è,
salvo ciò che dipende dai numeri del pool.

Perimetro (vincolante): SOLO queste schede, già individuate:
$(printf '  - %s\n' ${(f)SCHEDE})
Per ciascuna rilancia i suoi analogues.py find (stessi argomenti, sempre --before
$TODAY) e i suoi event_study.py. Se il pool non cambia, non toccare la scheda. Se
cambia, riscrivila nello stesso file e con lo stesso slug, aggiornando solo pool, N,
potature, event study e la lettura che ne discende; nient'altro. Non toccare le altre
schede, le righe di triage né il digest. L'originale è già in _forecast_sources/.
EOF
  NOTA="**Aggiornamento dopo la revisione dei versi (${TAG#rev}).**"
  TITOLO="dopo la revisione dei versi"
else
  STUDI="$(printf '  - %s\n' "$@")"
  read -r -d '' TESTA <<EOF
RIANALISI DOPO UNA NUOVA RESEARCH — giornata $TODAY, già analizzata e consegnata stamattina.

Nella Knowledge Base sono appena stati indicizzati questi studi:
$STUDI

Domanda: che cosa avrebbe scritto il run di stamattina se questi studi fossero già
esistiti? Rispondi SOLO per le notizie di oggi che gli studi servono davvero.

Perimetro (vincolante):
1) Leggi $DAY/_index.md (triage, Sintesi, Lacune emerse) e gli studi elencati.
   Individua le righe di triage che questi studi servono: lo stesso tema e sotto-tema,
   gli stessi asset, o la lacuna che chiudono. Se nessuna, non modificare nulla e dillo.
2) Riga scartata (✖) che ora ha un pool direzionale o descrittivo utile: crea la scheda
   con il flusso completo del runbook $PIPE/PHASE5_RUNBOOK.md (assets, match, new-card,
   analogues, event_study, sezioni qualitative) e aggiorna la riga di triage.
3) Riga già coperta da una scheda: riscrivi QUELLA scheda nello stesso file e con lo
   stesso slug, cambiando solo ciò che lo studio cambia (pool, event study, lettura).
   L'originale è già conservato in _forecast_sources/: non copiarlo altrove.
4) Non toccare le altre righe di triage né le altre schede; non rigenerare il digest.
EOF
  NOTA="**Aggiornamento dopo la research (${TAG#rev}).**"
  TITOLO="dopo una nuova research"
fi

read -r -d '' PROMPT <<EOF
$TESTA

Dati congelati al brief (vincolante):
- Fonti: il brief di stamattina ($NEWSDIR/morning brief/${TODAY}-morning-briefing.html),
  la KB e i tool della pipeline. Nient'altro: nessuna notizia, prezzo o commento
  successivo al brief, nemmeno se lo conosci.
- I prezzi sono già la copia del mattino (variabile NEWSIMPACT_DB, la leggono tutti i
  tool): non aprire market_data/market_data.db direttamente.
- Scorecard: usa SOLO $SCORECARD, non una più recente.
- analogues.py find sempre con --before $TODAY; event_study.py con --as-of $TODAY.

Chiusura:
- In _index.md aggiungi in coda alla Sintesi di sessione un paragrafo "$NOTA"
  con cosa è cambiato e perché. Una lacuna che ora è chiusa, se non è già segnata,
  va segnata in "Lacune emerse" con N per verso e ticker e con l'etichetta
  \`#lacuna <slug> stato=chiusa\` (slug della lacuna, da venv/bin/python lacune.py).
- Scrivi in $DAY/_rianalisi_${TAG}.md un riassunto per il telefono, max 8 righe,
   senza tabelle: quali notizie, scheda nuova o rifatta, cosa dice ora il pool
   (N, verso, INDICATIVE ONLY se N<10) rispetto a stamattina.

Valgono tutte le regole del runbook: verso = pressione attesa sul prezzo, N sempre
riportato, scorecard letta prima della lettura direzionale, [descrittiva] se il segno
non regge. ECONOMIA DEL RUN: raccogli tutto prima di scrivere, un passaggio per file,
Edit chirurgico per le correzioni, niente --help. Lavora in $DAY/.
EOF

# --- Agente, con watchdog --------------------------------------------------
/bin/zsh "$PIPE/attendi_rete.sh" >/dev/null || log "WARN: API non raggiungibile, lancio comunque."
log "Lancio Claude Code headless (model=$MODEL, effort=$EFFORT, prezzi ${DBM:t}, scorecard ${SCORECARD:t}, tetto ${RUN_MAX}s)."
cd "$NEWSDIR"
RAW="$LOGDIR/.raw_rianalisi_${TODAY}.json"
NEWSIMPACT_DB="$DBM" "$CLAUDE" -p "$PROMPT" --model "$MODEL" --effort "$EFFORT" \
  --permission-mode bypassPermissions --strict-mcp-config --disallowedTools WebSearch WebFetch \
  --output-format json </dev/null > "$RAW" 2>>"$LOG" &
PID_HEADLESS=$!
( t=0; while (( t < RUN_MAX )); do sleep 1; t=$((t+1)); kill -0 $PID_HEADLESS 2>/dev/null || exit 0; done
  kill -TERM $PID_HEADLESS 2>/dev/null ) &
PID_GUARDIANO=$!
wait $PID_HEADLESS
RC=$?
kill $PID_GUARDIANO 2>/dev/null
log "Claude exit code $RC."
"$PY" "$PIPE/record_claude_usage.py" "$RAW" "$LOG" "$LOGDIR/usage.csv" "$TODAY" rianalisi "$MODEL" \
  || log "WARN: parsing usage fallito."
rm -f "$RAW"

# --- Cosa è cambiato --------------------------------------------------------
CAMBIATE=()
for f in "$DAY"/news_*.md(N); do
  sha=$(shasum "$f" | cut -c1-12)
  if [[ -z "${PRIMA[${f:t}]:-}" ]]; then CAMBIATE+=("nuova ${f:t}")
  elif [[ "${PRIMA[${f:t}]}" != "$sha" ]]; then CAMBIATE+=("rifatta ${f:t}"); fi
done
if (( ! ${#CAMBIATE} )); then
  log "DONE: nessuna scheda toccata (niente di nuovo per le notizie di oggi)."
  exit 0
fi
log "Schede: ${(j:, :)CAMBIATE}."

FASE=$("$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --fase 2>>"$LOG")
if [[ "$FASE" == "triage_completato" || "$FASE" == "schede_validate" ]]; then
  MSG="rianalisi $TODAY: le schede rifatte non passano la validazione ($FASE). Niente registrazione né invio: stato_giornata.py --date $TODAY"
  log "ERROR: $MSG"; avvisa "$MSG"; exit 1
fi

"$PY" "$PIPE/forecast_tracking.py" register --date "$TODAY" --revisione "$TAG" >> "$LOG" 2>&1 \
  || { log "WARN: registrazione $TAG parziale o fallita."; avvisa "rianalisi $TODAY: registrazione previsioni parziale, vedi log"; }
"$PY" "$PIPE/render_report.py" --date "$TODAY" >> "$LOG" 2>&1 || log "WARN: render_report.py fallito."

# --- Aggiornamento breve su Telegram -----------------------------------------
TESTO="🔁 Analisi $TODAY aggiornata $TITOLO"$'\n'
for c in "${CAMBIATE[@]}"; do
  TESTO+="• ${c%% *} ${c#* }: $(sed -n 's/^# //p' "$DAY/${c#* }" | head -1)"$'\n'
done
[[ -f "$DAY/_rianalisi_${TAG}.md" ]] && TESTO+=$'\n'"$(cat "$DAY/_rianalisi_${TAG}.md")"
if /bin/zsh "$PIPE/send_telegram.sh" --messaggio "$TESTO" >> "$LOG" 2>&1; then
  # Il report sul disco è cambiato: la ricevuta lo riallinea, altrimenti la giornata
  # risulterebbe "rigenerata dopo l'invio".
  "$PY" "$PIPE/stato_giornata.py" --date "$TODAY" --registra-consegna ok >> "$LOG" 2>&1
else
  log "WARN: aggiornamento Telegram non inviato."
fi
log "DONE."
