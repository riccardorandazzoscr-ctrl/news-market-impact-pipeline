#!/usr/bin/env python3
"""parse_briefing.py e render_report.py — il passaggio briefing → dato strutturato → HTML.

Perché esiste (R08, revisione 2026-09-14/15): il parser leggeva solo il primo
paragrafo di ogni storia e buttava via gli URL delle fonti; il renderer non
trasformava i link `news_NN.md` del triage in ancore interne al report HTML
combinato. Tutti e tre i comportamenti sono verificati qui su HTML sintetico,
non sui briefing reali (che restano coperti da test_briefing_race.sh).

Non distruttivo: lavora solo su file temporanei.
"""

import sys
import tempfile
from pathlib import Path

PIPE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPE))
import parse_briefing as pb  # noqa: E402
import render_report as rr  # noqa: E402

PASS = FAIL = 0


def check(cond, descr, extra=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {descr}")
        PASS += 1
    else:
        print(f"  ✗ {descr}")
        if extra:
            print(f"      {extra}")
        FAIL += 1


HTML = """<html><head><title>Morning Briefing</title></head><body>
<section><h2>Top 10 Economics &amp; Finance News</h2>
<div class="story">
  <div class="story-num">01</div>
  <h3>Titolo</h3>
  <p>Primo paragrafo.</p>
  <p>Secondo paragrafo, oggi perso.</p>
  <p class="source">Source: <a href="https://example.com/a">Fonte A</a>; <a href="https://example.com/b">Fonte B</a></p>
</div>
</section>
</body></html>"""

print("--- parse_briefing: corpo multi-paragrafo e fonti con URL ---")
tmp = Path(tempfile.mkdtemp()) / "2026-09-15-morning-briefing.html"
tmp.write_text(HTML, encoding="utf-8")
parsed = pb.parse_briefing(tmp)
story = parsed["sections"]["finance"][0]
check("Secondo paragrafo" in story["body"],
      "il corpo include il secondo paragrafo, non solo il primo", story["body"])
check(story["sources"] == [
    {"name": "Fonte A", "url": "https://example.com/a"},
    {"name": "Fonte B", "url": "https://example.com/b"},
], "le fonti portano nome e URL", str(story["sources"]))

print("\n--- parse_briefing --count: il parser vero, non un grep su class=\"story\" ---")
senza_section = tmp.with_name("senza-section.html")
senza_section.write_text(
    '<html><body><h2>Economics &amp; Finance</h2>'
    '<div class="story"><h3>T</h3><p>Corpo.</p></div></body></html>',
    encoding="utf-8",
)
import subprocess  # noqa: E402

rc = subprocess.run(
    [sys.executable, str(PIPE / "parse_briefing.py"), "--file", str(senza_section), "--count"],
    capture_output=True, text=True,
)
check(rc.stdout.strip() == "0",
      "storia senza <section> contenitore: il conteggio vero e' zero",
      f"stdout={rc.stdout!r} stderr={rc.stderr}")

rc2 = subprocess.run(
    [sys.executable, str(PIPE / "parse_briefing.py"), "--file", str(tmp), "--count"],
    capture_output=True, text=True,
)
check(rc2.stdout.strip() == "1", "storia dentro <section>+<h2>: conta", rc2.stdout)

print("\n--- render_report: link news_NN.md -> ancora interna ---")
testo = rr._internal_links("Vedi la scheda [qui](news_03.md) per il dettaglio.")
check("(#doc-news_03)" in testo, "il link diventa un'ancora #doc-news_03", testo)
check("news_03.md)" not in testo, "il vecchio percorso file non resta nell'output", testo)

print(f"\n{'=' * 60}")
print(f"parse_briefing/render_report: {PASS} passati, {FAIL} falliti")
print(f"{'=' * 60}")
sys.exit(1 if FAIL else 0)
