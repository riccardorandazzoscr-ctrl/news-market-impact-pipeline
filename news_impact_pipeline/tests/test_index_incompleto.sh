#!/bin/zsh
# Test del guardiano sulla COMPLETEZZA dell'analisi in run_daily_analysis.sh
# (guasto dell'11/09/2026: limite di sessione a metà run, scheletro di _index.md
# scambiato per un successo e spedito su Telegram senza un allarme).
#
#   ./tests/test_index_incompleto.sh
#
# COME FUNZIONA, e cosa NON copre.
# Lo script sotto test gira in un $HOME finto, in due copie:
#   run.sh     — troncata dopo `log "START..."`, come nella suite del briefing:
#                copre idempotenza, riconoscimento dello scheletro e archiviazione
#                del parziale, che stanno tutti sopra quel punto.
#   run_fin.sh — identica all'originale TRANNE il blocco della chiamata a Claude
#                headless (da `log "Lancio..."` a `rm -f`), sostituito da uno stub
#                che scrive un _index.md a scelta e imposta il codice di uscita.
#                Serve a far arrivare il controllo al ramo finale — quello che
#                decide fra fallimento, run monco e successo — senza spendere i
#                ~6 dollari di un run vero. Tutto il resto è codice reale.
# Le altre dipendenze (venv, index_studies.sh, send_telegram.sh) sono stub dentro
# la sandbox; `render_report.py` è finto, quindi il contenuto del report non è sotto
# test — solo il fatto che venga prodotto e spedito.
#
# ⚠ I casi sul ramo finale fanno comparire DAVVERO una notifica sul desktop:
# `osascript` è chiamato per percorso assoluto e non si può sostituire. È il
# comportamento sotto test, non un effetto collaterale.

set -u
PIPE="${0:A:h:h}"
SCRIPT="$PIPE/run_daily_analysis.sh"
INDEX_REALI="$HOME/Claude/mercati_finanza/daily_analysis"
PASS=0; FAIL=0

ok()  { print -r -- "  ✓ $1"; PASS=$((PASS+1)); }
ko()  { print -r -- "  ✗ $1"; print -r -- "      $2"; FAIL=$((FAIL+1)); }
check() { if eval "$1"; then ok "$2"; else ko "$2" "${3:-condizione non soddisfatta: $1}"; fi }

# ---------------------------------------------------------------- ambiente finto
setup() {
  SANDBOX=$(mktemp -d)
  export FAKE_HOME="$SANDBOX/home"
  BDIR="$FAKE_HOME/Claude/morning brief"
  DAILY="$FAKE_HOME/Claude/mercati_finanza/daily_analysis"
  FPIPE="$FAKE_HOME/Claude/mercati_finanza/news_impact_pipeline"
  mkdir -p "$BDIR" "$DAILY" "$FPIPE/logs" "$FPIPE/venv/bin"

  GIORNO="2026-09-11"
  BRIEF="$BDIR/${GIORNO}-morning-briefing.html"
  LOG="$FPIPE/logs/${GIORNO}.log"
  GIORNODIR="$DAILY/$GIORNO"
  TELEGRAM="$FPIPE/logs/telegram.txt"

  # copia troncata dopo lo START (idempotenza, ripresa, archiviazione)
  awk '/^log "START/ { print; print "exit 0"; exit } { print }' \
      "$SCRIPT" > "$FPIPE/run.sh"

  # copia con la sola chiamata a Claude sostituita da uno stub pilotabile
  cat > "$SANDBOX/stub.zsh" <<'STUB'
log "Lancio Claude Code headless (STUB DI TEST)."
[[ -n "${STUB_LOG:-}" ]] && print -r -- "$STUB_LOG" >> "$LOG"
if [[ -n "${STUB_INDEX:-}" ]]; then
  mkdir -p "$DAILY/$TODAY"
  cp "$STUB_INDEX" "$INDEX"
fi
for n in $(seq 1 ${STUB_SCHEDE:-0}); do
  print -r -- "# scheda finta $n" > "$DAILY/$TODAY/news_0${n}.md"
done
RC=${STUB_RC:-0}
log "Claude exit code $RC."
STUB
  awk -v stubf="$SANDBOX/stub.zsh" '
    /^log "Lancio Claude Code headless/ { while ((getline l < stubf) > 0) print l; salta=1; next }
    /^rm -f / { salta=0; next }
    !salta { print }
  ' "$SCRIPT" > "$FPIPE/run_fin.sh"
  chmod +x "$FPIPE/run.sh" "$FPIPE/run_fin.sh"

  # --- dipendenze finte ---
  cat > "$FPIPE/venv/bin/python" <<'PYSTUB'
#!/bin/zsh
case "$*" in
  *render_report.py*)
    R="$HOME/Claude/mercati_finanza/daily_analysis/$3"
    mkdir -p "$R"; print -r -- "<html>report finto $3</html>" > "$R/report.html" ;;
  -) print 99 ;;          # controllo salute DB (heredoc su stdin)
  *) : ;;                 # analogues.py build & co.
