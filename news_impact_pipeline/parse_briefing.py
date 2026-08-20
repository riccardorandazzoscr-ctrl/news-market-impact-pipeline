#!/usr/bin/env python3
"""
parse_briefing.py

Parser deterministico per i morning briefing HTML (Fase 5).

I briefing vivono in `~/Claude/morning brief/` con naming
`YYYY-MM-DD-morning-briefing.html`. Ogni file ha tre sezioni:
  - "Top 10 International News"      -> 10 storie geopolitiche
  - "Top 10 Economics & Finance News" -> 10 storie macro/mercati
  - "One Thing to Watch Today"       -> 1 box di sintesi

Questo modulo estrae gli item in forma strutturata. Non fa NESSUNA
classificazione semantica: quella resta compito dell'agente Claude in
sessione (cfr. cambio architetturale Fase 3). Serve solo a trasformare
l'HTML in dati puliti su cui l'agente può iterare.

Uso CLI (esempi):
    venv/bin/python parse_briefing.py                      # briefing di oggi, listing leggibile
    venv/bin/python parse_briefing.py --date 2026-05-29
    venv/bin/python parse_briefing.py --file "/path/to/file.html"
    venv/bin/python parse_briefing.py --section finance    # solo economics/finance
    venv/bin/python parse_briefing.py --json               # output JSON per uso programmatico
    venv/bin/python parse_briefing.py --list-dates         # quali briefing sono disponibili

Uso programmatico:
    from parse_briefing import parse_briefing, briefing_path
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup


BRIEFING_DIR = Path.home() / "Claude" / "morning brief"
FILENAME_FMT = "{date}-morning-briefing.html"
FILENAME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-morning-briefing\.html$")

# Etichette di sezione canoniche dell'output.
SECTION_INTERNATIONAL = "international"
SECTION_FINANCE = "finance"


def briefing_path(d: date) -> Path:
    """Percorso atteso del briefing per una data."""
    return BRIEFING_DIR / FILENAME_FMT.format(date=d.isoformat())


def available_dates() -> list[str]:
    """Date (YYYY-MM-DD) dei briefing presenti nella cartella, ordinate."""
    if not BRIEFING_DIR.exists():
        return []
    dates = []
    for p in BRIEFING_DIR.iterdir():
        m = FILENAME_RE.search(p.name)
        if m:
            dates.append(m.group(1))
    return sorted(dates)


def _clean(text: str) -> str:
    """Normalizza whitespace; bs4 ha gia' defatto le entita' HTML."""
    return re.sub(r"\s+", " ", text or "").strip()


def _first_text(node, selectors: list[str]) -> str:
    """Testo del primo selettore che matcha (gestisce la deriva di layout).

    Ogni selettore e' un tag ("h3") o una classe (".headline")."""
    for sel in selectors:
        el = node.find(class_=sel[1:]) if sel.startswith(".") else node.find(sel)
        if el:
            return _clean(el.get_text())
    return ""


def _section_label(h2_text: str) -> str | None:
    """Mappa il titolo della sezione (h2) su un'etichetta canonica.

    Ritorna None per sezioni che non sono liste di storie numerate
    (es. "One Thing to Watch Today", gestita a parte)."""
    t = h2_text.lower()
    if "international" in t:
        return SECTION_INTERNATIONAL
    if "econom" in t or "finance" in t:
        return SECTION_FINANCE
    return None


