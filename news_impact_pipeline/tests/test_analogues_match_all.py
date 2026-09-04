#!/usr/bin/env python
"""Sessione di test per il flag --match-all di analogues.py find.

Strategia:
  - ORACOLO INDIPENDENTE: ricalcola il pool atteso direttamente da _episodes.yaml,
    con un predicato scritto in forma diversa da quello sotto test (lista di hit
    per token, poi all/any) — così un errore di quantificatore non si replica.
  - ISOLAMENTO DEL PREDICATO: le chiamate usano --min-n 0 (mai degrado: strict
    passa sempre) e --max-pool 0 (nessun cap), così l'output E' il set filtrato.
  - MATRICE AMPIA: tutte le coppie dei token piu' frequenti di ogni tema, piu'
    triple, piu' casi limite.
  - INVARIANTI: proprieta' che devono valere sempre, non solo sui casi scelti.
"""
import io
import itertools
import subprocess
import sys
from collections import defaultdict
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

PIPE = Path.home() / "Claude/mercati_finanza/news_impact_pipeline"
sys.path.insert(0, str(PIPE))
import analogues  # noqa: E402

EPS = analogues._load()
analogues._load = lambda: EPS          # cache: evita di rileggere lo yaml ogni volta

FAILS = []
CHECKS = 0