esac
exit 0
PYSTUB
  cat > "$FPIPE/index_studies.sh" <<'IDX'
#!/bin/zsh
exit 0
IDX
  cat > "$FPIPE/send_telegram.sh" <<'TG'
#!/bin/zsh
print -r -- "TELEGRAM $*" >> "$HOME/Claude/mercati_finanza/news_impact_pipeline/logs/telegram.txt"
exit 0
TG
  chmod +x "$FPIPE/venv/bin/python" "$FPIPE/index_studies.sh" "$FPIPE/send_telegram.sh"

  scrivi_brief 20
}
teardown() { [[ -n "${SANDBOX:-}" ]] && rm -rf "$SANDBOX"; }

scrivi_brief() {
  { print -r -- "<html><head><title>Morning Briefing</title></head><body>"
    for i in $(seq 1 ${1:-20}); do
      print -r -- "<div class=\"story\"><h3>Notizia $i</h3></div>"
    done
    print -r -- "</body></html>"
  } > "$BRIEF"
}

# --- i tre stati di _index.md ------------------------------------------------
# Lo SCHELETRO è quello vero dell'11/09: righe di triage a ⏳ e Sintesi da compilare.
scrivi_index() {
  mkdir -p "$GIORNODIR"
  case "$1" in
    scheletro)
      { print -r -- "# Daily Analysis — $GIORNO"
        print -r -- "| # | Sez. | Notizia | Decisione | Tema | Scheda |"
        print -r -- "|---|------|---------|-----------|------|--------|"
        for i in $(seq 1 20); do print -r -- "| 0$i | fin | Notizia $i | ⏳ | | |"; done
        print -r -- "## Sintesi di sessione"
        print -r -- "_(nota dell'analista: temi dominanti del giorno. Da compilare dopo il triage.)_"
      } > "$GIORNODIR/_index.md" ;;
    sintesi-vuota)   # triage fatto, ma il run è morto prima della sintesi (19/07, 31/07)
      { print -r -- "# Daily Analysis — $GIORNO"
        print -r -- "| 01 | fin | Notizia | ✅ | inflazione | news_01.md |"
        print -r -- "## Sintesi di sessione"
        print -r -- "_(nota dell'analista: temi dominanti del giorno. Da compilare dopo il triage.)_"
      } > "$GIORNODIR/_index.md" ;;
    completo)
      { print -r -- "# Daily Analysis — $GIORNO"
        print -r -- "| 01 | fin | Notizia | ✅ | inflazione | news_01.md |"
        print -r -- "## Sintesi di sessione"
        print -r -- "Il tema dominante del giorno è stato l'inflazione."
      } > "$GIORNODIR/_index.md" ;;
  esac
}

run_sut()     { ( HOME="$FAKE_HOME" WAIT_MAX=1 WAIT_STEP=1 /bin/zsh "$FPIPE/run.sh" "$GIORNO" >/dev/null 2>&1 ); echo $?; }
run_finale()  { ( HOME="$FAKE_HOME" WAIT_MAX=1 WAIT_STEP=1 \
                  STUB_RC="${1:-0}" STUB_INDEX="${2:-}" STUB_SCHEDE="${3:-0}" STUB_LOG="${4:-}" \
                  /bin/zsh "$FPIPE/run_fin.sh" "$GIORNO" >/dev/null 2>&1 ); echo $?; }

print -r -- "=============================================================="
print -r -- "TEST — guardiano sulla completezza dell'analisi"
print -r -- "=============================================================="

# ---------------------------------------------------------------- 0. sintassi
print -- "\n0. Sintassi degli script INTERI (non solo la parte testata)"
setup
for s in "$SCRIPT" "$PIPE/send_telegram.sh"; do
  if zsh -n "$s" 2>/dev/null; then ok "${s:t}: sintassi valida"
  else ko "${s:t}: sintassi valida" "zsh -n fallisce"; fi
done
check "grep -c '^log \"Lancio Claude Code headless' '$SCRIPT' | grep -q '^1$'" \
      "lo stub dei test aggancia un marcatore unico (^log \"Lancio...)"
