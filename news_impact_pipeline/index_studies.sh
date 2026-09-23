#!/bin/zsh
# index_studies.sh — auto-indicizzazione YAML degli studi della Knowledge Base
# (Fase 2 / Variante B). Lanciato da launchd via WatchPaths su knowledge_base/,
# e anche come backstop dal run giornaliero (Variante A) per coprire il caso in
# cui un file venga aggiunto DENTRO una sottocartella già esistente (che i
# WatchPaths su una dir non sempre rilevano).
#
# Cosa fa:
#   - scopre le sottocartelle-studio NON ancora indicizzate (= nessun .md con
#     blocco ```yaml in fondo) ma che contengono materiale sorgente
#   - se ce ne sono, lancia Claude Code headless con un prompt che legge la
#     ricerca (anche da PDF), accoda il blocco YAML canonico §5.2 e rilancia
#     build_catalog.py
#   - idempotente: se non trova studi non indicizzati esce subito (no-op),
#     quindi il ri-trigger causato dalla scrittura di catalog.yaml non cicla.

set -u
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# --- Configurazione --------------------------------------------------------
MODEL="claude-opus-5-5"   # stesso modello del run giornaliero
PROJECT="$HOME/Claude"
NEWSDIR="$PROJECT/mercati_finanza"
PIPE="$NEWSDIR/news_impact_pipeline"
PY="$PIPE/venv/bin/python"
KB="$NEWSDIR/knowledge_base"
LOGDIR="$PIPE/logs"
CLAUDE="/opt/homebrew/bin/claude"

mkdir -p "$LOGDIR"
LOG="$LOGDIR/index_studies.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

if [[ ! -d "$KB" ]]; then
  log "ERRORE: KB non trovata ($KB). Esco."
  exit 0
fi

# --- Scoperta studi non indicizzati ----------------------------------------
# La domanda «cosa manca all'indice, e il catalogo è stale?» la risponde
# build_catalog --scan, cioè chi possiede la regola. Prima la rispondeva questo
# script per conto suo, e divergeva dal builder su tre punti: marcava
# indicizzata un'INTERA cartella se un qualsiasi .md conteneva un fence ```yaml
# (anche invalido, e anche con un secondo studio non indicizzato accanto);
# cercava a un solo livello mentre il builder è ricorsivo; e rilevava lo
# staleness per sola mtime, quindi una research RIMOSSA o RINOMINATA lasciava
# la sua voce nel catalogo per sempre. Ora lo staleness è per contenuto.
#
# build_catalog riscrive catalog.yaml (che diventa il più recente e allineato)
# → al ri-trigger del WatchPath nulla risulta stale → no-op → nessun loop.
setopt NULL_GLOB
SCAN_OUT="$( cd "$PIPE" && "$PY" build_catalog.py --scan )" || {
  log "ERROR: build_catalog --scan fallito."
  exit 1
}
stale=0
UNINDEXED=()
while IFS= read -r riga; do
  case "$riga" in
    STALE=1)     stale=1 ;;
    UNINDEXED=*) UNINDEXED+=("${riga#UNINDEXED=}") ;;
  esac
done <<< "$SCAN_OUT"
CATALOG="$KB/catalog.yaml"

if (( ${#UNINDEXED[@]} == 0 )); then
  if (( stale )); then
    log "Nessuno studio da generare, ma catalog stale → rebuild build_catalog.py."
    ( cd "$PIPE" && "$PY" build_catalog.py ) >> "$LOG" 2>&1 || {
      log "ERROR: build_catalog fallito."
      exit 1
    }
    log "build_catalog rieseguito. DONE."
  else
    log "SKIP: nessuno studio non indicizzato e catalog aggiornato. No-op."
  fi
  exit 0
fi

# --- Lock (evita doppio run watchpath + backstop giornaliero) --------------
LOCK="$LOGDIR/.lock_index"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP: altro run di indicizzazione in corso (lock presente)."
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "START: studi da indicizzare → ${UNINDEXED[*]}"

# --- Prompt per l'agente ---------------------------------------------------
LIST="$(printf '%s\n' "${UNINDEXED[@]}")"
read -r -d '' PROMPT <<EOF
Indicizza i seguenti studi appena caricati nella Knowledge Base, ciascuno nella
propria sottocartella sotto $KB:

$LIST

Per OGNI studio nell'elenco:
1) Leggi il materiale sorgente nella sua cartella (PDF, .md, .html, .txt).
   Comprendi tema, fasi di regime, asset e
   meccanismi di trasmissione descritti.
2) Individua il file markdown della ricerca scritto dal maintainer. Se non esiste,
   segnala la lacuna e NON scrivere una ricerca o un prompt al suo posto.
3) Accoda IN FONDO a quel .md il blocco metadata YAML canonico (Design Document
   §5.2), dentro un fence \`\`\`yaml. Campi obbligatori: title, date_compiled
   (oggi), primary_theme, sub_themes, relevant_assets, time_window
   (start/end), regime_phases (lista "fase: AAAA-MM-GG to AAAA-MM-GG"),
   keywords. Vincoli:
   - primary_theme DEVE essere uno dei 9 temi dell'ontologia §6.1:
     monetary_policy, fiscal_policy, geopolitical, macro_data,
     corporate_idiosyncratic, regulatory, commodity_energy,
     financial_stability, structural_themes.
   - relevant_assets DEVE usare SOLO ticker presenti nella tabella assets del DB
     $NEWSDIR/market_data/market_data.db. Interroga il DB, non usare una lista fissa.
     Eventuali asset citati ma non in DB vanno in un campo extra
     external_assets_mentioned (lista descrittiva), NON in relevant_assets.
   - Usa come riferimento di stile il blocco già presente in
     sovereign_debt/sovereign_debt_crisis.md.
4) Quando hai indicizzato tutti gli studi, esegui dalla cartella $PIPE:
   venv/bin/python build_catalog.py
   e verifica che il report finisca con 0 warning per i nuovi studi (correggi i
   campi se compaiono warning su primary_theme o asset non in DB).
Output finale in chat: per ogni studio, lo slug, il primary_theme assegnato e
gli asset rilevanti; più la riga di riepilogo del catalog (n. entries, warning).
EOF

log "Lancio Claude Code headless (model=$MODEL)."
cd "$NEWSDIR"
"$CLAUDE" -p "$PROMPT" --model "$MODEL" --permission-mode bypassPermissions \
  </dev/null >> "$LOG" 2>&1
RC=$?
log "Claude exit code $RC."
if (( RC != 0 )); then
  log "ERROR: indicizzazione incompleta."
  exit "$RC"
fi
log "DONE."
exit 0
