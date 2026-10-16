# Prompt di ricerca notizie — Morning Briefing (v3, 2026-10-16)

> Questo è il prompt che il job `com.riccardo.newsimpact.brief` esegue ogni mattina
> alle 07:40. Copia canonica e versionabile, **fonte unica**:
> `run_morning_brief.sh` estrae da qui SOLO il blocco delimitato da
> `=== PROMPT START/END ===` e non ne tiene una copia propria — quindi per
> cambiare il briefing si modifica questo file, e basta. Le note qui sopra
> restano fuori dal prompt (è in inglese di proposito:
> un prompt in inglese produce un briefing in inglese — la v2/v2.1 erano in italiano
> e facevano uscire il briefing in italiano).
>
> Changelog:
> - v1→v2 (06-05): path dedup+salvataggio → `~/Claude/morning brief/`; dati macro con
>   valore+attesa; espansione sigle; tag rilevanza-mercato; fonti primarie.
> - v2→v2.1 (06-05): aggiunta riga "output in inglese" (insufficiente: prompt ancora IT).
> - v2.1→v2.2 (06-06): **prompt riscritto interamente in INGLESE** = fix definitivo
>   della lingua. Il contenuto/miglioramenti sono identici alla v2.
> - v2.2→v3 (10-16): **fonti raggiungibili e testo più lungo.** Reuters, AP, FT, WSJ, The
>   Economist, BBC, Guardian, NYT, Politico, MarketWatch, Barron's, Le Monde ed El País
>   bloccano il crawler di Anthropic (né fetch né risultati di ricerca: la ricerca con quei
>   domini in `allowed_domains` risponde 400): il prompt v2 chiedeva fonti irraggiungibili
>   e il modello ripiegava su aggregatori (investingLive, BabyPips, Substack). Ora: livelli
>   di fonte con l'elenco dei domini verificati il 2026-10-16, dati macro dal comunicato
>   ufficiale, 90–150 parole per notizia invece di 2–3 frasi, fetch del testo intero invece
>   dei "key facts", finestra "dall'edizione precedente" invece di "pubblicate oggi".
>   Se un dominio dell'elenco smette di rispondere, va tolto da qui.

---

=== PROMPT START ===
Use web search to find the most important news since the previous edition (roughly the
last 24 hours, Europe/Rome time). Only include stories published or significantly
updated in that window. Write the **entire briefing in English**.

**Sources — tiered (important).** Many top outlets block automated access: Reuters,
Associated Press, Financial Times, Wall Street Journal, The Economist, BBC, The Guardian,
New York Times, Politico, MarketWatch, Barron's, Le Monde and El País cannot be fetched
and do not even appear in search results. Do not search for them or cite them.
Use these tiers instead:
1. **Primary institutional sources — mandatory for every data point.** For any macro
   release or policy decision, open the official release: Eurostat (ec.europa.eu), ECB
   (ecb.europa.eu), Federal Reserve (federalreserve.gov), BLS (bls.gov), BEA (bea.gov),
   Census Bureau (census.gov), ISTAT (istat.it), IMF (imf.org), Bank of England
   (bankofengland.co.uk), and other central banks or statistics offices as relevant.
   Link the release itself.
2. **Reachable quality outlets — first choice for news.** Run your news searches with
   `allowed_domains` set to: bloomberg.com, cnbc.com, asia.nikkei.com, semafor.com,
   axios.com, france24.com, euronews.com, scmp.com, japantimes.co.jp, npr.org, cnn.com,
   aljazeera.com, handelsblatt.com, ilsole24ore.com, ansa.it. If a search fails with
   "not accessible to our user agent", remove the domains it names and retry.
   Bloomberg pages often cannot be opened: you may use a Bloomberg headline or search
   snippet only together with a second source you actually read.
3. **Anything else — fallback only.** Other sites (market blogs, aggregators, newsletters,
   data portals like Trading Economics) may fill a gap, but never as the sole source for a
   figure when tier 1 has it, and mark them "(secondary source)" next to the citation.
Cite the source you actually read, with its real URL.

**Reading articles.** When you fetch a page, ask for the full article text with all
figures, quotes, names and dates — not a summary or "key facts". For a long page, read on
with the offset the previous result gives. You need the substance to write a real
paragraph, not a headline.

**Deduplication (important).** Before generating the briefing, read the most recent
briefing file in `/Users/riccardo/Claude/mercati_finanza/morning brief/` (the previous day's file). Any story
already present there with **no concrete new development** must be excluded — do
not repeat static facts, standing estimates, or unchanged institutional positions. A
story may reappear **only** if there is a concrete update (new data released, policy
decision made, significant market reaction, etc.), and then the paragraph must lead with
what is new.

**Macro data — actual + expected (mandatory).** Whenever you cite an economic data
release (inflation, jobs, GDP, PMI surveys, etc.), report **the actual figure, the
consensus/expected figure, the previous figure, and the direction of the surprise** — it is
the surprise versus expectations that moves markets. Example: "US CPI (Consumer Price
Index) for May rose to 3.2% vs 3.0% expected and 3.1% in April — an upside surprise".

**Acronyms.** Expand every acronym on first use, then you may abbreviate (e.g. "CPI
(Consumer Price Index)", "NFP (Non-Farm Payrolls)"). Keep the tone professional and
analytical, no sensationalism.

**Depth.** Each story gets one paragraph of **90–150 words**: what happened (who, what,
when, the key numbers), the background a reader needs, and why it matters. Do not write
headline-only items; if you could not read enough to write the paragraph, drop the story.

Structure the output exactly as follows:

# 🌍 Morning Briefing — [Today's Date]

## Top 10 International News
For each: bold headline, a 90–150 word paragraph on what happened and why it matters
globally, source name and link.

## 💹 Top 10 Economics & Finance News
For each: bold headline, a 90–150 word paragraph focused on market implications, macro
relevance or policy impact, source name and link. **Add a final "Markets:" line** noting
briefly the transmission channel and asset class affected (e.g. "Markets: government-bond
yields and European equities; touches the BTP-Bund spread and Euro Stoxx 50"). If the
story is a data release, include actual vs expected as above.

## 🔎 One Thing to Watch Today
The single most market-moving development to monitor today, and why.

**Saving.** After generating the briefing, save it as an HTML file named
`YYYY-MM-DD-morning-briefing.html` (using today's Europe/Rome date) in
`/Users/riccardo/Claude/mercati_finanza/morning brief/`
— clean, readable HTML: white background, sans-serif font, comfortable line spacing,
styled headings, mobile-friendly. **Keep the existing HTML structure**: each
verified story must be in a numbered container with `class="story"`, grouped under
an `<h2>` containing either "International" or "Economics & Finance". Include up to
10 stories per section. If fewer than 20 stories are available, publish a clearly
labelled partial edition with only the new, verified stories; do not pad it with
older, duplicate or weakly verified items. Each story needs an `<h3>` headline, a
text paragraph, and a source link with the actual URL. The downstream parser depends
on these tags and class names. Build the entire HTML in a temporary file in the same
directory, verify that the number of `story` containers matches the number of
published stories and that a closing `</body>` tag is present, then atomically rename
it to the final filename. If the final file already exists and passes these checks,
do not overwrite it. If no new, verifiable stories are available, do not publish a
file and report that outcome.

=== PROMPT END ===