check "grep -c '^rm -f ' '$SCRIPT' | grep -q '^1$'" \
      "lo stub dei test chiude su un marcatore unico (^rm -f)"
teardown

# ------------------------------------------------- 1. idempotenza solo se completa
print -- "\n1. Analisi COMPLETA già presente → si esce, come prima"
setup
scrivi_index completo
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "esce con 0" "rc=$RC"
check "grep -q 'SKIP: analisi' '$LOG'" "logga SKIP"
check "! grep -q 'RIPRESA\|START' '$LOG'" "non rifà nulla"
check "[[ -f '$GIORNODIR/_index.md' ]]" "non tocca l'analisi esistente"
teardown

# ---------------------------------------------------------------- 2. lo scheletro
print -- "\n2. Scheletro di triage (il guasto dell'11/09) → NON è un'analisi fatta"
setup
scrivi_index scheletro
print -r -- "# scheda vera" > "$GIORNODIR/news_01.md"
RC=$(run_sut)
check "[[ $RC -eq 0 ]]" "prosegue invece di uscire" "rc=$RC"
check "! grep -q 'SKIP: analisi' '$LOG'" "NON logga SKIP (era il blocco dell'11/09 alle 10:07)"
check "grep -q 'RIPRESA' '$LOG'" "logga RIPRESA"
check "grep -q 'START' '$LOG'" "arriva ad avviare una nuova analisi"
teardown

# ------------------------------------------------------ 3. sintesi non compilata
print -- "\n3. Triage fatto ma Sintesi mai compilata (19/07 e 31/07) → incompleta"
setup
scrivi_index sintesi-vuota
RC=$(run_sut)
check "grep -q 'RIPRESA' '$LOG'" "riconosce anche questa forma di run monco"
check "grep -q 'START' '$LOG'" "rifà il giorno"
teardown

# ------------------------------------------------------- 4. archiviazione parziale
print -- "\n4. Il parziale si archivia, non si cancella e non si sovrascrive"
setup
scrivi_index scheletro
print -r -- "# scheda vera 1" > "$GIORNODIR/news_01.md"
print -r -- "# scheda vera 2" > "$GIORNODIR/news_02.md"
RC=$(run_sut)
ARCHIVI=("$GIORNODIR"/_interrotto_*(N/))
check "[[ ${#ARCHIVI} -eq 1 ]]" "crea una cartella _interrotto_<ora>/" "trovate: ${#ARCHIVI}"
check "[[ -f '${ARCHIVI[1]}/_index.md' ]]" "ci sposta dentro lo scheletro"
check "[[ -f '${ARCHIVI[1]}/news_01.md' && -f '${ARCHIVI[1]}/news_02.md' ]]" "ci sposta dentro le schede"
check "[[ ! -f '$GIORNODIR/_index.md' ]]" "il giorno riparte da una cartella pulita"
NEWS=("$GIORNODIR"/news_*.md(N))
check "[[ ${#NEWS} -eq 0 ]]" "nessuna scheda orfana nel glob di render/analogues" "rimaste: ${#NEWS}"
teardown

# ---------------------------------------- 5. ramo finale: run interrotto a metà
print -- "\n5. Claude si ferma a metà (limite di sessione) → allarme, non silenzio"
setup
scrivi_index scheletro                      # lo stub lo userà come output di Claude
cp "$GIORNODIR/_index.md" "$SANDBOX/scheletro.md"
rm -rf "$GIORNODIR"
RC=$(run_finale 1 "$SANDBOX/scheletro.md" 6 "You've hit your session limit · resets 12:40pm (Europe/Rome)")
check "[[ $RC -eq 1 ]]" "esce con codice 1" "rc=$RC"
check "grep -q 'ERROR' '$LOG'" "logga ERROR"
check "grep -q 'INCOMPLETA' '$LOG'" "dice che l'analisi è incompleta"
check "grep -q 'limite di sessione' '$LOG'" "riconosce la causa"
check "grep -q '12:40pm' '$LOG'" "riporta quando si azzera il limite"
check "grep -q '6 schede' '$LOG'" "conta le schede salvate dal parziale"
check "grep -q 'run_daily_analysis.sh $GIORNO' '$LOG'" "suggerisce come rilanciare"
check "! grep -q 'DONE' '$LOG'" "NON si dichiara completato"
check "! grep -q 'WARN: Claude exit' '$LOG'" "non è più il WARN silenzioso di prima"
check "[[ -f '$GIORNODIR/report.html' ]]" "il lavoro parziale viene comunque renderizzato"
check "grep -q -- '--parziale' '$TELEGRAM'" "Telegram avvisa che il report è incompleto"
teardown

