# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**News-to-Market Impact Pipeline** — a system that classifies daily economic/geopolitical news, maps them to historically analogous market events, and produces structured event-study output. Not a trading bot; produces descriptive historical statistics intended for analytical content (LinkedIn) and quantitative finance skill-building.

Full design spec is in `Design_Document_NewsImpact.md`.

## Commands

All scripts run from inside the venv in `news_impact_pipeline/`:

```bash
# One-time historical bootstrap (15 years, 66 assets via yfinance)
news_impact_pipeline/venv/bin/python news_impact_pipeline/bootstrap_market_data.py

# Daily incremental update (adds only missing rows since last run)
news_impact_pipeline/venv/bin/python news_impact_pipeline/update_market_data.py

# Weekly feedback loop: score past forecasts against realized market moves
# (backfill ledger + evaluate matured forecasts + regenerate scorecard).
# Runs automatically Monday 09:00 via launchd; this is the manual equivalent.
news_impact_pipeline/venv/bin/python news_impact_pipeline/forecast_tracking.py run
```

Install dependencies:
```bash
cd news_impact_pipeline && python3 -m venv venv && venv/bin/pip install -r requirements.txt
```

## Architecture: three layers

**Layer 1 — Market Data** (`market_data/market_data.db`, SQLite): Historical daily prices for 66 assets from 2011 to present (17 originali + 9 aggiunti il 2026-06-05: ^NDX, SOXX, URA, LIT, EEM, HYG, ^VIX, HG=F, DX-Y.NYB — vedi audit strato 2; + 2 aggiunti il 2026-07-07 per il canale energetico EU: TTF=F gas europeo, EXH9.DE utility europee/proxy elettricità; + CNY=X yuan onshore aggiunto il 2026-07-13 per il canale valuta cinese/dazi; + EWZ/BRL=X Brasile aggiunti il 2026-07-19 per il canale LatAm; + 7 ASEAN aggiunti il 2026-07-30 — THB=X/SGD=X/MYR=X/IDR=X e THD/EWS/EIDO — perché EEM era troppo diluito per il Sud-Est asiatico; + SHLD.L/EWY/EWT aggiunti il 2026-08-10 — difesa globale/NATO-Europa, Corea, Taiwan — per i canali difesa europea e memoria/HBM-Taiwan segnalati ripetutamente come strutturalmente invisibili; + CAD=X aggiunto il 2026-08-16 — canale dazi/attriti commerciali USA-Canada, assente mentre i dazi sono diventati strumento ricorrente; + 6 aggiunti il 2026-08-18 dopo il selloff sincronizzato sulle curve — ^TYX 30Y USA, IGLT.L gilt, 1482.T JGB, VGB.AX ACGB, ^GSPTSE azionario canadese, EXV7.DE chimica europea; + 14 aggiunti il 2026-08-19 come **primo audit di copertura NON reattivo** — settoriali IGV/XLE/IYT/XLV/ITA/REMX/TAN, India INDA/INR=X, valute KRW=X/NOK=X/ILS=X, curva ^FVX e volatilita' obbligazionaria ^MOVE: tutti buchi gia' segnalati fra il 5 e il 14 agosto e mai colmati). `bootstrap_market_data.py` does the one-time full load; `update_market_data.py` does incremental daily updates. Both scripts live in `news_impact_pipeline/`. The update script imports shared constants and helpers directly from the bootstrap script — do not split them.

**Layer 2 — Knowledge Base** (`knowledge_base/`): one subfolder per study (e.g. `knowledge_base/sovereign_debt/`), each holding the source material (PDF, etc.) plus a markdown deep-research file ending with a structured YAML metadata block (template in Design_Document §5.2). `build_catalog.py` scans the KB **recursively** and regenerates the `catalog.yaml` index (`source_file` is the path relative to the KB). Files without a YAML block are skipped. Matching to news uses `primary_theme`, `relevant_assets`, and `regime_phases`. To add a study: drop its folder under `knowledge_base/`, ensure the .md has the trailing YAML block, then re-run `build_catalog.py`.