def parse_briefing(path: Path) -> dict:
    """Estrae il contenuto strutturato di un briefing HTML.

    Ritorna:
        {
          "date": "YYYY-MM-DD" | None,
          "title": str,
          "sections": {
              "international": [ {num, title, body, sources}, ... ],
              "finance":       [ {num, title, body, sources}, ... ],
          },
          "watch": {"title": str, "body": str} | None,
          "source_file": str,
        }
    """
    if not path.exists():
        raise FileNotFoundError(f"Briefing non trovato: {path}")

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    # Data: prima dal nome file (autoritativo), poi fallback all'header.
    m = FILENAME_RE.search(path.name)
    file_date = m.group(1) if m else None

    title_tag = soup.find("title")
    title = _clean(title_tag.get_text()) if title_tag else ""

    sections: dict[str, list[dict]] = {
        SECTION_INTERNATIONAL: [],
        SECTION_FINANCE: [],
    }
    watch = None

    for section in soup.find_all("section"):
        h2 = section.find("h2")
        if not h2:
            continue
        label = _section_label(h2.get_text())
        if label is None:
            continue

        for story in section.find_all(class_="story"):
            num_tag = story.find(class_="story-num")
            src = story.find(class_="source")
            sections[label].append(
                {
                    "num": _clean(num_tag.get_text()) if num_tag else "",
                    # Il tag del titolo e' variato fra le "ere" dei briefing:
                    # <h3> (layout attuale) oppure .headline (fine aprile).
                    "title": _first_text(story, ["h3", ".headline"]),
                    "body": _clean(story.find("p").get_text()) if story.find("p") else "",
                    "sources": _clean(src.get_text()) if src else "",
                }
            )

    # "One Thing to Watch Today": il box puo' stare dentro un <section>
    # (layout recente) o come <div> nudo nel body (layout vecchio); il
    # titolo e' in <h3> oppure .watch-headline. Cerchiamo su tutto il doc.
    box = soup.find(class_="watch-box")
    if box:
        wp = box.find("p")
        watch = {
            "title": _first_text(box, ["h3", ".watch-headline"]),
            "body": _clean(wp.get_text()) if wp else "",
        }

    # Validazione rumorosa: titoli vuoti = layout sconosciuto, non un
    # briefing davvero vuoto. Meglio segnalarlo che restituire dati monchi.
    empty = sum(
        1
        for stories in sections.values()
        for s in stories
        if not s["title"]
    )
    if empty:
        print(
            f"⚠ parse_briefing: {empty} storie senza titolo in {path.name} "
            f"— possibile layout HTML non riconosciuto.",
            file=sys.stderr,
        )

    return {
        "date": file_date,
        "title": title,
        "sections": sections,
        "watch": watch,
        "source_file": str(path),
    }


def _all_items(parsed: dict, which: str) -> list[tuple[str, dict]]:
    """Appiattisce le storie selezionate in (etichetta_sezione, story)."""
    out: list[tuple[str, dict]] = []
    order = (
        [SECTION_INTERNATIONAL, SECTION_FINANCE]
        if which == "all"
        else [which]
    )
    for label in order:
        for story in parsed["sections"].get(label, []):
            out.append((label, story))
    return out


def format_listing(parsed: dict, which: str = "all") -> str:
    """Listing leggibile per l'agente: titoli + corpo per sezione."""
    lines = []
    hdr = parsed.get("date") or parsed.get("title") or "briefing"
    lines.append(f"# Morning Briefing — {hdr}")
    lines.append("")

    labels = {
        SECTION_INTERNATIONAL: "🌍 International",
        SECTION_FINANCE: "💹 Economics & Finance",
    }
    order = (
        [SECTION_INTERNATIONAL, SECTION_FINANCE]
        if which == "all"
        else [which]
    )
    for label in order:
        stories = parsed["sections"].get(label, [])
        lines.append(f"## {labels.get(label, label)} ({len(stories)})")
        lines.append("")
        for s in stories:
            lines.append(f"[{label}/{s['num']}] {s['title']}")
            lines.append(f"    {s['body']}")
            if s["sources"]:
                lines.append(f"    — {s['sources']}")
            lines.append("")

    if which == "all" and parsed.get("watch"):
        lines.append("## 🔍 One Thing to Watch Today")
        lines.append("")
        lines.append(parsed["watch"]["title"])
        lines.append(f"    {parsed['watch']['body']}")
        lines.append("")

    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Parser dei morning briefing HTML (Fase 5)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--date", help="Data del briefing (YYYY-MM-DD). Default: oggi.")
    g.add_argument("--file", help="Percorso esplicito a un file briefing HTML.")
    ap.add_argument(
        "--section",
        choices=["international", "finance", "all"],
        default="all",
        help="Quali storie estrarre. Default: all.",
    )
    ap.add_argument("--json", action="store_true", help="Output JSON invece del listing.")
    ap.add_argument(
        "--list-dates",
        action="store_true",
        help="Elenca le date dei briefing disponibili ed esce.",
    )
    args = ap.parse_args(argv)

    if args.list_dates:
        dates = available_dates()
        if not dates:
            print(f"Nessun briefing in {BRIEFING_DIR}", file=sys.stderr)
            return 1
        print("\n".join(dates))
        return 0

    if args.file:
        path = Path(args.file).expanduser()
    elif args.date:
        try:
            d = date.fromisoformat(args.date)
        except ValueError:
            print(f"Data non valida: {args.date} (atteso YYYY-MM-DD)", file=sys.stderr)
            return 2
        path = briefing_path(d)
    else:
        path = briefing_path(date.today())

    try:
        parsed = parse_briefing(path)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        avail = available_dates()
        if avail:
            print(f"Disponibili: {avail[0]} … {avail[-1]} ({len(avail)} file)", file=sys.stderr)
        return 1

    if args.json:
        if args.section != "all":
            parsed = {
                **parsed,
                "sections": {args.section: parsed["sections"].get(args.section, [])},
                "watch": parsed["watch"] if args.section == "all" else None,
            }
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    else:
        print(format_listing(parsed, which=args.section))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