# ------------------------------------------------- 6. ramo finale: giorno riuscito
print -- "\n6. Run completo → nessun falso allarme"
setup
scrivi_index completo
cp "$GIORNODIR/_index.md" "$SANDBOX/completo.md"
rm -rf "$GIORNODIR"
RC=$(run_finale 0 "$SANDBOX/completo.md" 3)
check "[[ $RC -eq 0 ]]" "esce con 0" "rc=$RC"
check "grep -q 'DONE' '$LOG'" "logga DONE"
check "! grep -q 'ERROR\|INCOMPLETA' '$LOG'" "nessun allarme"
check "grep -q 'TELEGRAM $GIORNO$' '$TELEGRAM'" "Telegram con la didascalia normale"
teardown

# --------------------------- 7. ramo finale: exit≠0 ma lavoro finito (10/07/2026)
print -- "\n7. Exit ≠0 a lavoro già scritto → resta un successo (regressione 10/07)"
setup
scrivi_index completo
cp "$GIORNODIR/_index.md" "$SANDBOX/completo.md"
rm -rf "$GIORNODIR"
RC=$(run_finale 1 "$SANDBOX/completo.md" 3)
check "[[ $RC -eq 0 ]]" "il giorno non si butta via" "rc=$RC"
check "grep -q 'WARN: Claude exit 1' '$LOG'" "logga il WARN"
check "grep -q 'DONE' '$LOG'" "arriva in fondo"
check "! grep -q -- '--parziale' '$TELEGRAM'" "Telegram con la didascalia normale"
teardown

# ------------------------------------------- 8. ramo finale: _index.md mai scritto
print -- "\n8. Claude muore prima di scrivere (regressione: 401, 529, 10/07)"
setup
RC=$(run_finale 1 "" 0 "You've hit your session limit · resets 8pm (Europe/Rome)")
check "[[ $RC -eq 1 ]]" "esce con 1" "rc=$RC"
check "grep -q 'FALLITO\|limite di sessione' '$LOG'" "logga il fallimento pieno"
check "grep -q 'Invio su Telegram del solo briefing' '$LOG'" "manda comunque il brief grezzo"
teardown

# ------------------------------------- 9. regressione sui 105 _index.md reali
print -- "\n9. Regressione: l'archivio vero passa per lo script vero"
# Ogni file passa per lo SCRIPT, non per una ri-scrittura del controllo: un test che
# ricopia la condizione verificherebbe la mia assunzione, non il codice. I 3 giorni
# rotti noti (19/07, 31/07, 11/09) devono essere riconosciuti monchi, gli altri sani.
setup
ROTTI_ATTESI=(2026-07-19 2026-07-31 2026-09-11)
tot=0; sani=0; monchi=(); falsi_allarmi=()
for f in "$INDEX_REALI"/2026-*/_index.md(N); do
  giorno="${${f:h}:t}"
  mkdir -p "$GIORNODIR"; cp "$f" "$GIORNODIR/_index.md"; rm -f "$LOG"
  tot=$((tot+1))
  if [[ "$(run_sut)" -eq 0 ]] && grep -q 'SKIP: analisi' "$LOG"; then
    sani=$((sani+1))
    (( ${ROTTI_ATTESI[(Ie)$giorno]} )) && falsi_allarmi+=("$giorno accettato ma è rotto")
  else
    monchi+=("$giorno")
    (( ${ROTTI_ATTESI[(Ie)$giorno]} )) || falsi_allarmi+=("$giorno respinto ma è sano")
  fi
  rm -rf "$GIORNODIR"
done
check "[[ $tot -gt 100 ]]" "archivio trovato ($tot file)"
check "[[ ${#falsi_allarmi} -eq 0 ]]" "nessun falso positivo né falso negativo" "${falsi_allarmi[*]}"
check "[[ ${#monchi} -eq ${#ROTTI_ATTESI} ]]" \
      "riconosce esattamente i ${#ROTTI_ATTESI} run monchi noti: ${monchi[*]}" \
      "attesi ${ROTTI_ATTESI[*]}, trovati ${monchi[*]}"
check "[[ $sani -eq $((tot - ${#monchi})) ]]" "gli altri $sani sono accettati come completi"
teardown

print -- "\n=============================================================="
print -r -- "PASSATI: $PASS   ·   FALLITI: $FAIL"
print -r -- "=============================================================="
exit $(( FAIL > 0 ? 1 : 0 ))
