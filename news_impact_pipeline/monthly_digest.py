#!/usr/bin/env python3
"""
monthly_digest.py — Layer 6: input per il Report Strategico Mensile.

NON produce previsioni: AGGREGA tutto il materiale del mese (schede giornaliere +
scorecard + regimi della Knowledge Base) in una bozza che l'agente Claude poi compila
nelle sezioni qualitative (vedi PHASE6_RUNBOOK.md). Sola lettura sul resto del sistema.

Filosofia (decisa il 2026-06-09): è una *sintesi di regime e scenari*, non
un oracolo a lungo raggio — perché la scorecard mostra che l'edge predittivo decade
con l'orizzonte. Quindi: regimi attivi, bilancio rischi, scenari condizionali, e una
manciata di previsioni FALSIFICABILI che alimenteranno una scorecard a lungo raggio.

Uso:
    venv/bin/python monthly_digest.py --month 2026-06     # bozza per quel mese
    venv/bin/python monthly_digest.py                     # mese corrente
    # aggiungi --force per rigenerare una bozza esistente
"""

import argparse
import re
from collections import Counter
from datetime import date
from pathlib import Path

import yaml
import markdown
from render_report import CSS, MD_EXTENSIONS

DAILY_DIR = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"
MONTHLY_DIR = DAILY_DIR / "_monthly"
SCORECARD_DIR = DAILY_DIR / "_scorecard"
CATALOG = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base" / "catalog.yaml"


def _field(text: str, name: str) -> str:
    m = re.search(rf"\|\s*`{name}`\s*\|\s*([^\|<\n]+)", text)
    return m.group(1).strip() if m else ""


def parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = ""
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    assets = sorted(set(re.findall(r"###\s+Event study\s+—\s+`([^`]+)`", text)))
    return {
        "date": path.parent.name,
        "title": title,
        "primary_theme": _field(text, "primary_theme"),
        "sentiment": _field(text, "sentiment"),
        "confidence": _field(text, "confidence"),
        "assets": assets,
    }


def discover_cards(month: str) -> list[dict]:
    """month = 'YYYY-MM'. Solo cartelle-giorno strette YYYY-MM-DD (esclude i backup)."""
    re_day = re.compile(rf"^{re.escape(month)}-\d{{2}}$")
    cards = []
    for day_dir in sorted(DAILY_DIR.iterdir()):
        if day_dir.is_dir() and re_day.match(day_dir.name):
            for card in sorted(day_dir.glob("news_*.md")):
                cards.append(parse_card(card))
    return cards


def latest_scorecard_excerpt() -> tuple[str, str]:
    """Restituisce (nome_file, estratto markdown) dell'ultima scorecard: 'In sintesi' +
    la tabella per-tema (sez. 5), che dicono DOVE abbiamo edge."""
    files = sorted(SCORECARD_DIR.glob("20*-W*.md")) if SCORECARD_DIR.exists() else []
    if not files:
        return ("(nessuna)", "_Scorecard non ancora disponibile._")
    text = files[-1].read_text(encoding="utf-8")
    def _section(header_regex):
        m = re.search(rf"(##\s+{header_regex}.*?)(?=\n##\s|\Z)", text, re.DOTALL)
        return m.group(1).strip() if m else ""
    parts = [p for p in (_section(r"In sintesi"), _section(r"\d+\.\s*Quali temi")) if p]
    return (files[-1].name, "\n\n".join(parts) or "_(sezioni non trovate)_")


def kb_regimes() -> list[str]:
    if not CATALOG.exists():
        return []
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}
    out = []
    for e in data.get("entries", []):
        phases = e.get("regime_phases") or []
        current = ""
        if phases:
            last = phases[-1]
            current = list(last.keys())[0] if isinstance(last, dict) else str(last)
        out.append(f"**{e.get('primary_theme','?')}** — {e.get('title','?')[:70]} "
                   f"(fase corrente: `{current}`)")
    return out


