# News-to-Market Impact Pipeline

A systematic macro research desk that reads the day's economic and geopolitical news,
matches each story against a library of dated historical precedent, runs a real event
study, and — every Monday — **grades its own past forecasts and bans itself from using
the signals it gets wrong.**

It is **not** a trading system. It produces descriptive historical statistics with a
sample size attached, built to practice quantitative research discipline: honest
uncertainty, no look-ahead bias, and measured self-correction.

Running unattended since May 2026.

---

## What it does, each morning

1. **Read** the day's news items and triage them — most are discarded, with the reason recorded.
2. **Classify** each kept story against a fixed ontology (`monetary_policy`, `fiscal_policy`,
   `commodity_energy`, `geopolitical`, `macro_data`, `regulatory`, …) and identify the
   *transmission channel* — the mechanism by which the news reaches a price.
3. **Retrieve** the dated historical episodes that share that mechanism, filtered by
   sub-theme, direction and regime, with a no-look-ahead cutoff.
4. **Run** an event study over that pool: cumulative returns at T+1, T+3, T+5, T+10 on the
   assets the channel actually moves.
5. **Write** a card with the reading, the caveats, and — critically — what the result
   *cannot* support.

Every directional claim it makes is logged. Weeks later, when enough trading days have
passed, that claim is scored against what the market actually did.

## The three layers

Le dimensioni sono una fotografia al **2026-08-30**: il sistema cresce, i numeri qui
sotto no. Per i valori correnti vedi la sezione "Dati che NON si scrivono qui" in
`CLAUDE.md`.

| Layer | What it is |
|---|---|
| **1 — Market data** | 78 assets, daily, 2011→present, in SQLite. Equities, FX, rates, commodities, credit, volatility. Includes two *derived* series computed daily from raw tickers — a 3-2-1 refining margin and a sovereign yield spread — stored as tickers so the event-study engine treats them like any other asset. |
| **2 — Knowledge base** | 24 deep-research studies. Each documents a regime, its transmission channels, and a dated catalogue of anchor episodes, with a structured YAML metadata block used for matching. |
| **3 — Analytics** | The episode library (~980 dated episodes), the event-study engine, the category→asset map, and the weekly forecast scorecard. |

## Architecture note: the agent is the classifier

There is **no call to a hosted LLM API anywhere in this repository.** The classification
step — reading a news item and reasoning about its transmission mechanism — is performed
by an AI coding agent in-session. Everything the agent needs to *act* on that reasoning is
exposed to it as deterministic Python it invokes as a tool: the database, the historical
matcher, the event-study math, the scorecard.

The consequence worth noting: the judgment stays with a reasoning model, while every
number stays reproducible and auditable. Re-running `event_study.py` on the same episode
list yields the same table, forever.

---

## The scorecard — the part most systems don't publish

`daily_analysis/_scorecard/` contains every weekly run. The most recent one, at the time
of writing, reads:

- **2,650** matured forecasts scored
- **52%** directional hit rate — a coin flip is 50%
- **+0.03** Information Coefficient, measured *per asset* — effectively zero
  (the naive pooled figure is higher, and is not used: it mostly rewards the fact
  that `^VIX` moves more than `EURUSD=X`, not any forecasting skill)

That headline number is deliberately unflattering, and publishing it is the point. It is
the average of two groups that cancel out. Broken down per asset, the picture is
different and actionable:

| Reliable (IC > 0) | Backwards (IC < 0) |
|---|---|
| `^STOXX50E` +0.17 · `^NDX` +0.17 · `^VIX` +0.17 · `EEM` +0.17 · `BZ=F` +0.13 | `GC=F` −0.07 · `DX-Y.NYB` −0.16 · `^TNX` −0.20 · `IEF` −0.29 |

On the right-hand column the historical pattern is **systematically inverted** — the pool's
implied direction is worse than useless. So the system enforces the split at write time:
a card may report the event study on a flagged asset, but is barred from drawing a
directional read from it, and must say so explicitly.

The standing observation is itself a finding: the reliable assets are **equity and
volatility**; the counterproductive ones are **safe havens, rates and the dollar**. Cards
on rates and FX are structurally the weakest output this system produces, and it says so.