⚠ **Chi scrive le research: il maintainer, non Claude** (regola fissata il 2026-08-16, precisata il 2026-08-18). Claude **non** scrive deep research, e **non** scrive nemmeno i prompt di deep research di sua iniziativa. Quando l'analisi giornaliera trova una lacuna di KB si limita a **descriverla** nella sezione "Lacune emerse" di `_index.md`. Il prompt in `knowledge_base/_prompts/<slug>.md` si scrive **solo su richiesta esplicita del maintainer** (template e convenzioni in `_prompts/README.md` e `_prompts/_TEMPLATE.md`). La research la esegue il maintainer; Claude riprende in mano il file solo per indicizzarlo (`build_catalog.py` + `analogues.py build`) e cancellare il prompt. Ogni percorso con un componente che inizia per `_` è escluso sia da `build_catalog.py` sia da `analogues.py` — è ciò che impedisce ai blocchi YAML e alle date ISO di esempio dei prompt di entrare in `catalog.yaml` e in `_episodes.yaml`.

**Layer 3 — Analytics & Pipeline** (LIVE): Receives news text → the agent itself classifies it (ontology in Design_Document §6.1 — **no Anthropic API key involved**, see Phase 3 note below) → queries KB for regime context → pulls analogous historical episodes from the **episode library** (`analogues.py`, "Opzione B") → runs event study (cumulative returns at T+1, T+3, T+5, T+10) → outputs a markdown card to `daily_analysis/YYYY-MM-DD/news_NN.md`, then `render_report.py` builds `report.html` and `send_telegram.sh` delivers brief+report to Telegram.

## Database

- Path: `~/Claude/mercati_finanza/market_data/market_data.db`
- Tables: `assets` (metadata/registry), `prices` (ticker × date, OHLCV + adj_close)
- `BTP_BUND_SPREAD` **is populated and DAILY** (since 2026-06-04): ~8,800 **daily** rows from 1991-11 to present, computed as Italy 10Y − Germany 10Y, stored **in basis points** in `close`/`adj_close` (OHLC/volume are NULL — a yield spread has no candles). Source = **Stooq** daily benchmark yields (`10YITY.B`, `10YDEY.B`), fetched by `fetch_daily_spread.py` (needs `STOOQ_API_KEY` in `~/Claude/.env`). In event studies T+N steps are **trading days**, like every other asset — `event_study.py` auto-detects the daily cadence (no monthly warning). Use it as the primary eurozone-periphery **fragmentation/risk indicator**. **Do not describe it as "not in DB" / "empty" / "monthly" / "placeholder".**
  - Legacy: `fetch_fred_data.py` (FRED monthly series `IRLTLT01ITM156N` / `IRLTLT01DEM156N`) was the previous **monthly** source — kept as a fallback only; the daily Stooq fetch supersedes it and overwrites the same ticker.
  - Refresh: neither FRED nor Stooq is touched by the daily incremental `update_market_data.py` — re-run `fetch_daily_spread.py` to extend the series (candidate for the daily/weekly automation).
  - 🟡 **HTTP fetch dead, manual path in place (diagnosed 2026-08-19)**: Stooq now sits behind a JavaScript **proof-of-work** challenge — `urllib` gets a 404 without a User-Agent and the verification page with one, so `fetch_daily_spread.py`'s automatic download cannot work regardless of the API key. No per-country daily substitute exists (Eurostat and the ECB give Italy only monthly; the ECB's daily YC covers the aggregate AAA curve, not Italy). Working procedure: open `https://stooq.com/q/d/?s=10yity.b` and `.../?s=10ydey.b` in the browser, read the closes, then `fetch_daily_spread.py --pairs YYYY-MM-DD,IT,DE ...` — include one date already in the DB as a **control**, the script refuses to write if the recomputed spread does not reproduce it. Backfilled through 2026-08-18 this way. This also closed off the Stooq route for gilt/JGB/ACGB — hence the ETF proxies added 2026-08-18.