def build_scaffold(month: str) -> str:
    cards = discover_cards(month)
    n = len(cards)
    days = sorted({c["date"] for c in cards})
    themes = Counter(c["primary_theme"] for c in cards if c["primary_theme"])
    sentiments = Counter(c["sentiment"] for c in cards if c["sentiment"])
    assets = Counter(a for c in cards for a in c["assets"])
    sc_name, sc_excerpt = latest_scorecard_excerpt()

    L = []
    L.append(f"# 📅 Report Strategico Mensile — {month}\n")
    L.append("> ⚠ **Bozza**: la sezione 'Materiale aggregato' è generata da "
             "`monthly_digest.py` (NON modificarla); le sezioni numerate le compila "
             "l'agente seguendo `PHASE6_RUNBOOK.md`. È una sintesi di **regime e "
             "scenari**, non previsioni puntuali.\n")

    L.append("## Materiale aggregato _(input — non modificare)_\n")
    L.append(f"- **Schede del periodo**: {n} su {len(days)} giorni "
             f"({days[0] if days else '—'} → {days[-1] if days else '—'}).")
    L.append(f"- **Temi dominanti**: " +
             (", ".join(f"{t} ({c})" for t, c in themes.most_common()) or "—") + ".")
    L.append(f"- **Bilancio sentiment**: " +
             (", ".join(f"{s} ({c})" for s, c in sentiments.most_common()) or "—") + ".")
    L.append(f"- **Asset più ricorrenti**: " +
             (", ".join(f"{a} ({c})" for a, c in assets.most_common(10)) or "—") + ".\n")

    L.append("### Regimi attivi dalla Knowledge Base\n")
    for r in kb_regimes():
        L.append(f"- {r}")
    L.append("")

    L.append(f"### Dove abbiamo edge — estratto dall'ultima scorecard ({sc_name})\n")
    L.append(sc_excerpt)
    L.append("")

    L.append("### Elenco schede per tema\n")
    by_theme: dict = {}
    for c in cards:
        by_theme.setdefault(c["primary_theme"] or "(senza tema)", []).append(c)
    for theme, sub in sorted(by_theme.items(), key=lambda kv: -len(kv[1])):
        L.append(f"- **{theme}** ({len(sub)}):")
        for c in sub:
            L.append(f"  - {c['date']} — {c['title']} "
                     f"[{c['sentiment']}, conf. {c['confidence']}, {', '.join(c['assets']) or 'no asset'}]")
    L.append("")

    L.append("---\n")
    L.append("## 1. Mappa dei regimi attivi\n")
    L.append("<!-- Quali regimi dominano ORA (da KB + schede del mese). Per ciascuno: "
             "cos'è, da quando, e quali asset muove. Espandi le sigle. -->\n")
    L.append("## 2. Bilancio dei rischi cross-asset\n")
    L.append("<!-- Dove convergono/divergono i segnali del mese. Direzione di rischio "
             "prevalente per le classi principali (azionario, tassi, FX, commodity, "
             "credito/volatilità). -->\n")
    L.append("## 3. Catalizzatori in arrivo (calendario)\n")
    L.append("<!-- Eventi datati del mese entrante: release macro (CPI/NFP/PIL), "
             "riunioni banche centrali, elezioni, scadenze. Fattuale, non scommesse. -->\n")
    L.append("## 4. Scenari (condizionali, ramificati)\n")
    L.append("<!-- 2-3 scenari con CONDIZIONE → conseguenze cross-asset. NON una "
             "previsione singola. Es: 'se Hormuz de-escala → … ; se la BCE è puramente "
             "restrittiva come nel 2011 → …'. -->\n")
    L.append("## 5. Lettura pesata dalla scorecard (dove fidarsi, dove no)\n")
    L.append("<!-- Usa l'estratto scorecard sopra: dai peso ai temi con edge "
             "(es. geopolitico/monetario/macro) e DECLASSA esplicitamente quelli senza "
             "(es. structural_themes/AI: IC negativo → lettura qualitativa, non "
             "magnitudo). Ricorda: l'edge è a orizzonte breve. -->\n")
    L.append("## 6. Previsioni falsificabili del mese\n")
    L.append("<!-- 3-4 affermazioni VERIFICABILI tra ~1 mese, ognuna con condizione e "
             "data di verifica. Alimentano la scorecard a lungo raggio. Sii specifico e "
             "falsificabile, non vago. -->\n")
    L.append("| # | Affermazione verificabile | Condizione / metro | Verifica il |")
    L.append("|---|---|---|---|")
    L.append("| 1 | … | … | … |")
    L.append("")
    return "\n".join(L)


def render_html(md_path: Path, month: str) -> Path:
    """Rende il .md (bozza o compilato) in HTML impaginato, stesso stile dei report."""
    body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=MD_EXTENSIONS)
    html = (f"<!DOCTYPE html><html lang='it'><head><meta charset='UTF-8'>"
            f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
            f"<title>Report Strategico Mensile — {month}</title><style>{CSS}</style></head>"
            f"<body><section class='doc'>{body}</section></body></html>")
    out_html = md_path.with_suffix(".html")
    out_html.write_text(html, encoding="utf-8")
    return out_html


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--month", default=date.today().strftime("%Y-%m"),
                    help="Mese da sintetizzare, formato YYYY-MM (default: mese corrente).")
    ap.add_argument("--force", action="store_true", help="Rigenera anche se la bozza esiste.")
    ap.add_argument("--render-only", action="store_true",
                    help="NON rigenera la bozza: rende solo l'HTML dal .md esistente "
                         "(usalo DOPO che l'agente ha compilato le sezioni).")
    args = ap.parse_args()

    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    out_md = MONTHLY_DIR / f"{args.month}.md"

    if args.render_only:
        if not out_md.exists():
            print(f"[monthly] nessun .md da rendere: {out_md}")
            return
        out_html = render_html(out_md, args.month)
        print(f"[monthly] HTML rigenerato dal .md compilato: {out_html.name}")
        return

    if out_md.exists() and not args.force:
        print(f"[monthly] bozza già presente: {out_md} (usa --force per rigenerare).")
        return

    out_md.write_text(build_scaffold(args.month), encoding="utf-8")
    out_html = render_html(out_md, args.month)
    n_cards = len(discover_cards(args.month))
    print(f"[monthly] bozza scritta: {out_md.name} + {out_html.name} "
          f"({n_cards} schede aggregate). Ora l'agente compila le sezioni (PHASE6_RUNBOOK.md).")


if __name__ == "__main__":
    main()