def check(cond, label, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(f"{label}  {detail}")


def run(theme, tokens=None, match_all=False, direction=None, before=None,
        min_n=0, max_pool=0):
    """Chiama cmd_find catturando stdout (date) e stderr (nota)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        analogues.cmd_find(theme, direction, before, tokens, min_n, max_pool,
                           match_all)
    dates = [d for d in out.getvalue().strip().split(",") if d]
    return dates, err.getvalue()


def oracle(theme, tokens, mode, before=None, field="subthemes_local"):
    """Oracolo indipendente: hit per token, poi all/any. Forma diversa dal SUT."""
    wanted = [analogues._norm_label(t) for t in tokens]
    dates = set()
    for e in EPS:
        if e["theme"] != theme:
            continue
        if before and e["date"] >= before:
            continue
        labels = e.get(field) or []
        hits = []
        for w in wanted:
            found = False
            for st in labels:
                if w in st:
                    found = True
                    break
            hits.append(found)
        if (all(hits) if mode == "and" else any(hits)):
            dates.add(e["date"])
    return sorted(dates)


# ---------------------------------------------------------------- token reali
by_theme = defaultdict(lambda: defaultdict(int))
for e in EPS:
    for t in e.get("subthemes_local") or []:
        by_theme[e["theme"]][t] += 1

THEMES = sorted(by_theme)
TOP = {t: [k for k, _ in sorted(by_theme[t].items(), key=lambda kv: -kv[1])[:8]]
       for t in THEMES}

print("=" * 78)
print("SESSIONE DI TEST — analogues.py find --match-all")
print("=" * 78)
print(f"\nLibreria: {len(EPS)} episodi · {len(THEMES)} temi")
print(f"Temi: {', '.join(THEMES)}\n")

# ============================================================ 1. MATRICE COPPIE
print("-" * 78)
print("1. MATRICE — tutte le coppie dei top-8 token per tema (OR e AND)")
print("-" * 78)
pairs = 0
shrink = []
for th in THEMES:
    for a, b in itertools.combinations(TOP[th], 2):
        pairs += 1
        d_or, n_or = run(th, [a, b])
        d_and, n_and = run(th, [a, b], match_all=True)
        exp_or = oracle(th, [a, b], "or")
        exp_and = oracle(th, [a, b], "and")

        check(d_or == exp_or, "INV1 OR≠oracolo", f"{th} {a}+{b}: {len(d_or)} vs {len(exp_or)}")
        check(d_and == exp_and, "INV2 AND≠oracolo", f"{th} {a}+{b}: {len(d_and)} vs {len(exp_and)}")
        check(set(d_and) <= set(d_or), "INV3 AND⊄OR", f"{th} {a}+{b}")
        check("(unione)" in n_or, "INV-nota OR senza modalità", f"{th} {a}+{b}")
        check("(INTERSEZIONE)" in n_and, "INV-nota AND senza modalità", f"{th} {a}+{b}")

        # commutatività
        check(run(th, [b, a])[0] == d_or, "INV5 OR non commutativo", f"{th} {a}+{b}")
        check(run(th, [b, a], match_all=True)[0] == d_and, "INV5 AND non commutativo", f"{th} {a}+{b}")

        if d_or:
            shrink.append((len(d_and) / len(d_or), th, a, b, len(d_or), len(d_and)))

print(f"  coppie testate: {pairs}  ·  asserzioni finora: {CHECKS}")
shrink.sort()
print("\n  Coppie dove l'intersezione taglia di piu' (AND/OR piu' basso):")
for r, th, a, b, n_or, n_and in shrink[:6]:
    print(f"    {th:20s} {a}+{b}: OR {n_or:3d} → AND {n_and:3d}  ({r:.0%})")
print("\n  Coppie dove non taglia nulla (AND == OR → token ridondanti):")
same = [s for s in shrink if s[0] == 1.0]
for r, th, a, b, n_or, n_and in same[:4]:
    print(f"    {th:20s} {a}+{b}: {n_or} = {n_and}")
print(f"    (totale coppie con AND==OR: {len(same)}/{len(shrink)})")

# ============================================================== 2. TRIPLE
print("\n" + "-" * 78)
print("2. TRIPLE — 3 token insieme (l'AND deve stringere monotonicamente)")
print("-" * 78)
triples = 0
for th in THEMES:
    for a, b, c in itertools.islice(itertools.combinations(TOP[th], 3), 12):
        triples += 1
        d3, _ = run(th, [a, b, c], match_all=True)
        exp3 = oracle(th, [a, b, c], "and")
        check(d3 == exp3, "INV2 AND3≠oracolo", f"{th} {a}+{b}+{c}")
        # monotonicità: AND su 3 token ⊆ AND su ogni sua coppia
        for x, y in itertools.combinations([a, b, c], 2):
            sub, _ = run(th, [x, y], match_all=True)
            check(set(d3) <= set(sub), "INV-monotonia AND3⊄AND2", f"{th} {a}+{b}+{c} vs {x}+{y}")
print(f"  triple testate: {triples}  ·  asserzioni finora: {CHECKS}")

# ============================================================== 3. CASI LIMITE
print("\n" + "-" * 78)
print("3. CASI LIMITE")
print("-" * 78)
th = "macro_data"
tok = TOP[th][0]

# 3.1 token singolo: AND == OR, e la nota NON deve dichiarare modalità
d1, n1 = run(th, [tok])
d1a, n1a = run(th, [tok], match_all=True)
check(d1 == d1a, "LIM1 token singolo AND≠OR")
check("(unione)" not in n1 and "(INTERSEZIONE)" not in n1a, "LIM1 modalità dichiarata su token singolo")
print(f"  3.1 token singolo          OR={len(d1):3d}  AND={len(d1a):3d}  → identici, nessuna dicitura  ✓")

# 3.2 token duplicato: AND(a,a) == singolo(a)
d_dup, n_dup = run(th, [tok, tok], match_all=True)
check(d_dup == d1, "LIM2 AND(a,a)≠singolo", f"{len(d_dup)} vs {len(d1)}")
print(f"  3.2 token duplicato a+a    AND={len(d_dup):3d}  → uguale al singolo  ✓")

# 3.3 token inesistente
d_ghost, n_ghost = run(th, ["token_che_non_esiste_xyz"], match_all=True)
check(d_ghost == [], "LIM3 token inesistente non vuoto", f"{len(d_ghost)}")
d_mix, _ = run(th, [tok, "token_che_non_esiste_xyz"], match_all=True)
check(d_mix == [], "LIM4 AND con token inesistente non vuoto", f"{len(d_mix)}")
d_mix_or, _ = run(th, [tok, "token_che_non_esiste_xyz"])
check(d_mix_or == d1, "LIM5 OR con token inesistente ≠ singolo")
print(f"  3.3 token inesistente      AND=0 ✓ · AND(reale,fantasma)=0 ✓ · OR(reale,fantasma)={len(d_mix_or)} = singolo ✓")

# 3.4 nessun subtheme (None) — il flag non deve avere effetto
d_none, _ = run(th, None)
d_none_a, _ = run(th, None, match_all=True)
check(d_none == d_none_a, "LIM6 --match-all cambia il pool senza --subtheme")
print(f"  3.4 senza --subtheme       {len(d_none)} = {len(d_none_a)} → flag inerte  ✓")

# 3.5 lista vuota
d_empty, _ = run(th, [], match_all=True)
check(d_empty == d_none, "LIM7 lista token vuota ≠ nessun filtro")
print(f"  3.5 lista token vuota      {len(d_empty)} = {len(d_none)}  ✓")

# 3.6 normalizzazione (maiuscole / spazi)
d_norm, _ = run(th, [tok.upper(), TOP[th][1]], match_all=True)
d_base, _ = run(th, [tok, TOP[th][1]], match_all=True)
check(d_norm == d_base, "LIM8 normalizzazione maiuscole rotta", f"{len(d_norm)} vs {len(d_base)}")
d_sp, _ = run(th, [f"  {tok}  ", TOP[th][1]], match_all=True)
check(d_sp == d_base, "LIM9 normalizzazione spazi rotta", f"{len(d_sp)} vs {len(d_base)}")
print(f"  3.6 maiuscole / spazi      {len(d_norm)} = {len(d_sp)} = {len(d_base)}  ✓")

# ==================================================== 4. INTERAZIONE CON ALTRI FLAG
print("\n" + "-" * 78)
print("4. INTERAZIONE CON --before / --direction / --max-pool / --min-n")
print("-" * 78)
pair = (TOP[th][0], TOP[th][1])

# 4.1 no look-ahead in entrambe le modalità
CUT = "2024-01-01"
for ma in (False, True):
    d_b, _ = run(th, list(pair), match_all=ma, before=CUT)
    check(all(x < CUT for x in d_b), "INT1 look-ahead!", f"match_all={ma}")
    check(d_b == oracle(th, list(pair), "and" if ma else "or", before=CUT),
          "INT2 before≠oracolo", f"match_all={ma}")
print(f"  4.1 --before {CUT}    nessuna data ≥ cutoff, in OR e AND  ✓")

# 4.2 cap di recency
for ma in (False, True):
    d_cap, n_cap = run(th, list(pair), match_all=ma, max_pool=5)
    check(len(d_cap) <= 5, "INT3 cap non rispettato", f"match_all={ma}: {len(d_cap)}")
    full, _ = run(th, list(pair), match_all=ma)
    check(d_cap == full[-5:] if len(full) > 5 else d_cap == full,
          "INT4 cap non tiene i più recenti", f"match_all={ma}")
print(f"  4.2 --max-pool 5           rispettato e tiene i più recenti, in OR e AND  ✓")

# 4.3 direzione combinata
for d in ("pos", "neg", "neutral"):
    dd, nn = run(th, list(pair), match_all=True, direction=d, min_n=1)
    base, _ = run(th, list(pair), match_all=True, min_n=1)
    check(set(dd) <= set(base), "INT5 direzione allarga il pool AND", f"dir={d}")
print(f"  4.3 --direction pos/neg/neutral  il pool resta ⊆ del pool AND  ✓")

# 4.4 degrado: la nota deve avvisare che l'intersezione non è più garantita
found_degrade = None
for th2 in THEMES:
    for a, b in itertools.combinations(TOP[th2], 2):
        strict = oracle(th2, [a, b], "and")
        loose = oracle(th2, [a, b], "and", field="subthemes")
        if len(strict) < 12 <= len(loose):
            found_degrade = (th2, a, b, len(strict), len(loose))
            break
    if found_degrade:
        break
if found_degrade:
    th2, a, b, ns, nl = found_degrade
    _, note = run(th2, [a, b], match_all=True, min_n=12)
    check("NON è più garantita" in note, "INT6 degrado a documento non avvisato",
          f"{th2} {a}+{b}")
    print(f"  4.4 degrado → documento    {th2} {a}+{b} (locali {ns} < 12 ≤ doc {nl}): avviso presente  ✓")
else:
    print("  4.4 degrado → documento    nessun caso naturale trovato nella matrice")

# 4.5 degrado fino al pool del tema: deve riportare il conteggio dell'unione
_, note_theme = run(th, list(pair), match_all=True, min_n=9999)
check("richiesta INTERSEZIONE" in note_theme, "INT7 degrado a tema senza avviso AND")
check("in unione gli stessi token danno" in note_theme, "INT8 manca il conteggio dell'unione")
print(f"  4.5 degrado → pool del tema  avviso + conteggio dell'unione presenti  ✓")

# ==================================================== 5. CLI END-TO-END
print("\n" + "-" * 78)
print("5. CLI END-TO-END (subprocess: parsing argomenti, exit code)")
print("-" * 78)
PY = str(PIPE / "venv/bin/python")


def cli(*args):
    return subprocess.run([PY, "analogues.py", "find", *args], cwd=PIPE,
                          capture_output=True, text=True)


c1 = cli("--theme", th, "--subtheme", pair[0], "--subtheme", pair[1],
         "--min-n", "0", "--max-pool", "0")
c2 = cli("--theme", th, "--subtheme", pair[0], "--subtheme", pair[1],
         "--match-all", "--min-n", "0", "--max-pool", "0")
check(c1.returncode == 0 and c2.returncode == 0, "CLI1 exit code non zero")
cli_or = [d for d in c1.stdout.strip().split(",") if d]
cli_and = [d for d in c2.stdout.strip().split(",") if d]
check(cli_or == oracle(th, list(pair), "or"), "CLI2 OR da CLI ≠ oracolo")
check(cli_and == oracle(th, list(pair), "and"), "CLI3 AND da CLI ≠ oracolo")
print(f"  5.1 exit code 0 · OR={len(cli_or)} AND={len(cli_and)} coerenti con l'oracolo  ✓")

c3 = cli("--theme", th, "--match-all")          # flag senza --subtheme
check(c3.returncode == 0, "CLI4 --match-all senza --subtheme fallisce")
c4 = cli("--theme", "tema_inesistente", "--subtheme", "x", "--match-all")
check(c4.returncode == 0, "CLI5 tema inesistente fallisce")
check(c4.stdout.strip() == "", "CLI6 tema inesistente restituisce date")
c5 = cli("--theme", th, "--subtheme", pair[0], "--match-all", "--direction", "pos",
         "--before", "2025-06-01")
check(c5.returncode == 0, "CLI7 combinazione completa fallisce")
print(f"  5.2 flag senza --subtheme ✓ · tema inesistente ✓ · combinazione completa ✓")

# help
c6 = cli("--help")
check("--match-all" in c6.stdout, "CLI8 --match-all assente dall'help")
print(f"  5.3 --match-all documentato in --help  ✓")

# ==================================================== 6. REGRESSIONE GLOBALE
print("\n" + "-" * 78)
print("6. REGRESSIONE — il default deve replicare la semantica PRE-modifica")
print("-" * 78)


def legacy_match(theme, tokens, field="subthemes_local"):
    """Predicato ORIGINALE, copiato letteralmente da prima della modifica."""
    wanted = [analogues._norm_label(s) for s in tokens]
    return sorted({e["date"] for e in EPS if e["theme"] == theme
                   and any(w in st for w in wanted
                           for st in (e.get(field) or []))})


reg = 0
for th2 in THEMES:
    for a, b in itertools.combinations(TOP[th2], 2):
        reg += 1
        d, _ = run(th2, [a, b])
        check(d == legacy_match(th2, [a, b]), "REG default cambiato!", f"{th2} {a}+{b}")
    for a in TOP[th2]:
        reg += 1
        d, _ = run(th2, [a])
        check(d == legacy_match(th2, [a]), "REG default cambiato (singolo)!", f"{th2} {a}")
print(f"  {reg} combinazioni confrontate col predicato originale  ✓")

# ==================================================== ESITO
print("\n" + "=" * 78)
print(f"ASSERZIONI: {CHECKS}   ·   FALLITE: {len(FAILS)}")
print("=" * 78)
if FAILS:
    for f in FAILS[:40]:
        print("  ✗", f)
    sys.exit(1)
print("Tutte verdi.")
