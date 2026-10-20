#!/usr/bin/env python3
"""
render_report.py

Rende il report giornaliero (markdown) in un singolo file HTML impaginato,
nello stile dei morning briefing, così si apre con doppio clic nel browser.

Combina in un'unica pagina:
  - _index.md      (digest di triage + sintesi di sessione)
  - news_NN.md     (le singole schede, in ordine)
con una barra di navigazione in cima. Tabelle dell'event study renderizzate.

Uso CLI:
    venv/bin/python render_report.py                 # report di oggi
    venv/bin/python render_report.py --date 2026-05-29
    venv/bin/python render_report.py --date 2026-05-29 --open   # apre nel browser

Output: daily_analysis/YYYY-MM-DD/report.html
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import markdown

from stile import REPORT


DAILY_ANALYSIS_DIR = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"
GLOSSARY_PATH = Path(__file__).resolve().parent / "glossario.md"

CSS = REPORT   # stile condiviso: stile.py

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "nl2br"]

_NEWS_LINK_RE = re.compile(r"\]\((news_\d+)\.md\)")


def _internal_links(text: str) -> str:
    """Riscrive i link `news_NN.md` del triage in ancore interne alla pagina
    renderizzata: `doc-{stem}` e' l'id di sezione assegnato piu' sotto in `render()`."""
    return _NEWS_LINK_RE.sub(r"](#doc-\1)", text)


def _first_h1(md_text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md_text, flags=re.MULTILINE)
    return m.group(1).strip() if m else fallback


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render(day_dir: Path, day: str) -> Path:
    index_path = day_dir / "_index.md"
    news_paths = sorted(day_dir.glob("news_*.md"))
    if not index_path.exists() and not news_paths:
        raise FileNotFoundError(f"Nessun report in {day_dir}")

    docs = []  # (anchor, nav_title, html)
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    if index_path.exists():
        md.reset()
        text = _internal_links(index_path.read_text(encoding="utf-8"))
        docs.append(("doc-index", "Indice & triage", md.convert(text)))

    for p in news_paths:
        text = _internal_links(p.read_text(encoding="utf-8"))
        title = _first_h1(text, p.stem)
        anchor = f"doc-{p.stem}"
        md.reset()
        docs.append((anchor, f"{p.stem} — {title}", md.convert(text)))

    if GLOSSARY_PATH.exists():
        md.reset()
        docs.append(("doc-glossario", "Glossario", md.convert(GLOSSARY_PATH.read_text(encoding="utf-8"))))

    nav = "\n".join(
        f'      <li><a href="#{a}">{t}</a></li>' for a, t, _ in docs
    )
    sections = "\n".join(
        f'    <section class="doc" id="{a}">\n{h}\n    </section>' for a, _, h in docs
    )

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Daily Analysis — {day}</title>
<style>{CSS}</style>
</head>
<body>
  <header class="report-head">
    <div class="date-label">News-to-Market Impact</div>
    <h1>Daily analysis — {day}</h1>
    <p class="subtitle">Triage del morning briefing + event study sugli analoghi storici. Statistiche descrittive, non segnali operativi.</p>
  </header>
  <nav class="toc">
    <h2>In questa pagina</h2>
    <ol>
{nav}
    </ol>
  </nav>
{sections}
  <footer>
    Generato da News-to-Market Impact Pipeline · {day} · Le statistiche con N&lt;10 sono "indicative only".
  </footer>
</body>
</html>
"""
    out = day_dir / "report.html"
    out.write_text(html, encoding="utf-8")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rende il report giornaliero in HTML")
    ap.add_argument("--date", help="AAAA-MM-GG (default: oggi)")
    ap.add_argument("--open", action="store_true", help="Apre il report nel browser (macOS)")
    args = ap.parse_args(argv)

    day = args.date or date.today().isoformat()
    day_dir = DAILY_ANALYSIS_DIR / day
    try:
        out = render(day_dir, day)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1

    print(f"Report HTML generato: {out}")
    if args.open:
        subprocess.run(["open", str(out)], check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
