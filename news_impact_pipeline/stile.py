#!/usr/bin/env python3
"""stile.py — foglio di stile unico delle pagine della pipeline.

Lo stile è quello dell'anteprima settimanale (2026-10-19): fondo caldo, testo serif,
titoli e tabelle sans-serif, riquadri arrotondati, tema scuro automatico.

- BASE: colori, tipografia, tabelle, riquadri richiudibili. Lo usano tutte le pagine.
- REPORT: le pagine rese da Markdown (daily analysis, scorecard, report mensile).
- BRIEF: il morning brief, con le classi che il modello scrive e che parse_briefing legge.

Uso da riga di comando: `stile.py brief FILE` sostituisce il blocco <style> del morning
brief scritto dal modello. Tocca solo lo stile: tag, classi e testo restano identici,
quindi l'impronta del briefing (parse_briefing.py) non cambia.
"""
import os
import re
import sys
from pathlib import Path

BASE = """
:root{--bg:#fafaf7;--card:#fff;--ink:#1f2328;--soft:#5f6670;--line:#e4e2dc;--accent:#1d4e89;
--up:#1a7f37;--down:#c0392b;--warn-bg:#fff4e0;--warn:#8a5a00;--quote:#f3f2ee}
@media (prefers-color-scheme:dark){:root{--bg:#16181b;--card:#1f2226;--ink:#e8e6e1;--soft:#9aa0a8;
--line:#33373d;--accent:#7fb0ea;--up:#4cc26d;--down:#ef6b5b;--warn-bg:#3a2e17;--warn:#f0c46b;--quote:#262a2f}}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Georgia,'Iowan Old Style',serif}
h1,h2,h3,h4,table,summary,nav,footer,.sans{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif}
a{color:var(--accent)}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;margin:12px 0}
th{font-weight:600;color:var(--soft);font-size:12px;text-transform:uppercase;letter-spacing:.04em;
text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:bottom}
td{text-align:left;padding:8px;border-bottom:1px solid var(--line);vertical-align:top}
img{max-width:100%;border-radius:8px}
details{margin:14px 0;font-size:15px}
summary{cursor:pointer;color:var(--accent);font-size:14px;font-weight:600}
blockquote{background:var(--warn-bg);color:var(--ink);border-radius:10px;padding:10px 16px;margin:14px 0;font-size:15px}
blockquote p{margin:4px 0}
code{background:var(--quote);padding:1px 5px;border-radius:4px;font-size:.85em;font-family:'SF Mono',Menlo,Consolas,monospace}
pre{background:var(--quote);padding:14px 16px;border-radius:10px;overflow-x:auto;font-size:13px}
pre code{background:none;padding:0}
hr{border:none;border-top:1px solid var(--line);margin:24px 0}
footer{color:var(--soft);font-size:13px;margin-top:36px}
@media (max-width:520px){body{font-size:16px}td,th{padding:6px 4px}table{font-size:13px}}
"""

REPORT = BASE + """
body{padding:28px 16px 60px}
body>*{max-width:760px;margin-left:auto;margin-right:auto}
header.report-head{margin-bottom:24px}
header.report-head .date-label{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;font-size:12px;
letter-spacing:.1em;text-transform:uppercase;color:var(--soft);margin-bottom:4px}
header.report-head h1{font-size:30px;margin:0 0 6px;letter-spacing:-.01em;line-height:1.2}
header.report-head p.subtitle{color:var(--soft);font-size:15px;margin:0}
nav.toc{background:var(--quote);border-radius:10px;padding:14px 18px;margin-bottom:28px;font-size:15px}
nav.toc h2{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0 0 6px}
nav.toc ol{margin:0;padding-left:20px}nav.toc li{margin:3px 0}
nav.toc a{text-decoration:none;font-weight:600}
section.doc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 22px;margin-bottom:28px}
section.doc h1{font-size:24px;line-height:1.25;margin:0 0 12px}
section.doc h2{font-size:20px;margin:28px 0 8px}
section.doc h3{font-size:16px;margin:22px 0 6px}
section.doc h4{font-size:15px;margin:16px 0 4px;color:var(--soft)}
section.doc>:first-child{margin-top:0}
p{margin:8px 0}ul,ol{margin:8px 0;padding-left:24px}li{margin:3px 0}
section.doc table{display:block;overflow-x:auto}
@media (max-width:520px){section.doc{padding:18px 14px}header.report-head h1{font-size:25px}}
"""

BRIEF = BASE + """
body{padding:28px 16px 60px}
.container{max-width:760px;margin:auto}
header{margin-bottom:28px}
header .date-label{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;font-size:12px;
letter-spacing:.1em;text-transform:uppercase;color:var(--soft);margin-bottom:4px}
header h1{font-size:30px;margin:0 0 6px;letter-spacing:-.01em;line-height:1.2}
header p.subtitle{color:var(--soft);font-size:15px;margin:0}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 22px 6px;margin-bottom:28px}
section h2{font-size:20px;margin:0 0 16px}
.story{padding:0 0 20px;margin:0 0 20px;border-bottom:1px solid var(--line)}
.story:last-child{border-bottom:none;margin-bottom:0}
.story-num{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;font-size:12px;font-weight:600;
letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin-bottom:2px}
.story h3{font-size:18px;line-height:1.35;margin:0 0 8px}
.story p{margin:0 0 8px}
.story .markets{display:block;margin-top:6px;font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;
font-size:13px;color:var(--soft)}
.story .source{display:inline-block;margin-top:4px;font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;
font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--soft)}
.story .source a{text-decoration:none}
.watch-box{border-left:3px solid var(--accent);padding:2px 0 2px 16px;margin:0 0 16px}
.watch-box h3{font-size:18px;margin:0 0 8px}
.watch-box p{margin:0 0 8px}
@media (max-width:520px){section{padding:18px 14px 4px}header h1{font-size:25px}}
"""

_STYLE = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)


def restyle_brief(path: Path) -> bool:
    """Sostituisce il primo <style> del brief con BRIEF; scrittura atomica. False se non c'è."""
    text = path.read_text(encoding="utf-8")
    new, n = _STYLE.subn(lambda _: f"<style>{BRIEF}</style>", text, count=1)
    if not n or new == text:
        return False
    tmp = path.with_name(f".{path.name}.restyle")
    tmp.write_text(new, encoding="utf-8")
    os.replace(tmp, path)
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "brief":
        sys.exit("uso: stile.py brief FILE")
    print("ristilizzato" if restyle_brief(Path(sys.argv[2])) else "invariato")
