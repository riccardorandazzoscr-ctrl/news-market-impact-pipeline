#!/usr/bin/env python3
"""Refuse to mark a monthly report done while template sections remain empty."""

import re
import sys
from pathlib import Path


def validate(path: Path) -> list[str]:
    text = path.read_text()
    start = text.find("## 1. Mappa dei regimi attivi")
    if start < 0:
        return ["sezione 1 mancante"]
    text = text[start:]
    headings = list(re.finditer(r"^## ([1-6])\. ", text, re.M))
    if [int(match.group(1)) for match in headings] != list(range(1, 7)):
        return ["le sei sezioni non sono presenti nell'ordine previsto"]
    problems = []
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[match.end():end]
        body = re.sub(r"<!--.*?-->", "", section, flags=re.S).strip()
        if len(body) < 80 or "…" in body:
            problems.append(f"sezione {index + 1} vuota o con segnaposto")
        if index == 5 and len(re.findall(r"^\|\s*\d+\s*\|", body, re.M)) < 3:
            problems.append("meno di tre previsioni falsificabili")
    return problems


if __name__ == "__main__":
    errors = validate(Path(sys.argv[1]))
    if errors:
        print("Report mensile incompleto: " + "; ".join(errors), file=sys.stderr)
        sys.exit(1)
