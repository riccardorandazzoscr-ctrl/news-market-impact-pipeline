# Anteprima settimanale dal calendario — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** un job della domenica sera che, per ogni evento macro e di banca centrale della settimana
successiva, mostra i due scenari storici condizionali (con N), le research collegate, un commento
e una bozza LinkedIn.

**Architecture:** `weekly_preview.py` è deterministico. Legge il calendario (FRED più un file
YAML delle banche centrali), costruisce i pool con `analogues.cmd_find` (stdout catturato, senza
modificare `analogues.py`) e le statistiche con `event_study.run_event_study`, poi scrive
`tabelle.json` e `tabelle.md`. `run_weekly_preview.sh` aggiunge un run breve di `claude -p` per
il testo, lo valida, rende l'HTML e lo invia su Telegram con curl.

**Tech Stack:** Python 3 nel venv del progetto (pyyaml, pandas, markdown già installati), zsh,
launchd, API FRED, Claude Code headless.

**Spec:** `docs/superpowers/specs/2026-10-17-anteprima-settimanale-design.md`

## Global Constraints

- Tutto gira con `news_impact_pipeline/venv/bin/python`; nessuna dipendenza nuova.
- Nessuna API key Anthropic: il testo lo scrive `claude -p` (`MODEL="claude-opus-5-5"`), come in `run_monthly_report.sh`.
- No look-ahead: i pool usano `before = as_of`, le statistiche `as_of = as_of`.
- Si riporta sempre N. Con N<10 lo scenario è `indicativo`, con N<5 `insufficiente`.
- Statistica descrittiva, non previsione: ogni bozza LinkedIn chiude con N e con la frase esatta «statistica descrittiva, non una previsione».
- Gli indicatori calcolati non si persistono nel DB; vivono solo in `weekly_preview/AAAA-Www/`.
- Commenti nel codice, documenti, report e bozze in italiano; messaggi di commit in inglese, chiusi da `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Commit solo quando il maintainer lo chiede.** Mai `git add -A`. I passi «Commit» qui sotto elencano i file da aggiungere uno per uno.
- **Non importare `cpi_lab_auto.py`**: resta locale e non versionato. Il deduplicatore degli avvisi si riscrive qui (deviazione dalla spec, che citava `cpi_lab_auto.alert`).
- I job launchd girano da `/Users/riccardo/Claude/mercati_finanza`. La copia viva del plist sta in `~/Library/LaunchAgents/`: va copiata e ricaricata.

## Review Focus

1. **Stesso giorno, due eventi** (il 2026-10-29 escono insieme PIL e PCE): devono restare due eventi distinti, con id distinti, nello stesso report. Il test va nel Task 1.
2. **Ripresa a metà settimana**: se il Mac si accende martedì, gli eventi di lunedì già passati non compaiono, quelli da oggi in poi sì. Test nel Task 1 (`target_week`, filtro `>= as_of`).
3. **Nessun evento mappato con analoghi sufficienti** (per esempio una settimana con solo BCE e BoE): niente run del modello, report con calendario e lacune. Test nel Task 4 (render senza testo) e passo nel Task 5.
4. **Il modello inventa una cifra o omette la frase di chiusura**: il validatore deve rifiutare e il report deve uscire con le sole tabelle. Test nel Task 3.
5. **Cifre con la virgola decimale e col segno** («−0,73%»): il validatore deve riconoscerle come le stesse cifre della tabella. Test nel Task 3.

## File

| File | Responsabilità |
|---|---|
| `news_impact_pipeline/weekly_preview.py` (nuovo) | calendario, scenari, `build`, `validate`, `render`, `check-calendar` |
| `news_impact_pipeline/anteprima_eventi.yaml` (nuovo) | tipo di evento → tema, sotto-temi, riferimento, scenari, asset |
| `news_impact_pipeline/calendario_banche_centrali.yaml` (nuovo) | riunioni da 2026-10-19 a 2027-12-31 |
| `news_impact_pipeline/weekly_preview_prompt.md` (nuovo) | prompt del modello fra `=== PROMPT START/END ===` |
| `news_impact_pipeline/run_weekly_preview.sh` (nuovo) | job: rete, build, modello, validate, render, Telegram |
| `news_impact_pipeline/launchd/com.riccardo.newsimpact.weeklypreview.plist` (nuovo) | ottavo job |
| `news_impact_pipeline/tests/test_weekly_preview.py` (nuovo) | suite offline |
| `news_impact_pipeline/run_tests.sh` | registra la suite (filtro `anteprima`) |
| `.gitignore` | `weekly_preview/` è output, come `daily_analysis/*` |
| `references/routine_giornaliera.md`, `CLAUDE.md`, `../CLAUDE.md`, `MEMORY.md` | da 7 a 8 job, riga del job, filone nuovo |

---

### Task 1: Ingressi e calendario della settimana

**Files:**
- Create: `news_impact_pipeline/anteprima_eventi.yaml`, `news_impact_pipeline/calendario_banche_centrali.yaml`, `news_impact_pipeline/weekly_preview.py`
- Test: `news_impact_pipeline/tests/test_weekly_preview.py`

**Interfaces:**
- Produces:
  - `EVENTS_MAP: Path`, `CB_CALENDAR: Path`, `PREVIEW_DIR: Path` (= repo root `/ "weekly_preview"`), `ROME = ZoneInfo("Europe/Rome")`
  - `load_events_map(path: Path = EVENTS_MAP) -> dict[str, dict]`
  - `load_cb_calendar(path: Path = CB_CALENDAR) -> list[dict]`: righe con `bank`, `decision: date`, `reaction_session: date`, `time_local: str`
  - `fred_dates(release_id: int, start: date, end: date) -> list[date]`: rete, `FRED_API_KEY` letto da `~/Claude/.env`
  - `target_week(now: datetime) -> date | None`: il lunedì della settimana da preparare
  - `week_events(monday: date, as_of: date, fred=fred_dates, cb: list[dict] | None = None, events_map: dict | None = None) -> list[dict]`. Ogni evento ha `id` (`f"{reaction_session}:{event_type}"`), `event_type`, `label`, `reaction_session: date`, `time_rome: str` («HH:MM»), `mapped: bool`. Lista ordinata per (`reaction_session`, `time_rome`, `event_type`).

**Contenuto pinnato di `anteprima_eventi.yaml`** (pool misurati il 2026-10-17 con `strict=True`, `min_n=12`; servono solo a orientarsi, non vanno copiati nel file). Ogni voce ha `label`, `theme`, `subthemes`, `match_all`, `reference`, `scenarios: {pos, neg}`, `assets`, `match_query`, più `fred_release_id` oppure `bank`:

| voce | sorgente | theme / subthemes | reference | pos / neg (a parole) | assets | pool oggi |
|---|---|---|---|---|---|---|
| `us_cpi` | fred 10 | macro_data / [us_cpi] | `^TNX` | sopra / sotto attese | `^TNX, ^FVX, IEF, DX-Y.NYB, ^GSPC, GC=F, EURUSD=X, JPY=X` | 17 / 14 |
| `us_nfp` | fred 50 | macro_data / [nfp] | `^TNX` | sopra / sotto attese | come `us_cpi` | 16 / 11 |
| `us_pce` | fred 54 | macro_data / [inflation_print] | `^TNX` | sopra / sotto attese | come `us_cpi` | 24 / 16 |
| `us_gdp` | fred 53 | macro_data / [activity_growth] | `^TNX` | sopra / sotto attese | come `us_cpi` | 15 / 11 |
| `us_retail` | fred 9 | macro_data / [consumer] | `IEF` | sotto attese (prezzo su) / sopra attese | come `us_cpi` più `XLY` se in DB | 13 / 12 |
| `fed_decision` | bank `fed` | monetary_policy / [rate_decision] | `IEF` | più accomodante / più restrittiva delle attese | `IEF, ^TNX, ^FVX, DX-Y.NYB, ^GSPC, GC=F, EURUSD=X, JPY=X` | 2 / 12 |
| `ecb_decision` | bank `ecb` | monetary_policy / [ecb] | `EURUSD=X` | più restrittiva / più accomodante | `EURUSD=X, IEAG.AS, ^STOXX50E, BTP_BUND_SPREAD` | 2 / 0 |
| `boj_decision` | bank `boj` | monetary_policy / [boj] | `JPY=X` | più accomodante / più restrittiva | `JPY=X, 1482.T, ^N225, ^TNX` | 8 / 2 |
| `boe_decision` | bank `boe` | monetary_policy / [rate_decision, britain_release], `match_all: true` | `GBPUSD=X` | più restrittiva / più accomodante | `GBPUSD=X, IGLT.L, ^FTSE` se in DB | 0 / 0 |
| `pboc_lpr` | bank `pboc` | monetary_policy / [pboc] | `CNY=X` | allentamento (yuan debole) / stretta | `CNY=X, ^HSI, HG=F, EEM` se in DB | 26 / 5 |

Orari: i rilasci FRED alle 08:30 America/New_York. `time_local` del file: Fed «14:00 America/New_York», BCE «14:15 Europe/Berlin», BoJ «12:00 Asia/Tokyo», BoE «12:00 Europe/London», PBOC «09:15 Asia/Shanghai».

**`calendario_banche_centrali.yaml`**: le date di Fed, BCE, BoJ e BoE dal 2026-10-19 al 2027-12-31 vanno prese dalle pagine ufficiali (federalreserve.gov, ecb.europa.eu, boj.or.jp, bankofengland.co.uk), con un commento `# fonte: <URL>` per banca. Non si scrivono a memoria.
- Fed e BCE: `reaction_session = decision`.
- BoJ: `reaction_session = decision` (annuncio in seduta di Tokyo).
- PBOC: LPR il 20 del mese, spostato al primo giorno feriale successivo, solo per i 3 mesi a venire, con `source: regola`. Commento `# ponytail: festività cinesi non gestite; verificare su pbc.gov.cn se il 20 cade in una festività`.
- Se una data ufficiale non è trovabile, la riga non entra.

- [ ] **Step 1: Scrivi i test che falliscono**

```python
MAP = {"us_cpi": {"label": "CPI USA", "fred_release_id": 10, "theme": "macro_data", ...},
       "us_gdp": {"label": "PIL USA", "fred_release_id": 53, ...},
       "us_pce": {"label": "PCE USA", "fred_release_id": 54, ...},
       "boj_decision": {"label": "Decisione BoJ", "bank": "boj", ...}}
CB = [{"bank": "boj", "decision": date(2026,10,30), "reaction_session": date(2026,10,30), "time_local": "12:00 Asia/Tokyo"},
      {"bank": "snb", "decision": date(2026,10,29), "reaction_session": date(2026,10,29), "time_local": "09:30 Europe/Zurich"}]
FRED = {10: [date(2026,11,10)], 53: [date(2026,10,29)], 54: [date(2026,10,29)]}
fake_fred = lambda rid, start, end: [d for d in FRED.get(rid, []) if start <= d <= end]

def test_target_week():
    assert wp.target_week(datetime(2026,10,18,18,5, tzinfo=wp.ROME)) == date(2026,10,19)   # domenica sera
    assert wp.target_week(datetime(2026,10,18,17,0, tzinfo=wp.ROME)) is None               # domenica pomeriggio
    assert wp.target_week(datetime(2026,10,20,9,0, tzinfo=wp.ROME)) == date(2026,10,19)    # martedì: ripresa
    assert wp.target_week(datetime(2026,10,21,9,0, tzinfo=wp.ROME)) is None                # mercoledì: troppo tardi

def test_same_day_events_stay_distinct_and_ordered():
    ev = wp.week_events(date(2026,10,26), date(2026,10,25), fred=fake_fred, cb=CB, events_map=MAP)
    assert [e["id"] for e in ev if e["mapped"]] == ["2026-10-29:us_gdp", "2026-10-29:us_pce", "2026-10-30:boj_decision"]
    assert [e["time_rome"] for e in ev if e["event_type"] == "us_gdp"] == ["13:30"]   # 08:30 New York in ora solare di Roma
    assert next(e for e in ev if e["event_type"] == "boj_decision")["time_rome"] == "04:00"

def test_unmapped_bank_is_explicit():
    ev = wp.week_events(date(2026,10,26), date(2026,10,25), fred=fake_fred, cb=CB, events_map=MAP)
    snb = [e for e in ev if not e["mapped"]]
    assert len(snb) == 1 and snb[0]["event_type"] == "snb"

def test_resume_drops_past_events():
    ev = wp.week_events(date(2026,10,26), date(2026,10,30), fred=fake_fred, cb=CB, events_map=MAP)
    assert [e["event_type"] for e in ev] == ["boj_decision"]

def test_map_tickers_exist_in_db():
    tickers = {r[0] for r in sqlite3.connect(DB).execute("SELECT ticker FROM assets")}
    for name, spec in wp.load_events_map().items():
        assert spec["reference"] in tickers, name
        assert set(spec["assets"]) <= tickers, name
        assert spec["reference"] in spec["assets"], name
        assert set(spec["scenarios"]) == {"pos", "neg"}, name

def test_cb_calendar_schema():
    rows = wp.load_cb_calendar()
    assert rows and all(r["bank"] in {"fed", "ecb", "boj", "boe", "pboc"} for r in rows)
    assert all(r["reaction_session"] >= r["decision"] for r in rows)
```

Il 2026-10-29 Roma è già in ora solare e New York ancora in ora legale: le 08:30 di New York sono le 13:30 a Roma. Il test lo blocca.

- [ ] **Step 2: Verifica che falliscano.** `cd news_impact_pipeline && venv/bin/python -m unittest tests.test_weekly_preview -v` → `ModuleNotFoundError: weekly_preview`.

- [ ] **Step 3: Implementa.**
  - Scrivi i due YAML come pinnato sopra; per gli asset «se in DB» verifica con `SELECT ticker FROM assets` e togli quelli assenti.
  - In `weekly_preview.py` scrivi le funzioni dell'Interfaces block.
  - `target_week`: domenica dalle 18:00 → lunedì successivo; lunedì o martedì → lunedì corrente; altrimenti `None`.
  - `week_events`: considera il lunedì–venerdì di `monday`, tiene solo `reaction_session >= as_of`, converte gli orari con `zoneinfo`.
  - Una banca senza voce nella mappa genera un evento `mapped: False` con `event_type = bank` e `label = bank.upper()`.

- [ ] **Step 4: Verifica che passino.** Stesso comando → OK.

- [ ] **Step 5: Commit** (solo su richiesta): `git add news_impact_pipeline/weekly_preview.py news_impact_pipeline/anteprima_eventi.yaml news_impact_pipeline/calendario_banche_centrali.yaml news_impact_pipeline/tests/test_weekly_preview.py` → `Weekly preview: event map, central bank calendar and week assembly`.

### Task 2: Scenari, statistiche e `build`

**Files:**
- Modify: `news_impact_pipeline/weekly_preview.py`
- Test: `news_impact_pipeline/tests/test_weekly_preview.py`

**Interfaces:**
- Consumes: `week_events`, `load_events_map` (Task 1); `analogues.cmd_find(theme, direction, before, subtheme, min_n, max_pool, match_all=..., direction_reference=..., strict=...)`, che stampa le date CSV su stdout e la nota su stderr; `event_study.run_event_study(tickers, event_dates, windows, as_of=...)` → `{ticker: {"per_event": [{"returns": {n: pct}}], "stats": {n: {"median", "N", ...}}}}`; `pipeline_tools.match_research(theme=, sub_themes=, assets=, text=)` → lista di dict con `score`, `title`, `source_file`.
- Produces:
  - `WINDOWS = [1, 3, 5, 10]`
  - `status_for(n: int) -> str`: `"insufficiente"` se n<5, `"indicativo"` se n<10, altrimenti `"ok"`
  - `scenario_pool(spec: dict, direction: str, before: date) -> tuple[list[str], str]`: chiama `cmd_find` con `strict=True`, `min_n=12`, `max_pool=0` e cattura stdout e stderr
  - `scenario_stats(dates: list[str], assets: list[str], as_of: date) -> dict[str, dict[str, dict]]`: `{ticker: {"1": {"median": float|None, "pos_share": float|None, "N": int}, ...}}`. Le chiavi delle finestre sono stringhe, per il JSON. `pos_share` è la quota di rendimenti > 0.
  - `build(week_of: date, as_of: date, out_root: Path = PREVIEW_DIR, fred=fred_dates) -> Path`: il lunedì è il primo lunedì **strettamente successivo** a `week_of` (`week_of + timedelta(days=7 - week_of.weekday())`); scrive `out_root / f"{iso_year}-W{iso_week:02d}"` con `tabelle.json` e `tabelle.md`, e restituisce la cartella.
  - Schema di `tabelle.json`: `{"week", "monday", "as_of", "events": [{"id", "event_type", "label", "reaction_session", "time_rome", "mapped", "status", "reference", "scenarios": {"pos"|"neg": {"label", "dates", "N", "status", "note", "stats"}}, "research": [{"title", "source_file", "score"}]}], "lacune": [{"event", "theme", "reference", "direction", "N"}]}`.
  - `status` dell'evento: `"non_mappato"`; `"insufficiente"` se entrambi gli scenari sono insufficienti; altrimenti `"ok"`.
  - Ogni scenario insufficiente aggiunge una riga a `lacune`, e le sue `stats` restano `{}`.
  - `research` contiene le prime 2 per `score`.

- [ ] **Step 1: Scrivi i test che falliscono**

```python
def test_status_thresholds():
    assert [wp.status_for(n) for n in (0, 4, 5, 9, 10)] == ["insufficiente"]*2 + ["indicativo"]*2 + ["ok"]

def test_scenario_pool_has_no_look_ahead():
    eps = [episodio("2024-05-01", {"JPY=X": ["neg"]}), episodio("2026-10-20", {"JPY=X": ["neg"]})]
    with patch.object(analogues, "_load", return_value=eps):
        dates, _ = wp.scenario_pool(MAP_BOJ, "neg", date(2026,10,20))
    assert dates == ["2024-05-01"]

def test_scenario_stats_median_and_share():
    fake = {"JPY=X": {"per_event": [{"returns": {1: 1.0}}, {"returns": {1: -2.0}}, {"returns": {1: 3.0}}], "stats": {1: {"median": 1.0, "N": 3}}}}
    with patch.object(event_study, "run_event_study", return_value=fake):
        s = wp.scenario_stats(["2024-05-01","2024-07-31","2022-12-20"], ["JPY=X"], date(2026,10,18))
    assert s["JPY=X"]["1"] == {"median": 1.0, "pos_share": 2/3, "N": 3}

def test_build_marks_insufficient_and_lacune(tmp_path):
    # pos: 6 date (indicativo), neg: 2 date (insufficiente)
    with patch.object(wp, "scenario_pool", side_effect=lambda spec, d, before: (SIX if d == "pos" else TWO, "nota")), \
         patch.object(wp, "scenario_stats", return_value={"JPY=X": {}}), \
         patch.object(wp, "week_events", return_value=[EVENTO_BOJ, EVENTO_SNB]):
        out = wp.build(date(2026,10,18), date(2026,10,18), out_root=tmp_path)
    t = json.loads((out / "tabelle.json").read_text())
    boj, snb = t["events"]
    assert out.name == "2026-W43"
    assert boj["status"] == "ok" and boj["scenarios"]["pos"]["status"] == "indicativo"
    assert boj["scenarios"]["neg"]["status"] == "insufficiente" and boj["scenarios"]["neg"]["stats"] == {}
    assert t["lacune"] == [{"event": boj["id"], "theme": "monetary_policy", "reference": "JPY=X", "direction": "neg", "N": 2}]
    assert snb["status"] == "non_mappato"
    assert "N=6" in (out / "tabelle.md").read_text()
```

`episodio(...)` riprende la fixture di `tests/test_analogues_direction.py::episode`, adattata a `theme="monetary_policy"` con `subthemes_local: ["boj"]` sull'evento.

- [ ] **Step 2: Verifica che falliscano.** Stesso comando del Task 1 → `AttributeError` sulle funzioni nuove.

- [ ] **Step 3: Implementa** le funzioni dell'Interfaces block.
  - Per `tabelle.md`, ogni evento è una sezione `## <id> — <label>` con riga `ora di Roma · riferimento · stato`.
  - Ogni scenario è una sottosezione `### Scenario pos: <label> (N=<n>, <status>)` con tabella `| asset | T+1 | T+3 | T+5 | T+10 |`. Ogni cella vale `mediana% (quota positivi%)`, con la mediana a 2 decimali e la quota come intero percentuale.
  - Seguono le research collegate.
  - In coda, `## Lacune`.
  - Aggiungi il sottocomando CLI `build [--week-of AAAA-MM-GG] [--as-of AAAA-MM-GG]` (default oggi), che stampa la cartella.

- [ ] **Step 4: Verifica che passino**, poi prova dal vero: `venv/bin/python weekly_preview.py build --week-of 2026-10-25 --as-of 2026-10-25` → cartella `weekly_preview/2026-W44`. Deve contenere PIL e PCE il 29 e la BoJ il 30 se il file la contiene, ciascuno con N.

- [ ] **Step 5: Commit** (solo su richiesta): `weekly_preview.py`, test → `Weekly preview: conditional scenario pools and tables`.

### Task 3: Validatore del testo del modello

**Files:**
- Modify: `news_impact_pipeline/weekly_preview.py`
- Test: `news_impact_pipeline/tests/test_weekly_preview.py`

**Interfaces:**
- Consumes: lo schema di `tabelle.json` (Task 2).
- Produces:
  - `CLOSING = "statistica descrittiva, non una previsione"`
  - `parse_text(text: str) -> dict[str, dict[str, str]]`: `{event_id: {"commento": str, "bozza": str}}`. Il formato di `testo.md` è `## <event_id>`, poi `### Commento`, poi `### Bozza LinkedIn`.
  - `validate(text: str, tables: dict) -> list[str]`: problemi in italiano; lista vuota vuol dire valido.
  - CLI: `validate <cartella>`, con exit 1 e i problemi su stderr se non è valido.

Regole di `validate`:
1. Ogni evento con `status == "ok"` ha una sezione con entrambe le parti non vuote, e nessuna sezione ha un id sconosciuto.
2. Ogni bozza contiene `CLOSING` e la stringa `N=`.
3. Le cifre: prima togli date ISO, `T+\d+` e gli id; poi ogni numero (`\d+(?:[.,]\d+)?`, segno ignorato) deve stare nell'insieme ammesso:
   - le mediane con 1 e 2 decimali, con il punto e con la virgola;
   - le quote positive come interi percentuali;
   - tutti gli N;
   - 1, 3, 5, 10;
   - gli anni delle date dei pool e di `as_of`.

- [ ] **Step 1: Scrivi i test che falliscono**

```python
T = {"as_of": "2026-10-18", "events": [{"id": "2026-10-30:boj_decision", "status": "ok", "scenarios": {
      "pos": {"N": 8, "dates": ["2024-03-19"], "stats": {"JPY=X": {"10": {"median": -0.734, "pos_share": 0.375, "N": 8}}}},
      "neg": {"N": 2, "dates": ["2022-12-20"], "stats": {}}}}]}
OK = ("## 2026-10-30:boj_decision\n### Commento\nCon N=8 la mediana a T+10 è −0,73% (38% positivi), dal 2022.\n"
      "### Bozza LinkedIn\nN=8. statistica descrittiva, non una previsione\n")

def test_accepts_table_figures_with_comma_and_sign():
    assert wp.validate(OK, T) == []

def test_rejects_invented_figure():
    assert any("2,5" in p for p in wp.validate(OK.replace("−0,73%", "−2,5%"), T))

def test_rejects_missing_closing_or_section():
    assert wp.validate(OK.replace(wp.CLOSING, ""), T)
    assert wp.validate("", T)

def test_rejects_unknown_event():
    assert wp.validate(OK + "## 2026-10-31:fed_decision\n### Commento\nx\n### Bozza LinkedIn\nN=1 " + wp.CLOSING, T)
```

- [ ] **Step 2: Verifica che falliscano.**
- [ ] **Step 3: Implementa** `parse_text`, `validate` e il sottocomando.
- [ ] **Step 4: Verifica che passino.**
- [ ] **Step 5: Commit** (solo su richiesta) → `Weekly preview: validator for model-written text`.

### Task 4: Render HTML e avviso del calendario in scadenza

**Files:**
- Modify: `news_impact_pipeline/weekly_preview.py`
- Test: `news_impact_pipeline/tests/test_weekly_preview.py`

**Interfaces:**
- Consumes: `tabelle.json` e `tabelle.md` (Task 2), `parse_text` e `validate` (Task 3).
- Produces:
  - `render(week_dir: Path) -> Path`: scrive `week_dir / "anteprima.html"`. Usa `testo.md` solo se esiste e `validate` restituisce `[]`; altrimenti mette in testa una riga «Commento e bozze non disponibili: <motivo>».
  - Ordine del report:
    1. calendario (giorno, ora di Roma, evento, stato);
    2. per ogni evento `ok`: le tabelle degli scenari (dal Markdown di `tabelle.md`, con `markdown.markdown(..., extensions=["tables"])`), poi il commento, poi le research;
    3. `Lacune`;
    4. `Bozze LinkedIn`, ognuna con l'etichetta «bozza da rivedere».

    HTML autonomo, sfondo bianco, sans-serif, leggibile da telefono.
  - `ALERTS = LOGDIR / "weeklypreview_avvisi.txt"`
  - `calendar_warning(today: date, rows: list[dict], alerts: Path = ALERTS) -> str | None`: restituisce il testo dell'avviso se l'ultima riunione è a meno di 60 giorni da `today` **e** l'avviso non è già stato dato oggi. Il deduplicatore scrive righe `AAAA-MM-GG<TAB>testo`.
  - CLI: `render <cartella>` e `check-calendar`; quest'ultimo stampa l'avviso, se c'è, su stdout.

- [ ] **Step 1: Scrivi i test che falliscono**

```python
def test_render_without_text_still_has_tables_and_reason(tmp_path):
    week = build_fixture(tmp_path)              # tabelle.json + tabelle.md minimi, nessun testo.md
    html = wp.render(week).read_text()
    assert "Commento e bozze non disponibili" in html and "<table" in html and "Lacune" in html

def test_render_uses_valid_text(tmp_path):
    week = build_fixture(tmp_path); (week / "testo.md").write_text(OK)
    html = wp.render(week).read_text()
    assert "bozza da rivedere" in html and wp.CLOSING in html

def test_calendar_warning_once_per_day(tmp_path):
    rows = [{"bank": "fed", "decision": date(2026,12,10), "reaction_session": date(2026,12,10), "time_local": "14:00 America/New_York"}]
    a = tmp_path / "avvisi.txt"
    assert wp.calendar_warning(date(2026,11,1), rows, a)
    assert wp.calendar_warning(date(2026,11,1), rows, a) is None
    assert wp.calendar_warning(date(2026,9,1), rows, a) is None   # oltre 60 giorni
```

- [ ] **Step 2: Verifica che falliscano.**
- [ ] **Step 3: Implementa.**
- [ ] **Step 4: Verifica che passino.**
- [ ] **Step 5: Commit** (solo su richiesta) → `Weekly preview: HTML report and calendar expiry warning`.

### Task 5: Job, prompt, registrazione e documentazione

**Files:**
- Create: `news_impact_pipeline/weekly_preview_prompt.md`, `news_impact_pipeline/run_weekly_preview.sh`, `news_impact_pipeline/launchd/com.riccardo.newsimpact.weeklypreview.plist`
- Modify: `news_impact_pipeline/run_tests.sh`, `.gitignore`, `references/routine_giornaliera.md`, `CLAUDE.md`, `../CLAUDE.md`, `MEMORY.md`
- Modify: `news_impact_pipeline/weekly_preview.py` (sottocomando `target-week`)

**Interfaces:**
- Consumes: CLI `build`, `validate`, `render`, `check-calendar` (Task 2–4); `target_week` (Task 1).
- Produces: CLI `target-week`, che stampa il lunedì AAAA-MM-GG oppure niente, con exit 0.

**Prompt** (il blocco fra i marcatori è in italiano). Il modello:
- legge `tabelle.md`;
- scrive solo `testo.md` nella stessa cartella, nel formato del Task 3, una sezione per ogni evento con stato `ok`;
- per il commento, 100–150 parole su cosa distingue i due scenari e dove gli analoghi sono deboli (N piccolo, scenario insufficiente, regimi mescolati);
- per la bozza LinkedIn, 120–200 parole con un gancio sull'evento in arrivo, il confronto fra scenari con le cifre della tabella, e una chiusura con N e la frase esatta di `CLOSING`;
- usa solo cifre presenti nelle tabelle;
- niente raccomandazioni operative;
- sigle espanse al primo uso.

**`run_weekly_preview.sh`** riprende la struttura di `run_monthly_report.sh`: `set -u`, PATH, lock in `logs/.lock_weeklypreview`, log `logs/weeklypreview-<settimana>.log`, trap che registra il consumo se il grezzo resta. In ordine:
1. `MONDAY=$($PY weekly_preview.py target-week)`; se è vuoto, `exit 0` senza log.
2. `RETE_URL=https://api.stlouisfed.org attendi_rete.sh || exit 0`.
3. `check-calendar`: se stampa qualcosa, `sendMessage` Telegram con curl. Credenziali da `~/Claude/.env`, opzioni curl come in `send_telegram.sh`.
4. Se `anteprima.html` esiste per quella settimana e, in più, `testo.md` passa `validate` oppure `tabelle.json` non ha eventi `ok`, logga SKIP ed esci.
5. `build --week-of <MONDAY − 1 giorno> --as-of <oggi>`; se fallisce, log ed exit 1.
6. Solo se `tabelle.json` ha almeno un evento `ok`, `claude -p "<prompt estratto con awk fra i marcatori>" --model claude-opus-5-5 --permission-mode bypassPermissions --output-format json`, con grezzo in `logs/.raw_weeklypreview_<settimana>.json` e consumo con `record_claude_usage.py <raw> <log> logs/usage_weeklypreview.csv <settimana> weeklypreview claude-opus-5-5`.
7. `validate`: un errore va nel log ma non ferma niente.
8. `render`.
9. `sendDocument` di `anteprima.html` con didascalia `Anteprima <settimana>: <n> eventi, <k> con analoghi`; se il testo non è valido, aggiunge « — solo tabelle». Il messaggio si costruisce con un one-liner Python su `tabelle.json`.

**Plist**: label `com.riccardo.newsimpact.weeklypreview`, `ProgramArguments` = `/bin/zsh news_impact_pipeline/run_weekly_preview.sh`, `WorkingDirectory` `/Users/riccardo/Claude/mercati_finanza`, `StartInterval` 3600, `RunAtLoad` true, log `logs/weeklypreview.log` e `logs/weeklypreview.error.log`. Gira ogni ora come il job CPI, perché `StartCalendarInterval` non recupera i run persi a Mac spento; `target-week` e lo SKIP del passo 4 rendono innocui i giri a vuoto.

- [ ] **Step 1: Registra la suite** in `run_tests.sh` col filtro `anteprima`, sullo stile delle righe `cpi` (righe 60–63): `run "Anteprima settimanale — calendario, scenari, validatore, render" tests/test_weekly_preview.py`. Aggiungi `weekly_preview/` a `.gitignore` vicino a `daily_analysis/*`.
- [ ] **Step 2: Esegui** `cd news_impact_pipeline && ./run_tests.sh anteprima` → verde; poi `./run_tests.sh` → «TUTTE LE SUITE VERDI».
- [ ] **Step 3: Scrivi** il prompt, lo script (`chmod +x`), il plist e il sottocomando `target-week`.
- [ ] **Step 4: Prova a secco del job.**
  - Lancia `venv/bin/python weekly_preview.py build --week-of 2026-10-25 --as-of 2026-10-25`.
  - Poi un run manuale del solo blocco modello, validate e render su quella cartella.
  - Atteso: `validate` esce 0, `anteprima.html` ha calendario, tabelle, lacune (BCE/BoE se in settimana) e bozze, e `logs/usage_weeklypreview.csv` ha una riga.
  - Riporta al maintainer costo e durata del run.
- [ ] **Step 5: Installa il job.** `cp news_impact_pipeline/launchd/com.riccardo.newsimpact.weeklypreview.plist ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.riccardo.newsimpact.weeklypreview.plist`; poi `launchctl print gui/$(id -u)/com.riccardo.newsimpact.weeklypreview | grep -E "runs|last exit"` → `last exit code = 0`. Oggi non è domenica sera, quindi è un giro a vuoto.
- [ ] **Step 6: Documentazione.**
  - `routine_giornaliera.md`: riga del job (domenica 18:00, ripresa fino a martedì, ogni ora) e conteggio a 8 job.
  - `CLAUDE.md` e `../CLAUDE.md`: da 7 a 8 job, `weeklypreview` nell'elenco, `weekly_preview/AAAA-Www/` in «Dove sta ogni cosa».
  - `MEMORY.md`: filone «Anteprima settimanale» (stato, decisioni del 2026-10-17, prossimo passo: strade 2 e 3).
- [ ] **Step 7: Commit** (solo su richiesta) di tutti i file del Task 5 elencati uno per uno → `Weekly preview job: Sunday calendar preview with scenario tables and LinkedIn drafts`.
