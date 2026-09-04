#!/bin/bash
# Esegue tutte le suite di test del progetto. Un solo comando, un solo esito.
#
#   ./run_tests.sh              # tutto
#   ./run_tests.sh asset        # solo l'universo asset
#   ./run_tests.sh analogues    # solo il filtro sotto-tema di analogues.py
#
# I test sono NON distruttivi: leggono il DB e lanciano i tool in sola lettura.
# L'unica eccezione è `update_market_data.py`, rilanciato per verificare che sia
# idempotente — cioè che NON aggiunga righe se non ce ne sono di nuove.
set -uo pipefail
cd "$(dirname "$0")"
V=venv/bin/python
FILTRO="${1:-tutto}"
FALLITE=0

run() {   # run <etichetta> <file> [args...]
  echo
  echo "############################################################"
  echo "# $1"
  echo "############################################################"
  if $V "$2" "${@:3}"; then
    echo "→ $1: OK"
  else
    echo "→ $1: FALLITA"
    FALLITE=$((FALLITE + 1))
  fi
}

[ "$FILTRO" = "tutto" ] || [ "$FILTRO" = "analogues" ] && \
  run "analogues.py — filtro sotto-tema (unione vs --match-all)" \
      tests/test_analogues_match_all.py

[ "$FILTRO" = "tutto" ] || [ "$FILTRO" = "asset" ] && \
  run "universo asset — registro, dati, mappa, integrazione, regressione" \
      tests/test_asset_universe.py

echo
echo "============================================================"
if [ "$FALLITE" -eq 0 ]; then
  echo "TUTTE LE SUITE VERDI"
else
  echo "SUITE FALLITE: $FALLITE"
fi
echo "============================================================"
exit "$FALLITE"
