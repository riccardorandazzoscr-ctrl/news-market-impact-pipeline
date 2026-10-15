#!/bin/zsh
# attendi_rete.sh — aspetta che l'API risponda, poi esce.
#
# Perché esiste: dal 12/10/2026 il run delle 08:15 falliva ogni mattina con ENOTFOUND
# (il Mac non aveva ancora la rete) e si arrendeva alla prima prova. Qui si aspetta.
#
# Exit 0 appena l'host risponde (stampa i secondi attesi), 1 se non risponde entro
# ATTESA_RETE_MAX. Vale qualsiasi risposta HTTP: il 404 della radice è normale, conta
# solo che DNS e connessione funzionino. Chi chiama decide cosa fare del fallimento.
MAX=${ATTESA_RETE_MAX:-900}
STEP=${ATTESA_RETE_STEP:-15}
URL=${RETE_URL:-https://api.anthropic.com}
waited=0
until /usr/bin/curl -s -m 5 -o /dev/null "$URL"; do
  (( waited >= MAX )) && exit 1
  sleep "$STEP"; waited=$(( waited + STEP ))
done
print -r -- "$waited"