---

## A worked example of self-correction

The design flaw that took longest to find is a good illustration of the method.

Each daily card carries one `sentiment` field. When the episode library was built, that
single field was stamped onto **every historical date the card cited** — including the
20–30 unrelated analogues from years earlier. The direction attached to an episode
therefore described *the card that referenced it*, not the episode.

The symptom was reported on **5 August** ("the `--direction` filter isn't discriminating"),
along with the correct fix. It was re-reported under different names on the 10th, 13th,
14th and 15th. It was only measured and fixed on the **19th**:

```
367 / 844 episodes (43%) carried two or three contradictory directions at once
regulatory / tariff_escalation: positive-direction episodes = 0
  → every "tariffs de-escalate" story was compared against a pool of pure escalation
```

The fix derives each episode's sign from the text immediately surrounding *that* date.
On the activity-growth pool, `--direction pos` and `--direction neg` went from returning
**28 of 29 identical** episodes to **16 and 20 with 12 in common**.

The lesson is recorded in the runbook, not just the code: the same class of bug — a
document-level attribute smeared across every date the document mentions — had already
been fixed twice before for other fields. The upstream fix now has cards declare their
episodes in a structured block, so the library reads fields instead of inferring them
from prose.

---

## Repository layout

```
news_impact_pipeline/     the code
  analogues.py              episode library: build / find / labels / stats
  event_study.py            cumulative-return event study with percentile bands
  forecast_tracking.py      forecast ledger + weekly scorecard (IC, hit rate, coverage)
  bootstrap_market_data.py  one-time historical load  (all assets in ASSETS)
  update_market_data.py     daily incremental refresh
  subtheme_taxonomy.yaml    canonical sub-theme vocabulary
  category_asset_map.yaml   ontology category → transmission assets
  PHASE5_RUNBOOK.md         the operating procedure the daily run follows

knowledge_base/           research studies + the episode library
daily_analysis/           sample output + the full weekly scorecard history
references/               one file per recurring method (asset coverage, reading
                          conventions, derived series, label attribution, run cost)
CLAUDE.md                 the map: where things are, how to run them, hard constraints
MEMORY.md                 current state per workstream (status / decided / next step)
Design_Document_NewsImpact.md   original design spec
```

## Running it

```bash
cd news_impact_pipeline
python3 -m venv venv && venv/bin/pip install -r requirements.txt

venv/bin/python bootstrap_market_data.py     # one-time: 15y history, all assets
venv/bin/python update_market_data.py        # daily incremental
venv/bin/python analogues.py build           # (re)build the episode library
venv/bin/python analogues.py stats           # library size + quality metrics

# find analogues and run an event study
venv/bin/python analogues.py find --theme commodity_energy --subtheme supply_disruption --direction neg
venv/bin/python event_study.py --ticker 'BZ=F,CRACK_321' --events <dates> --windows 1,3,5,10 --markdown

venv/bin/python forecast_tracking.py run     # score matured forecasts, rebuild scorecard
```

API keys (FRED, Stooq, Telegram delivery) are read from an `.env` file kept **outside**
this repository. Everything except those optional integrations runs without credentials.

## What's excluded from this repo, and why

- **The market database** (28 MB) — fully regenerable with `bootstrap_market_data.py`.
- **The virtualenv** — see `requirements.txt`.
- **Rendered HTML reports** — generated from the committed `.md` sources.
- **Most of the daily-analysis archive** — the cards embed short summaries of the day's
  news, second-hand from wire reporting. Three consecutive days are published as a
  representative sample; the full run stays local.

---

## Caveats, stated up front

- Sample sizes are small. Any statistic on fewer than 10 episodes is flagged
  `INDICATIVE ONLY` in the output, and should be read as illustrative.
- Attribution is imperfect: a realized return over a T+10 window reflects *everything*
  that happened in that window, not only the classified news. This is why the
  distribution-coverage metric is treated as more honest than the point hit rate.
- Regime segmentation is the main defence against mixing structurally different macro
  environments, and it is a judgment call, not a solved problem.
- Nothing here is investment advice or a recommendation of any kind.
