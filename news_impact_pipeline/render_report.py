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


DAILY_ANALYSIS_DIR = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #ffffff; color: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px; line-height: 1.7; padding: 0 16px; max-width: 900px; margin: 0 auto;
}
header.report-head { border-bottom: 3px solid #1a1a1a; padding: 36px 0 20px; margin-bottom: 16px; }
header.report-head .date-label { font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: #666; margin-bottom: 6px; }
header.report-head h1 { font-size: clamp(1.6rem, 5vw, 2.2rem); font-weight: 700; line-height: 1.2; }
header.report-head p.subtitle { margin-top: 8px; color: #555; font-size: 0.95rem; }
nav.toc { background: #f5f5f5; border-left: 5px solid #1a1a1a; padding: 16px 22px; border-radius: 4px; margin-bottom: 40px; }
nav.toc h2 { font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; color: #888; margin-bottom: 10px; }
nav.toc ol { margin-left: 18px; }
nav.toc a { color: #1a1a1a; text-decoration: none; }
nav.toc a:hover { text-decoration: underline; }
section.doc { margin-bottom: 56px; padding-bottom: 32px; border-bottom: 1px solid #e8e8e8; }
section.doc:last-child { border-bottom: none; }
h1 { font-size: 1.5rem; font-weight: 700; line-height: 1.25; margin: 28px 0 12px; color: #111; }
h2 { font-size: 1.05rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; border-left: 4px solid #1a1a1a; padding-left: 12px; margin: 32px 0 16px; }
h3 { font-size: 1rem; font-weight: 700; margin: 20px 0 8px; }
h4 { font-size: 0.92rem; font-weight: 700; margin: 16px 0 6px; color: #333; }
p, li { font-size: 0.95rem; }
p { margin: 8px 0; }
ul, ol { margin: 8px 0 8px 24px; }
strong { font-weight: 700; }
hr { border: none; border-top: 1px solid #e8e8e8; margin: 24px 0; }
blockquote { background: #fff8e1; border-left: 4px solid #e0a800; padding: 10px 16px; margin: 12px 0; border-radius: 3px; font-size: 0.92rem; }
code { background: #f0f0f0; padding: 1px 5px; border-radius: 3px; font-size: 0.85em; font-family: "SF Mono", Menlo, Consolas, monospace; }
pre { background: #1a1a1a; color: #f5f5f5; padding: 14px 16px; border-radius: 6px; overflow-x: auto; margin: 12px 0; font-size: 0.82rem; }
pre code { background: none; color: inherit; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 0.85rem; }
th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
th { background: #f5f5f5; font-weight: 700; }
tr:nth-child(even) td { background: #fafafa; }
details { margin: 10px 0; }
summary { cursor: pointer; font-weight: 600; font-size: 0.88rem; color: #555; }
footer { border-top: 1px solid #e8e8e8; padding: 24px 0; margin-top: 40px; font-size: 0.8rem; color: #aaa; }
@media (max-width: 600px) { body { font-size: 15px; } table { font-size: 0.78rem; } }
"""

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "nl2br"]


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
        docs.append(("doc-index", "Indice & triage", md.convert(index_path.read_text(encoding="utf-8"))))

    for p in news_paths:
        text = p.read_text(encoding="utf-8")
        title = _first_h1(text, p.stem)
        anchor = f"doc-{p.stem}"
        md.reset()
        docs.append((anchor, f"{p.stem} — {title}", md.convert(text)))

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
    <h1>📊 Daily Analysis — {day}</h1>
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
