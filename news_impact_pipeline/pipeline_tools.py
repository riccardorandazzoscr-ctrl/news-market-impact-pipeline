#!/usr/bin/env python3
"""
pipeline_tools.py

Strumenti deterministici per la pipeline di analisi news (Fase 3).
Pensati per essere chiamati da Claude in sessione Claude Code via Bash:
l'agente esegue la classificazione semantica, poi invoca questi tool per
ottenere asset rilevanti e research correlate dalla knowledge base.

Uso CLI (esempi):
    venv/bin/python pipeline_tools.py assets monetary_policy
    venv/bin/python pipeline_tools.py assets geopolitical --level primary
    venv/bin/python pipeline_tools.py match --theme geopolitical \\
        --keyword "brexit" --keyword "sterling" --asset GBPUSD=X
    venv/bin/python pipeline_tools.py match --theme corporate_idiosyncratic \\
        --text "SpaceX IPO Nasdaq filing"
    venv/bin/python pipeline_tools.py list-categories

Uso programmatico (da altri script Python):
    from pipeline_tools import load_catalog, assets_for_category, match_research
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from parse_briefing import parse_briefing, briefing_path, available_dates


HERE = Path(__file__).parent
KB_DIR = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base"
CATALOG_PATH = KB_DIR / "catalog.yaml"
CATEGORY_MAP_PATH = HERE / "category_asset_map.yaml"
TEMPLATE_PATH = HERE / "news_card_template.md"
DAILY_ANALYSIS_DIR = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"


# Ontologia (Design Document §6.1) — duplicata qui per non importare da
# build_catalog (evitiamo dipendenze circolari fra moduli).
ONTOLOGY = {
    "monetary_policy",
    "fiscal_policy",
    "geopolitical",
    "macro_data",
    "corporate_idiosyncratic",
    "regulatory",
    "commodity_energy",
    "financial_stability",
    "structural_themes",
}


# --- Loader ----------------------------------------------------------------

def load_catalog() -> dict:
    """Legge knowledge_base/catalog.yaml. Errore esplicito se manca."""
    if not CATALOG_PATH.exists():
        raise SystemExit(
            f"catalog.yaml non trovato in {CATALOG_PATH}.\n"
            f"Eseguilo prima con: venv/bin/python build_catalog.py"
        )
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_category_map() -> dict:
    """Legge category_asset_map.yaml."""
    if not CATEGORY_MAP_PATH.exists():
        raise SystemExit(f"Mappa categoria→asset non trovata: {CATEGORY_MAP_PATH}")
    with CATEGORY_MAP_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# --- Lookup categoria → asset ---------------------------------------------

def assets_for_category(category: str, level: str = "all") -> list[str]:
    """
    Restituisce i ticker tipicamente esposti a una categoria.

    level: 'primary' (canale diretto), 'secondary' (effetti indiretti),
           'all' (entrambi, senza duplicati, primary prima).
    """
    if category not in ONTOLOGY:
        raise ValueError(
            f"Categoria '{category}' non e' nell'ontologia §6.1. "
            f"Categorie ammesse: {sorted(ONTOLOGY)}"
        )

    cmap = load_category_map()
    if category not in cmap:
        return []

    primary   = cmap[category].get("primary",   []) or []
    secondary = cmap[category].get("secondary", []) or []

    if level == "primary":
        return primary
    if level == "secondary":
        return secondary
    if level == "all":
        # dedup preservando ordine: primary prima, poi secondary nuovi.
        seen = set(primary)
        return primary + [a for a in secondary if a not in seen and not seen.add(a)]
    raise ValueError(f"level deve essere 'primary'|'secondary'|'all', ricevuto: {level}")


def category_info(category: str) -> dict:
    """Info complete su una categoria (description, horizon, primary, secondary)."""
    cmap = load_category_map()
    return cmap.get(category, {})


# --- Matching catalog ------------------------------------------------------

def _normalize(s: str) -> str:
    return s.lower().strip()


def _keyword_hits(query_text: str | None, query_keywords: list[str],
                  entry_keywords: list[str]) -> int:
    """
    Conta gli overlap fra le keyword della query (parole singole o frasi
    fornite dall'analista, opzionalmente anche un testo libero della notizia)
    e le keyword di una entry del catalog. Match case-insensitive su substring.
    """
    hits = 0
    entry_kw_norm = [_normalize(k) for k in entry_keywords]

    # 1) keyword esplicite della query verso keyword della entry
    for qk in query_keywords:
        qk_n = _normalize(qk)
        for ek in entry_kw_norm:
            if qk_n in ek or ek in qk_n:
                hits += 1
                break  # max 1 hit per keyword query

    # 2) testo libero notizia: cerco ogni keyword entry come substring
    if query_text:
        text_n = _normalize(query_text)
        for ek in entry_kw_norm:
            if ek and ek in text_n:
                hits += 1

    return hits


def match_research(theme: str | None = None,
                   sub_themes: list[str] | None = None,
                   keywords: list[str] | None = None,
                   assets: list[str] | None = None,
                   text: str | None = None,
                   min_score: int = 1) -> list[dict]:
    """
    Cerca nel catalog le research piu' pertinenti a una query.

    Scoring:
      +5  primary_theme match
      +2  per ogni sub_theme in comune
      +3  per ogni asset in comune (con relevant_assets della entry)
      +1  per ogni keyword hit (vedi _keyword_hits)

    Restituisce lista di dict ordinati per score decrescente. Ogni dict ha:
      score, source_file, title, primary_theme, matched_reasons (lista)
    Le entry con score < min_score vengono scartate.
    """
    sub_themes = sub_themes or []
    keywords   = keywords   or []
    assets     = assets     or []

    catalog = load_catalog()
    results = []

    for entry in catalog.get("entries", []):
        score = 0
        reasons = []

        # Theme match
        if theme and entry.get("primary_theme") == theme:
            score += 5
            reasons.append(f"primary_theme = {theme} (+5)")

        # Sub-theme overlap
        entry_subs = set(entry.get("sub_themes", []) or [])
        sub_overlap = entry_subs & set(sub_themes)
        if sub_overlap:
            score += 2 * len(sub_overlap)
            reasons.append(f"sub_themes match: {sorted(sub_overlap)} (+{2*len(sub_overlap)})")

        # Asset overlap (consideriamo solo quelli in relevant_assets, che sono
        # validati contro il DB; ignoriamo external_assets_mentioned)
        entry_assets = set(entry.get("relevant_assets", []) or [])
        asset_overlap = entry_assets & set(assets)
        if asset_overlap:
            score += 3 * len(asset_overlap)
            reasons.append(f"asset match: {sorted(asset_overlap)} (+{3*len(asset_overlap)})")

        # Keyword hits
        entry_kw = entry.get("keywords", []) or []
        hits = _keyword_hits(text, keywords, entry_kw)
        if hits:
            score += hits
            reasons.append(f"keyword hits = {hits} (+{hits})")

        if score >= min_score:
            results.append({
                "score": score,
                "source_file": entry.get("source_file"),
                "title": entry.get("title"),
                "primary_theme": entry.get("primary_theme"),
                "matched_reasons": reasons,
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


# --- CLI -------------------------------------------------------------------

def _print_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def cmd_assets(args):
    out = assets_for_category(args.category, level=args.level)
    if args.json:
        _print_json({"category": args.category, "level": args.level, "assets": out})
        return
    info = category_info(args.category)
    print(f"Categoria: {args.category}")
    if info.get("description"):
        print(f"  Descrizione: {info['description']}")
    if info.get("horizon"):
        print(f"  Orizzonte:   {info['horizon']}")
    print(f"  Asset ({args.level}):")
    for a in out:
        print(f"    - {a}")
    if not out:
        print("    (nessun asset diretto nel nostro universo cross-asset; vedi 'notes' nella mappa)")


def cmd_match(args):
    results = match_research(
        theme=args.theme,
        sub_themes=args.sub_theme or [],
        keywords=args.keyword or [],
        assets=args.asset or [],
        text=args.text,
        min_score=args.min_score,
    )
    if args.json:
        _print_json(results)
        return
    if not results:
        print("Nessuna research nel catalog ha raggiunto la soglia di pertinenza.")
        return
    print(f"Match nel catalog (ordinati per score):\n")
    for r in results:
        print(f"  [score={r['score']:>3}] {r['source_file']}")
        print(f"     {r['title']}")
        for reason in r['matched_reasons']:
            print(f"       · {reason}")
        print()


def cmd_new_card(args):
    """Crea daily_analysis/YYYY-MM-DD/news_NN.md pre-popolato dal template."""
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template non trovato: {TEMPLATE_PATH}")

    day = args.date or date.today().isoformat()
    day_dir = DAILY_ANALYSIS_DIR / day
    day_dir.mkdir(parents=True, exist_ok=True)

    # Trova il prossimo numero progressivo libero (news_01, news_02, ...)
    existing = sorted(day_dir.glob("news_*.md"))
    used_nums = []
    for f in existing:
        m = re.match(r"news_(\d+)", f.stem)
        if m:
            used_nums.append(int(m.group(1)))
    next_n = (max(used_nums) + 1) if used_nums else 1
    card_path = day_dir / f"news_{next_n:02d}.md"

    # Catalog timestamp (per provenance)
    catalog_ts = "n/a"
    if CATALOG_PATH.exists():
        try:
            cat = load_catalog()
            catalog_ts = cat.get("generated_at", "n/a")
        except Exception:
            pass

    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}":            args.title or "(titolo da compilare)",
        "{{DATE}}":             day,
        "{{SOURCE}}":           args.source or "(fonte da compilare)",
        "{{SLUG}}":             args.slug or "(slug da compilare)",
        "{{NEWS_TEXT}}":        args.text or "(incolla qui il testo della notizia)",
        "{{PRIMARY_THEME}}":    args.theme or "(da compilare — vedi list-categories)",
        "{{SUB_THEMES}}":       ", ".join(args.sub_theme or []) or "(da compilare)",
        "{{SENTIMENT}}":        args.sentiment or "(da compilare)",
        "{{CONFIDENCE}}":       args.confidence or "(da compilare)",
        "{{HORIZON}}":          args.horizon or "(da compilare)",
        "{{CATALOG_TIMESTAMP}}": catalog_ts,
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    card_path.write_text(text, encoding="utf-8")
    if args.json:
        _print_json({"path": str(card_path), "day": day, "n": next_n})
    else:
        print(f"Scheda creata: {card_path}")
        print(f"Modificala con un editor per riempire i campi rimanenti.")


def cmd_list_categories(args):
    cmap = load_category_map()
    if args.json:
        _print_json([{"category": c, **{k: v for k, v in info.items() if k != "notes"}}
                     for c, info in cmap.items()])
        return
    print("Categorie dell'ontologia §6.1:\n")
    for c in sorted(ONTOLOGY):
        info = cmap.get(c, {})
        desc = info.get("description", "(no description)")
        horizon = info.get("horizon", "")
        n_primary = len(info.get("primary", []) or [])
        n_secondary = len(info.get("secondary", []) or [])
        print(f"  {c}")
        print(f"     {desc}")
        if horizon:
            print(f"     orizzonte: {horizon}")
        print(f"     asset: {n_primary} primary, {n_secondary} secondary\n")


def _truncate(text: str, n: int = 160) -> str:
    """Accorcia il corpo per la cella di triage (il testo pieno e' nel briefing)."""
    text = text.strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def cmd_digest(args):
    """Crea daily_analysis/YYYY-MM-DD/_index.md: scaffold di triage del briefing.

    Pre-popola la tabella con tutte le 20 notizie + il watch del briefing.
    L'analista (agente) compila la colonna Decisione (✅ scheda / ✖ scarto) e
    la motivazione, e linka le schede news_NN.md create per gli item tenuti.
    """
    day = args.date or date.today().isoformat()

    # Briefing: file esplicito o quello atteso per la data.
    if args.file:
        bpath = Path(args.file).expanduser()
    else:
        bpath = briefing_path(date.fromisoformat(day))
    try:
        parsed = parse_briefing(bpath)
    except FileNotFoundError as e:
        avail = available_dates()
        hint = f" Disponibili: {avail[0]} … {avail[-1]}." if avail else ""
        raise SystemExit(f"{e}.{hint}")

    day_dir = DAILY_ANALYSIS_DIR / day
    day_dir.mkdir(parents=True, exist_ok=True)
    index_path = day_dir / "_index.md"
    if index_path.exists() and not args.force:
        raise SystemExit(
            f"{index_path} esiste gia'. Usa --force per rigenerarlo "
            f"(attenzione: sovrascrive le decisioni di triage gia' inserite)."
        )

    catalog_ts = "n/a"
    if CATALOG_PATH.exists():
        try:
            catalog_ts = load_catalog().get("generated_at", "n/a")
        except Exception:
            pass

    lines = [
        f"# Daily Analysis — {day}",
        "",
        f"- **Briefing:** `{parsed['source_file']}`",
        f"- **Generato:** {date.today().isoformat()}",
        f"- **Catalog KB:** {catalog_ts}",
        "",
        "Triage del briefing del giorno. Per ogni notizia: decisione "
        "(✅ = scheda prodotta, ✖ = scartata), tema/motivazione, e link alla "
        "scheda `news_NN.md` quando prodotta. Scope: subset triato — scheda "
        "completa solo per notizie che mappano sui 17 asset in DB e hanno un "
        "analogo storico plausibile.",
        "",
        "## Triage",
        "",
        "| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |",
        "|---|------|---------|-----------|--------------------|--------|",
    ]
    sec_short = {"international": "intl", "finance": "fin"}
    for label in ("international", "finance"):
        for s in parsed["sections"].get(label, []):
            num = s["num"] or "—"
            title = s["title"].replace("|", "\\|")
            lines.append(
                f"| {num} | {sec_short[label]} | {title} | ⏳ | | |"
            )

    lines += ["", "## 🔍 One Thing to Watch Today", ""]
    if parsed.get("watch"):
        lines.append(f"**{parsed['watch']['title']}**")
        lines.append("")
        lines.append(parsed["watch"]["body"])
    else:
        lines.append("_(assente nel briefing)_")

    lines += [
        "",
        "## Sintesi di sessione",
        "",
        "_(nota dell'analista: temi dominanti del giorno, episodi storici "
        "selezionati, letture trasversali. Da compilare dopo il triage.)_",
        "",
    ]

    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    n_items = sum(len(parsed["sections"].get(l, [])) for l in ("international", "finance"))
    if args.json:
        _print_json({"index": str(index_path), "day": day, "items": n_items})
    else:
        print(f"Digest creato: {index_path}")
        print(f"  {n_items} notizie in triage (⏳). Compila Decisione + Motivazione,")
        print(f"  poi crea le schede con: pipeline_tools.py new-card --date {day} ...")


def main():
    p = argparse.ArgumentParser(description="Strumenti pipeline news (Fase 3)")
    sub = p.add_subparsers(dest="command", required=True)

    # assets
    pa = sub.add_parser("assets", help="Asset rilevanti per una categoria")
    pa.add_argument("category", help="Nome categoria (vedi list-categories)")
    pa.add_argument("--level", choices=["primary", "secondary", "all"],
                    default="all")
    pa.add_argument("--json", action="store_true", help="Output JSON")
    pa.set_defaults(func=cmd_assets)

    # match
    pm = sub.add_parser("match", help="Cerca research correlate nel catalog")
    pm.add_argument("--theme", help="primary_theme della notizia (es. monetary_policy)")
    pm.add_argument("--sub-theme", action="append", help="Sub-tema (ripetibile)")
    pm.add_argument("--keyword",  action="append", help="Keyword (ripetibile)")
    pm.add_argument("--asset",    action="append", help="Ticker rilevante (ripetibile)")
    pm.add_argument("--text",     help="Testo libero della notizia (per keyword match)")
    pm.add_argument("--min-score", type=int, default=1)
    pm.add_argument("--json", action="store_true")
    pm.set_defaults(func=cmd_match)

    # list-categories
    pl = sub.add_parser("list-categories", help="Elenco delle 9 categorie")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_list_categories)

    # new-card
    pn = sub.add_parser("new-card", help="Crea una scheda notizia pre-popolata in daily_analysis/")
    pn.add_argument("--date",       help="AAAA-MM-GG (default: oggi)")
    pn.add_argument("--slug",       help="Slug breve (es. 'ecb-rate-hold')")
    pn.add_argument("--title",      help="Titolo della scheda")
    pn.add_argument("--source",     help="Fonte (es. Reuters, FT, briefing del giorno)")
    pn.add_argument("--text",       help="Testo della notizia")
    pn.add_argument("--theme",      help="primary_theme (vedi list-categories)")
    pn.add_argument("--sub-theme",  action="append", help="Sub-tema (ripetibile)")
    pn.add_argument("--sentiment",  help="hawkish/dovish/bullish/bearish/risk-on/risk-off/neutral")
    pn.add_argument("--confidence", choices=["low", "medium", "high"])
    pn.add_argument("--horizon",    help="Orizzonte atteso (es. '1-5 giorni')")
    pn.add_argument("--json", action="store_true")
    pn.set_defaults(func=cmd_new_card)

    # digest
    pd = sub.add_parser("digest", help="Crea lo scaffold _index.md di triage del briefing del giorno")
    pd.add_argument("--date", help="AAAA-MM-GG (default: oggi)")
    pd.add_argument("--file", help="Percorso esplicito al briefing HTML (override di --date)")
    pd.add_argument("--force", action="store_true", help="Rigenera _index.md anche se esiste")
    pd.add_argument("--json", action="store_true")
    pd.set_defaults(func=cmd_digest)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
