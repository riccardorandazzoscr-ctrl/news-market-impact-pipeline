#!/usr/bin/env python3
"""Nessun job lancia `claude -p` senza spegnere l'advisor (decisione 2026-11-25).

L'advisor rilegge l'intero contesto con lo stesso modello del run (Opus 5.5) e costava
~$1-1,5 a chiamata (+40-50% sul run giornaliero) senza un beneficio dimostrato.
`advisorModel` sta nel settings utente, che i `claude -p` di launchd leggono: l'unica
difesa è la variabile d'ambiente nello script. Questo test fallisce se un job nuovo
(o uno esistente) chiama `"$CLAUDE" -p` senza l'export prima della chiamata.
Non distruttivo: legge solo gli script.
"""
import re
import sys
from pathlib import Path

PIPE = Path(__file__).resolve().parents[1]
EXPORT = re.compile(r"^export CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1\b", re.M)
CALL = re.compile(r'"\$CLAUDE" -p|\bclaude -p ')   # la chiamata vera, non i commenti

job = [p for p in sorted(PIPE.glob("*.sh")) if re.search(r'^[^#\n]*"\$CLAUDE" -p', p.read_text(), re.M)]
assert len(job) >= 6, f"trovati solo {[p.name for p in job]}: il glob non vede i job?"
rotti = []
for p in job:
    t = p.read_text()
    e, c = EXPORT.search(t), re.search(r'^[^#\n]*"\$CLAUDE" -p', t, re.M)
    if not e or e.start() > c.start():
        rotti.append(p.name)
for p in job:
    print(f"  {'✗' if p.name in rotti else '✓'} {p.name}")
print(f"\nno_advisor: {len(job) - len(rotti)} passati, {len(rotti)} falliti")
sys.exit(1 if rotti else 0)
