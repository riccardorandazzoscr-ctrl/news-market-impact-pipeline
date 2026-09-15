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
import hashlib
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

# Sigla breve della sezione, usata nella colonna "Sez." della tabella di triage.
# Sta QUI e non in pipeline_tools perche' insieme al numero forma l'IDENTITA' di
# una notizia: i numeri si ripetono fra le due sezioni (esiste un 01 intl e un 01
# fin nello stesso briefing), quindi il numero da solo non identifica nulla.
SEZIONE_BREVE = {SECTION_INTERNATIONAL: "intl", SECTION_FINANCE: "fin"}


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


def _body_text(story) -> str:
    """Tutto il testo di contenuto della storia, non solo il primo paragrafo."""
    paras = [p for p in story.find_all("p") if p.get("class") != ["source"]]
    return _clean(" ".join(p.get_text() for p in paras))


def _sources(story) -> list[dict]:
    """Fonti della storia come {name, url}; url vuoto se il layout non la porta."""
    src = story.find(class_="source")
    if not src:
        return []
    links = src.find_all("a")
    if links:
        return [{"name": _clean(a.get_text()), "url": a.get("href", "")} for a in links]
    text = re.sub(r"^\s*Source:\s*", "", _clean(src.get_text()))
    return [{"name": n.strip(), "url": ""} for n in re.split(r"[;/]", text) if n.strip()]


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
            sections[label].append(
                {
                    "num": _clean(num_tag.get_text()) if num_tag else "",
                    # Il tag del titolo e' variato fra le "ere" dei briefing:
                    # <h3> (layout attuale) oppure .headline (fine aprile).
                    "title": _first_text(story, ["h3", ".headline"]),
                    "body": _body_text(story),
                    "sources": _sources(story),
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


def chiave_item(label: str, story: dict) -> str:
    """Identita' di una notizia dentro un briefing: "intl/01", "fin/07".

    Il solo numero non basta: si ripete fra le due sezioni."""
    return f"{SEZIONE_BREVE.get(label, label)}/{story.get('num') or '—'}"


def _canonico(story: dict) -> str:
    """Forma canonica del contenuto di una storia, per l'impronta."""
    fonti = " ; ".join(f"{s['name']}|{s['url']}" for s in story["sources"])
    return "\n".join([story["title"], story["body"], fonti])


def impronte(parsed: dict) -> dict:
    """Impronte del briefing: una per notizia, una per l'insieme.

    Servono a legare lo stato di una giornata all'IDENTITA' del suo input e non
    alla sola data (cfr. R07): al ritentativo una scheda si riusa solo se il testo
    delle notizie che la alimentano non e' cambiato.

    Il box "One Thing to Watch" e' escluso di proposito dall'impronta complessiva:
    non alimenta nessuna scheda, e includerlo farebbe rifare da capo un'intera
    giornata per una riga di contorno riscritta.

    Ritorna {"briefing": <sha>, "items": {"intl/01": <sha>, ...}}.
    """
    items, ordinate = {}, []
    for label, story in _all_items(parsed, "all"):
        k = chiave_item(label, story)
        h = hashlib.sha256(_canonico(story).encode("utf-8")).hexdigest()[:16]
        items[k] = h
        ordinate.append(f"{k}={h}")
    return {
        "briefing": hashlib.sha256("\n".join(ordinate).encode("utf-8")).hexdigest()[:16],
        "items": items,
    }


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
                src_str = "; ".join(
                    f"{src['name']} ({src['url']})" if src["url"] else src["name"]
                    for src in s["sources"]
                )
                lines.append(f"    — {src_str}")
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
    ap.add_argument(
        "--impronte",
        action="store_true",
        help="Stampa in JSON l'impronta del briefing e quella di ogni notizia.",
    )
    ap.add_argument(
        "--count",
        action="store_true",
        help="Stampa solo il numero totale di storie estratte (per guardie shell) ed esce.",
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
        if args.count:
            print(0)
            return 0
        print(str(e), file=sys.stderr)
        avail = available_dates()
        if avail:
            print(f"Disponibili: {avail[0]} … {avail[-1]} ({len(avail)} file)", file=sys.stderr)
        return 1

    if args.count:
        print(sum(len(stories) for stories in parsed["sections"].values()))
        return 0

    if args.impronte:
        print(json.dumps(impronte(parsed), ensure_ascii=False, indent=2))
        return 0

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