- ⚠ **Bond sign convention (mixed on purpose).** `^TNX` (10Y), `^FVX` (5Y) and `^TYX` (30Y) are **yields**: they rise in a selloff. `IEF`, `IEAG.AS`, `EXX6.DE`, `IGLT.L` (gilt), `1482.T` (JGB), `VGB.AX` (ACGB) are **ETF prices**: they fall in the same selloff. A synchronized global bond selloff therefore prints `^TYX` positive and the others negative — that is agreement, not divergence, and any card touching two of them must say so explicitly.
- `CRACK_321` **is the refining margin** (added 2026-08-11), stored in **USD per barrel** in `close`/`adj_close` (OHLC/volume NULL, like the BTP spread). Computed by `compute_crack_spread.py` as the standard 3-2-1 crack: `(2*RB=F + 1*HO=F) * 42 / 3 − BZ=F` — the 42 converts the products from $/gallon to $/barrel. Recomputed **every day** by `update_market_data.py` straight from tickers already in the DB (no external source, so no rate-limit/anti-bot risk). Use it for **refinery outages/attacks**: those hit products and margins, not crude — Brent alone can even fall while diesel spikes. Historical sanity check: median ~$9–17 in normal years, $7 in 2020 (COVID demand collapse), $32 in 2022 (post-invasion diesel crisis), $43 in 2026. NB: it pairs NYMEX products with **Brent** (not WTI) deliberately — the channel of interest is European/Russian.
- Computed indicators (returns, volatility, moving averages) are **never persisted** — always calculated on-the-fly in the analytics layer. (Exceptions: `BTP_BUND_SPREAD` and `CRACK_321`, which are *derived series* stored as tickers so the event study can treat them like any other asset.)

## Implementation status

**ALL PHASES COMPLETE & LIVE** (do not describe any of them as "not started").

- **Phase 1 (Market Data)**: live. 66 assets, daily incremental update via launchd 08:00.
- **Phase 2 (Knowledge Base)**: live. 19 studies indexed in `catalog.yaml`, auto-indexing via `index_studies.sh`.
- **Phase 3 (News Classification)**: live — **the agent in the Claude Code session IS the classifier**; Python only exposes deterministic tools (DB, catalog, event study) invoked via Bash. The `anthropic` package is deliberately NOT used (decided 2026-05-28): no API key, no extra billing.
- **Phase 4 (Event Study)**: live (`event_study.py`), with the "Opzione B" analogue library (`analogues.py`) supplying wide, filtered pools of dated episodes instead of ~5 hand-picked ones. Since 2026-08-15 each episode also carries **date-local** subtheme labels (`subthemes_local`), derived from the text surrounding that specific date and matched against the canonical taxonomy in `subtheme_taxonomy.yaml`; `find --subtheme` prefers them over the document-level `subthemes`, which stay as a recall fallback. Since 2026-08-19 the same treatment applies to **direction** (`directions_local`, vocabulary in `DIRECTION_PATTERNS` inside `analogues.py`): previously a card's single `sentiment` was stamped onto *every* date the card cited — including its 20-30 historical analogues — so 367 of 844 episodes carried 2-3 directions at once and `--direction` was nominal (`macro_data/activity_growth` returned 28 of 29 identical episodes for `pos` and `neg`). `find --direction` now prefers the date-local sign and **declares in stderr** when it degrades to card level. Adding a canonical label = editing that YAML, then `analogues.py build`. Check coverage before choosing a `--subtheme` token with `analogues.py labels --theme <t>`, and calibrate new patterns against the **real** contexts (cards write technical English — `FOMC`, `75bp`, `dot plot` — not Italian).
- **Phase 5 (Daily Automation)**: live via launchd (`run_daily_analysis.sh` at 08:15 + WatchPaths on the briefing folder).
- **Phase 6 (Monthly Strategic Report)**: live (`run_monthly_report.sh`, 1st of month 09:30) — regime & scenario synthesis, not point forecasts.
- **Feedback loop**: weekly scorecard (`run_scorecard.sh`, Monday 09:00) scores past forecasts against realized moves → `daily_analysis/_scorecard/YYYY-Www.md`.

⚠ Five launchd jobs (`com.newsimpact.*`) run this from **inside this folder**. If the project folder is ever moved, the plists must be edited AND reloaded (`launchctl bootout` then `bootstrap`) or every job silently stops firing.

## Key constraints

- Always report sample size (N) alongside event-study statistics — a result based on N<10 episodes must be flagged as indicative only.
- When selecting historical analogues, use only information available at the time of the historical event (no look-ahead bias).
- Regime segmentation (from KB metadata `regime_phases`) is the primary defence against mixing structurally different macro environments in the same sample.
