# Prompt di ricerca notizie — Morning Briefing (v2.2, 2026-06-06)

> Questo è il prompt che la routine schedulata di Claude esegue ogni mattina.
> Copia canonica e versionabile. **Incolla nella routine `/schedule` SOLO il blocco
> qui sotto delimitato da `=== PROMPT START/END ===`** (è in inglese di proposito:
> un prompt in inglese produce un briefing in inglese — la v2/v2.1 erano in italiano
> e facevano uscire il briefing in italiano).
>
> Changelog:
> - v1→v2 (06-05): path dedup+salvataggio → `~/Claude/morning brief/`; dati macro con
>   valore+attesa; espansione sigle; tag rilevanza-mercato; fonti primarie.
> - v2→v2.1 (06-05): aggiunta riga "output in inglese" (insufficiente: prompt ancora IT).
> - v2.1→v2.2 (06-06): **prompt riscritto interamente in INGLESE** = fix definitivo
>   della lingua. Il contenuto/miglioramenti sono identici alla v2.

---

=== PROMPT START ===

Use web search to find today's most important news. Only include stories published
or significantly updated **today**. Write the **entire briefing in English**.

**Sources.** Prioritize authoritative outlets: Reuters, Associated Press, Financial
Times, Bloomberg, The Economist, Wall Street Journal, and primary institutional
sources — the ECB, Federal Reserve, IMF, and official statistical agencies for macro
data (BLS and BEA for the US, Eurostat for the euro area, ISTAT for Italy). Note:
some sources (FT, Bloomberg, WSJ, The Economist) are paywalled and web search may not
read their full text — in that case verify the story on an accessible source
(Reuters/AP or the primary release) and cite that. For any **data point**, include a
verifiable primary link/source.

**Deduplication (important).** Before generating the briefing, read the most recent
briefing file in `~/Claude/morning brief/` (the previous day's file). Any story
already present there with **no concrete new development today** must be excluded — do
not repeat static facts, standing estimates, or unchanged institutional positions. A
story may reappear **only** if there is a concrete update (new data released, policy
decision made, significant market reaction, etc.).

**Macro data — actual + expected (mandatory).** Whenever you cite an economic data
release (inflation, jobs, GDP, PMI surveys, etc.), report **the actual figure, the
consensus/expected figure, and the direction of the surprise** — it is the surprise
versus expectations that moves markets. Example: "US CPI (Consumer Price Index) for
May rose to 3.2% vs 3.0% expected — an upside surprise".

**Acronyms.** Expand every acronym on first use, then you may abbreviate (e.g. "CPI
(Consumer Price Index)", "NFP (Non-Farm Payrolls)"). Keep the tone professional and
analytical, no sensationalism.

Structure the output exactly as follows:

# 🌍 Morning Briefing — [Today's Date]

## Top 10 International News
For each: bold headline, 2–3 sentences on what happened and why it matters globally,
source name.

## 💹 Top 10 Economics & Finance News
For each: bold headline, 2–3 sentences focused on market implications, macro relevance
or policy impact, source name. **Add a final "Markets:" line** noting briefly the
transmission channel and asset class affected (e.g. "Markets: government-bond yields
and European equities; touches the BTP-Bund spread and Euro Stoxx 50"). If the story
is a data release, include actual vs expected as above.

## 🔎 One Thing to Watch Today
The single most market-moving development to monitor today, and why.

**Saving.** After generating the briefing, save it as an HTML file named
`YYYY-MM-DD-morning-briefing.html` (using today's date) in `~/Claude/morning brief/`
— clean, readable HTML: white background, sans-serif font, comfortable line spacing,
styled headings, mobile-friendly. **Keep a stable HTML structure** (consistent
`<h1>`/`<h2>`/`<h3>` headings for sections and story titles): a downstream parser
reads this file, so do not change the tag layout from one day to the next.

=== PROMPT END ===
