# Fed: reaction function, indipendenza e divergenza con la BCE (2023–2026)

> **Nota metodologica sui dati di mercato.** Dove si descrivono reazioni di mercato su finestre T+1/T+3/T+5/T+10 per ^TNX, IEF, ^GSPC, EUR/USD, DXY e oro (GC=F), si forniscono **direzione e ordine di grandezza qualitativo** più i livelli puntuali riportati dalle fonti. **Il calcolo numerico esatto dei rendimenti cumulati T+N va eseguito dal sistema dell'utente contro il proprio Market Data Layer.** Non sono stati inventati rendimenti percentuali precisi laddove non verificati. Si distingue sistematicamente tra **[FATTO]** (supportato da fonte primaria/dati) e **[INTERPRETAZIONE]**.

---

## TL;DR

- **La funzione di reazione della Fed nel 2023–2026 si è capovolta due volte**: da "higher for longer" (plateau 5,25–5,50% da luglio 2023) a ciclo di tagli (settembre 2024 → dicembre 2025, fino a 3,50–3,75%), e infine a un **re-pricing hawkish** innescato dallo shock energetico dello Stretto di Hormuz (CPI maggio 2026 +4,2% a/a, energia +23,5%), che a giugno 2026 ha congelato i tassi e spostato i futures verso un possibile **rialzo**. È il classico dilemma da shock di offerta: la Fed non ha strumenti per abbassare il prezzo del petrolio.
- **Per l'event study, la lezione operativa è che a muovere i mercati è soprattutto la COMUNICAZIONE (il "path factor"), non l'azione**: i due episodi più violenti del periodo — il pivot dovish del 13 dicembre 2023 e l'"hawkish cut" del 18 dicembre 2024 — sono stati guidati dal *dot plot* e dalla guidance, non dalla decisione sul tasso (in dicembre 2024 il taglio era pienamente atteso, ma il dot plot revisionato al rialzo fece crollare l'S&P ~3%).
- **L'attacco all'indipendenza della Fed è la variabile di coda più nuova e meno trasferibile**: caso *Trump v. Cook* in Corte Suprema, indagine penale DOJ su Powell, e transizione Powell→Warsh sotto pressione politica (Warsh confermato 54–45 il 13 maggio 2026, giuramento 22 maggio). Il canale di trasmissione atteso è **term premium e dollaro più che tassi a breve**: storicamente (Nixon-Burns, Truss, Turchia) la perdita di credibilità si scarica su curva lunga, breakeven d'inflazione e valuta.

---

## Key Findings

1. **[FATTO]** Il tasso terminale di 5,25–5,50% è stato raggiunto il **26 luglio 2023** (11° rialzo del ciclo iniziato a marzo 2022) ed è rimasto invariato fino a settembre 2024 (fonte: comunicato FOMC, CNBC).
2. **[FATTO]** Primo taglio del ciclo: **18 settembre 2024**, 50bp a 4,75–5,00% (primo taglio in oltre 4 anni; unico dissenso di Bowman per 25bp). Seguono novembre 2024 (-25bp) e dicembre 2024 (-25bp a 4,25–4,50%).
3. **[FATTO]** Nel 2025 la Fed tiene fermo per le prime cinque riunioni, poi taglia tre volte (settembre, ottobre, dicembre) fino a **3,50–3,75%** — riduzione cumulata di 175bp da settembre 2024 (fonte: iShares, CNBC).
4. **[FATTO]** Lo shock dello Stretto di Hormuz (guerra con l'Iran iniziata 28 febbraio 2026) ha portato il **CPI di maggio 2026 a +4,2% a/a** (massimo da aprile 2023), con **energia +23,5%** e benzina +40,5% a/a; il core è rimasto contenuto a 2,9% (fonti: BLS via CNN, CNBC, Morningstar).
5. **[FATTO]** **Kevin Warsh** è stato nominato (30 gennaio 2026), confermato dal Senato **54–45** il **13 maggio 2026** (margine più stretto nella storia per un Chair) e giurato **17° Chair il 22 maggio 2026**; Powell resta governatore fino al 31 gennaio 2028; Stephen Miran dimissionario.
6. **[INTERPRETAZIONE]** Il regime 2023–2026 combina elementi raramente co-presenti — shock di offerta energetico, attacco istituzionale all'indipendenza e transizione di leadership ostile — rendendolo un analogo storico fragile per cicli passati guidati dalla domanda.

---

## Details

### 1. La reaction function, spiegata (dalle basi)

**Il doppio mandato.** Il Federal Reserve Act assegna alla Fed due obiettivi: **massima occupazione** e **stabilità dei prezzi** (formalizzata dal 2012 come target del 2% sull'indice PCE). **[FATTO]** Diversamente dalla BCE, che ha un mandato gerarchico con priorità alla stabilità dei prezzi, la Fed pondera i due obiettivi. Quando entrano in tensione — come nel 2025–26, con inflazione sopra target ma mercato del lavoro in raffreddamento — la Fed deve scegliere quale lato privilegiare. Powell ha descritto questa tensione esplicitamente: nel dicembre 2025 ha parlato di "no risk-free path", e nell'aprile 2026 di obiettivi "a bit in tension".

**La regola di Taylor come benchmark.** **[FATTO]** Taylor (1993, *Carnegie-Rochester Conference Series*) propose che il tasso di policy reagisca in modo prevedibile: i = r\* + π + 0,5(π−π\*) + 0,5(output gap). **[INTERPRETAZIONE]** La Fed non la segue meccanicamente, ma è il riferimento che gli economisti usano per giudicare se la politica è "dietro la curva". Nel 2025–26 le regole tipo Taylor, alimentate da un CPI sopra il 4%, segnalavano tassi molto più alti del 3,50–3,75% effettivo — la radice del re-pricing hawkish e dei dissensi interni.

**Esempio concreto di data-dependence.** **[FATTO]** Powell ha ripetuto fino alla nausea che le decisioni sono prese "meeting-by-meeting" e "based on the incoming data". Nel settembre 2025 ha definito il taglio un "risk-management cut", non una risposta a una recessione conclamata.

**Azione vs comunicazione — il cuore dell'event study.** **[FATTO]** **Gürkaynak, Sack & Swanson (2005, *International Journal of Central Banking*, vol. 1 n. 1, pp. 55–93)**, "Do Actions Speak Louder Than Words?", dimostrano con dati intraday dal 1990 che le mosse della Fed non sono catturate da un solo fattore (il livello del funds rate), ma da **due**: un **"target factor"** (la decisione sul tasso) e un **"path factor"** (le aspettative sul percorso futuro), quest'ultimo strettamente associato ai comunicati FOMC. Conclusione chiave: **le dichiarazioni muovono i rendimenti a lungo termine molto più dell'azione sul tasso**. Questo è il fondamento teorico per cui, in molti episodi sotto, il movimento di mercato non corrisponde alla decisione ma alla guidance.

**Il dot plot (SEP).** **[FATTO]** Quattro volte l'anno (marzo, giugno, settembre, dicembre) la Fed pubblica il *Summary of Economic Projections*, che include il "dot plot": 19 punti, uno per ciascun membro (votante e non), che indicano la proiezione individuale del funds rate. È anonimo. **[INTERPRETAZIONE]** Il *mediano* è il riferimento di mercato, ma la **dispersione** dei punti (molto ampia nel 2025–26) è essa stessa informazione: segnala disaccordo interno, che storicamente amplifica le oscillazioni dei prezzi (BlackRock: "Fed policy surprises, particularly those arising from internal divisions, have historically driven sharp asset price swings").

**Letteratura ad alta frequenza per la metodologia event study (≥6 paper):**

- **Gürkaynak, Sack & Swanson (2005, IJCB)** — Due fattori ("target" e "path"); le parole muovono i tassi lunghi più delle azioni. *Fondamento per separare la sorpresa di azione dalla sorpresa di guidance.*
- **Nakamura & Steinsson (2018, *Quarterly Journal of Economics*, 133(3):1283–1330)** — Identificazione ad alta frequenza su finestre di 30 minuti attorno agli annunci FOMC; documentano il **"Fed information effect"**: a un rialzo a sorpresa i mercati alzano anche le previsioni di crescita, perché l'annuncio rivela le credenze della Fed sui fondamentali, non solo sulla policy.
- **Bauer & Swanson (2023, *NBER Macroeconomics Annual*, vol. 37)** — "A Reassessment of Monetary Policy Surprises and High-Frequency Identification": **criticano il Fed information effect**, mostrando che le sorprese di policy sono correlate a dati macro/finanziari pubblici *precedenti* l'annuncio (R² del 10–40%). Lo spiegano col canale **"Fed response to news"**: il pubblico sottostima quanto la Fed reagirà ai dati. Estendono il dataset includendo i discorsi del Chair.
- **Romer & Romer (2004, *American Economic Review*, 94(4):1055–1084)** — "A New Measure of Monetary Shocks": misura **narrativa** degli shock 1969–1996, depurata da risposte endogene usando i Greenbook; gli shock così identificati hanno effetti su output e prezzi più ampi e rapidi degli indicatori convenzionali.
- **Alesina & Summers (1993, *Journal of Money, Credit and Banking*, 25(2):151–162)** — "Central Bank Independence and Macroeconomic Performance": nei paesi avanzati, maggiore indipendenza si associa a inflazione **più bassa e meno volatile** (1955–1988), senza costo in termini di crescita reale. *Pilastro empirico del perché i mercati prezzano l'indipendenza.*
- **Cukierman, Webb & Neyapti (1992, *World Bank Economic Review*, 6(3):353–398)** — "Measuring the Independence of Central Banks and Its Effect on Policy Outcomes": costruiscono un **indice legale aggregato su 72 paesi in quattro decenni**, scomposto in indipendenza del personale, di policy e finanziaria. Risultato: "Legal independence is inversely related to inflation in industrial, but not in developing, countries", dove conta di più il *turnover* dei governatori.

**Benvenuti aggiuntivi:**
- **Taylor (1993)** — La regola di Taylor, benchmark di policy.
- **Adrian, Crump & Moench (2013, *Journal of Financial Economics*)** — Modello affine a 5 fattori per il **term premium** (serie ACM della NY Fed dal 1961), il canale chiave per l'indipendenza.
- **Kim & Wright (2005)** — Stima alternativa del term premium (incorpora survey Blue Chip); utile come robustness all'ACM.
- **Sargent & Wallace (1981), "Unpleasant Monetarist Arithmetic"** — Quadro teorico della **fiscal dominance**: se il fisco è insostenibile, la banca centrale è alla fine costretta a monetizzare il debito, e l'inflazione diventa un fenomeno fiscale. *Rilevante per il rischio Trump/term premium 2026.*

### 2. Segmentazione per fasi di regime 2023–2026

#### Fase (a) — Plateau al tasso terminale (≈ 1 ago 2023 → 30 giu 2024)
**Driver:** disinflazione lenta + mercato del lavoro resiliente → "higher for longer".
**[FATTO]** Tasso terminale 5,25–5,50% raggiunto il **26 luglio 2023** (CPI giugno 2023 a 3,0%). La Fed tiene fermo per riunioni consecutive. Il SEP di settembre 2023 prevedeva ancora un possibile ulteriore rialzo.
**[INTERPRETAZIONE]** Regime caratterizzato da rendimenti reali restrittivi, picco dei Treasury a 10Y in ottobre 2023, narrazione "tassi al picco". Adatto come analogo per fasi di hold prolungato.

#### Fase (b) — Attesa di tagli / pivot dovish e falsi avvii (≈ 1 lug 2024 → 30 giu 2025)
**Driver:** pivot verso il lato occupazione del mandato; ripetuti riposizionamenti tra mercato e Fed.
- **[FATTO] 13 dicembre 2023:** il "Grande Pivot" — hold a 5,25–5,50% ma dot plot con **3 tagli per il 2024** (75bp, contro 50bp di settembre; mediana funds 4,6%). Powell ammette che i tagli sono "a discussion for us".
- **[FATTO] 18 settembre 2024:** taglio **50bp** (atteso conteso 25 vs 50), a 4,75–5,00%.
- **[FATTO] 18 dicembre 2024:** "hawkish cut" — taglio 25bp atteso a 4,25–4,50%, ma **dot plot 2025 revisionato a 3,9% (da 3,4%, cioè 2 tagli invece di 4)** e proiezione inflazione 2025 alzata a 2,5% da 2,1% (Fed SEP 18 dic 2024 via J.P. Morgan).
- **[INTERPRETAZIONE]** Fase ricca di "falsi avvii": il mercato anticipava più tagli di quanti la Fed ne consegnasse.

#### Fase (c) — Oil overhang / re-pricing hawkish (≈ 1 lug 2025 → 30 apr 2026)
**Driver:** shock energetico geopolitico che riapre il rischio inflattivo.
**[FATTO]** Guerra USA-Israele/Iran dal **28 febbraio 2026**; chiusura di fatto dello Stretto di Hormuz (≈20% del greggio mondiale). Sequenza CPI: gennaio 2,4% → marzo 3,3% → aprile 3,8% → **maggio 4,2%** (energia +23,5% a/a, benzina +40,5%, gasolio +58,9%; core 2,9%). Il funds rate resta a **3,50–3,75%** a giugno 2026.
**[FATTO]** I futures si spostano: CME FedWatch implica probabilità >50% di almeno un rialzo entro fine 2026. Beth Hammack (Cleveland Fed, 2 giugno 2026): "if recent trends continue, it may soon be appropriate to act".
**[INTERPRETAZIONE]** Dilemma classico da shock di offerta (Nela Richardson, ADP: "It's a supply shock... The Fed has limited tools to address supply-side disruptions"). La regola del manuale è "guardare attraverso" lo shock finché le aspettative restano ancorate — ma con CPI sopra il 4% e un nuovo Chair anti-inflazione, il margine si assottiglia.

#### Fase (d) — Pressioni sull'indipendenza e transizione della presidenza (≈ 1 mag 2026 → fine 2026)
**Driver:** interferenza politica e cambio di leadership.
**[FATTO]** Confluiscono: *Trump v. Cook* (Corte Suprema, udienza 21 gennaio 2026); indagine penale DOJ su Powell (subpoena sui costi di ristrutturazione, poi archiviata); conferma di Warsh (54–45, 13 maggio) e giuramento (22 maggio 2026).
**[INTERPRETAZIONE]** Perché conta: l'incertezza sulla successione e la percezione di una Fed "catturata" agiscono soprattutto sul **term premium** (compenso per rischio su scadenze lunghe) e sul **dollaro**, più che sui tassi a breve. Si veda la Sezione 4.

### 3. Catalizzatori discreti e datati

> Formato: **anchor date** — decisione/comunicazione — ATTESO vs REALIZZATO (sorpresa) — caratterizzazione qualitativa T+1/T+3/T+5/T+10 sugli asset target. **Rendimenti cumulati precisi → da calcolare nel Market Data Layer dell'utente.**

**Calendario FOMC 2023 (esiti):** 31 gen–1 feb (+25bp), 21–22 mar (+25bp), 2–3 mag (+25bp), 13–14 giu (hold), **25–26 lug (+25bp → 5,25–5,50%, terminale)**, 19–20 set (hold, SEP), 31 ott–1 nov (hold), **12–13 dic (hold, pivot dovish)**.

**Calendario FOMC 2024 (esiti):** 30–31 gen (hold), 19–20 mar (hold, SEP), 30 apr–1 mag (hold), 11–12 giu (hold, SEP), 30–31 lug (hold), **17–18 set (−50bp → 4,75–5,00%, SEP)**, 6–7 nov (−25bp), **17–18 dic (−25bp → 4,25–4,50%, SEP, hawkish cut)**.

**Calendario FOMC 2025 (esiti):** 28–29 gen (hold), 18–19 mar (hold, SEP), 6–7 mag (hold), 17–18 giu (hold, SEP), 29–30 lug (hold), **16–17 set (−25bp → 4,00–4,25%, SEP)**, 28–29 ott (−25bp), **9–10 dic (−25bp → 3,50–3,75%, SEP, hawkish cut)**.

**Calendario FOMC 2026 (esiti/previsti):** **27–28 gen (hold, voto 10–2)**, **17–18 mar (hold, SEP)**, **28–29 apr (hold, voto 8–4, ultima di Powell)**, **16–17 giu (atteso hold, SEP, prima di Warsh)**, 28–29 lug, 15–16 set (SEP), 27–28 ott, 8–9 dic (SEP).

---

**📌 26 luglio 2023 — Rialzo finale a 5,25–5,50%**
- **Decisione:** +25bp, 11° rialzo del ciclo. **Atteso vs realizzato:** pienamente prezzato (sorpresa ≈ 0).
- **[FATTO]** Reazione il giorno: Dow +82 punti, S&P e Nasdaq pressoché invariati, **Treasury yield in lieve calo**.
- **[INTERPRETAZIONE]** Esempio da manuale di "azione senza sorpresa" → reazione muta. Utile come baseline a basso impatto.

**📌 13 dicembre 2023 — Pivot dovish ("Grande Pivot")**
- **Decisione:** hold a 5,25–5,50%, ma **dot plot con 3 tagli 2024** (75bp; mediana 4,6%) e linguaggio addolcito ("any additional policy firming"). **Atteso vs realizzato:** **sorpresa dovish marcata** (mercato si aspettava toni più cauti).
- **[FATTO]** Reazione: **Dow a record storico sopra 37.000**, S&P +~1%, **2-year −25bp a ~4,5%** (poi −30bp nelle ore successive), **DXY −0,9%** (minimo da agosto), **oro +1% a 2.004,79 USD/oncia** (fonte: Deriv, TheStreet). ^TNX in calo, IEF in rialzo, EUR/USD in rialzo.
- **[INTERPRETAZIONE]** Caso scuola di "path factor" che domina: nessuna azione, ma rally cross-asset. Analogo ideale per "sorpresa dovish da guidance".

**📌 18 settembre 2024 — Taglio "jumbo" da 50bp**
- **Decisione:** −50bp a 4,75–5,00% (primo taglio in >4 anni). **Atteso vs realizzato:** mercato diviso 25 vs 50 (FedWatch ~63% per 50bp); **lieve sorpresa dovish sull'azione**, ma Powell frena ("not the beginning of a series of 50bp cuts").
- **[FATTO]** Reazione: trading volatile, Dow +375 punti intraday poi ripiega, **azioni chiudono leggermente in calo, Treasury yield rimbalzano al rialzo** (2-year swap −10bp poi recupero, 10-year −4bp). 
- **[INTERPRETAZIONE]** L'azione dovish è stata neutralizzata dalla guidance hawkish in conferenza → reazione ambivalente. Esempio di "azione e parole in conflitto".

**📌 18 dicembre 2024 — "Hawkish cut"**
- **Decisione:** −25bp a 4,25–4,50% (atteso), ma **dot plot 2025 a 3,9% (da 3,4%, 2 tagli invece di 4)**, inflazione 2025 a 2,5% (da 2,1%). **Atteso vs realizzato:** taglio prezzato, ma **forte sorpresa hawkish dalla guidance/SEP**.
- **[FATTO]** Reazione (J.P. Morgan): "**Equity markets sank nearly 3% immediately after the decision** on the hawkish rate cut Wednesday, **as interest rates across the curve rose by around 10 basis points**". S&P −~3%, Nasdaq −3,6%, Dow oltre −1.100 punti (serie negativa più lunga dal 1974). ^TNX su, IEF giù, DXY su, EUR/USD giù.
- **[INTERPRETAZIONE]** Il catalizzatore più violento del ciclo di tagli, e di nuovo guidato dalla *comunicazione* (il dot plot), non dall'azione. Analogo principe per "hawkish cut".

**📌 17 settembre 2025 — Primo taglio del 2025**
- **Decisione:** −25bp a 4,00–4,25%, voto 11–1 (Miran dissenziente per −50bp). **Atteso vs realizzato:** prezzato; "risk-management cut" (Powell).
- **[FATTO]** Reazione: azioni miste/modestamente su (Dow +~450 punti, S&P +0,1%, Nasdaq −0,3%), **Treasury yield in lieve calo** sulle scadenze sensibili. Il 10Y "barely moved" (NAHB).
- **[INTERPRETAZIONE]** Cut atteso, dissenso unico → reazione contenuta. Cook ha votato dopo che una corte d'appello aveva bloccato la sua rimozione (intreccio con l'indipendenza).

**📌 10 dicembre 2025 — Terzo taglio consecutivo, "hawkish cut"**
- **Decisione:** −25bp a **3,50–3,75%**; **voto diviso 9–3 con dissenso a tre vie** (Miran per −50bp; Schmid e Goolsbee per nessun taglio) — più "soft dissents" di 4 non votanti. **Dot plot mediana 2026 a 3,4% (da 2,9% di settembre)**, solo 1 taglio nel 2026 (fonte: Mariemont Capital, Fed SEP 10 dic 2025).
- **[FATTO]** Reazione: **Dow +500 punti, Treasury yield perlopiù in calo**; curva 2s10s ripida (+15bp nella settimana per Mariemont Capital). Powell: "we are well positioned to wait and see".
- **[INTERPRETAZIONE]** "Hawkish cut" con linguaggio (ripreso dal dicembre 2024) che alza l'asticella per i tagli futuri. La Fed conclude anche il QT e annuncia acquisti di T-bill per gestione delle riserve.

**📌 28–29 aprile 2026 — Ultima riunione di Powell come Chair**
- **Decisione:** hold a 3,50–3,75% (terzo consecutivo). **Voto 8–4 — il più diviso dall'ottobre 1992.** Dissensi: Miran (per −25bp) + tre membri (Hammack, Kashkari, Logan) contrari all'"easing bias" nello statement. **Atteso vs realizzato:** hold prezzato ~100%; **sorpresa = ampiezza del dissenso** (segnale hawkish interno).
- **[FATTO]** Statement: "developments in the Middle East are contributing to a high level of uncertainty"; inflazione "is elevated" (da "remains somewhat elevated"). Powell annuncia che resterà come governatore.
- **[INTERPRETAZIONE]** La spaccatura record segnala una Fed che fatica a trovare consenso sotto lo shock energetico, alzando il bar per tagli — di fatto un messaggio hawkish.

**📌 10 giugno 2026 — CPI maggio (dato macro, non FOMC)**
- **[FATTO]** CPI +4,2% a/a (massimo da aprile 2023), +0,5% m/m; energia +23,5% a/a (60% dell'aumento mensile); **core +0,2% m/m / 2,9% a/a (sotto attese)**. Reazione (Benzinga): 2-year −2bp a 4,11%, S&P futures −0,22%, DXY −0,11% a 99,54, **oro −0,50% a 4.158 USD/oncia**, WTI −0,17% a 88,92 USD.
- **[INTERPRETAZIONE]** Il core più freddo del previsto ha smorzato il pricing più aggressivo dei rialzi → reazione "misurata" nonostante il headline shock.

**Eventi su indipendenza/transizione (anchor dates):**
- **[FATTO] 1 ottobre 2025:** la Corte Suprema lascia Cook in carica (respinge l'appello d'emergenza dell'amministrazione) e fissa l'udienza a gennaio 2026.
- **[FATTO] 21 gennaio 2026:** udienza orale *Trump v. Cook*; tutti e nove i giudici esprimono dubbi sul potere di rimozione unilaterale (Kavanaugh: rimuovere governatori a piacimento "would weaken, if not shatter, the independence of the Federal Reserve").
- **[FATTO] 30 gennaio 2026:** Trump nomina Warsh Chair.
- **[FATTO] ~marzo–aprile 2026:** subpoena DOJ a Powell quashate dal giudice Boasberg (13 marzo: "essentially zero evidence"); DOJ archivia l'indagine (24 aprile); Tillis rimuove il blocco sul voto di commissione (26 aprile).
- **[FATTO] 21 aprile 2026:** audizione di Warsh alla Senate Banking Committee ("Inflation is a choice, and the Fed must take responsibility for it"; nega di aver promesso tagli alla Casa Bianca).
- **[FATTO] 13 maggio 2026:** Senato conferma Warsh **54–45** (Fetterman unico Dem a favore; margine più stretto di sempre).
- **[FATTO] 22 maggio 2026:** Warsh giurato 17° Chair (Powell pro tempore fino ad allora; Miran dimissionario).
- **[INTERPRETAZIONE]** Per l'event study, questi eventi non hanno "atteso vs realizzato" su un tasso, ma sorprese istituzionali → reazione attesa su **DXY (giù), oro (su), term premium (su)** se la percezione di indipendenza si erode (vedi Sez. 4). Reazioni puntuali di mercato a questi specifici eventi vanno verificate nel Market Data Layer dell'utente.

### 4. Indipendenza della banca centrale — perché i mercati ci tengono

**Il meccanismo.** **[FATTO]** La letteratura (Alesina & Summers 1993; Cukierman, Webb & Neyapti 1992) documenta che maggiore indipendenza si associa a inflazione più bassa e meno volatile. **[INTERPRETAZIONE]** Quando l'indipendenza è percepita a rischio, i mercati anticipano un *bias* inflazionistico futuro: anche se i tassi a breve oggi non cambiano, gli operatori chiedono più compenso per detenere debito lungo.

**Il canale del term premium.** **[FATTO]** Il modello ACM (Adrian, Crump & Moench 2013, NY Fed) scompone il rendimento di un Treasury in due parti: (i) aspettative sul percorso dei tassi a breve, e (ii) **term premium** — il compenso per rischio di tasso, incertezza d'inflazione e squilibri domanda/offerta. **[INTERPRETAZIONE]** La pressione politica sulla Fed colpisce soprattutto (ii): se gli investitori temono una Fed "catturata" che tollererà più inflazione, il term premium sale, irripidendo la curva (steepening) e indebolendo il dollaro — anche senza alcun cambio del funds rate. Sargent & Wallace (1981) forniscono il caso estremo della **fiscal dominance**: con debito insostenibile, la banca centrale è alla fine forzata a monetizzare, e l'inflazione diventa fiscale.

**Episodi storici comparati:**
- **[FATTO] Nixon-Burns (1971–72):** le registrazioni del "Nixon tapes" (Abrams 2006, *JEP*) mostrano Nixon che preme su Burns per allentare prima delle elezioni. Esito: contributo alla Grande Inflazione; tra il 6 novembre 1972 e l'agosto 1973 il rendimento del 10Y salì di oltre 130bp (NBC News). Drechsel (2024) stima che gli shock di pressione politica alzano inflazione e aspettative in modo persistente.
- **[FATTO] Truss mini-budget (23 settembre 2022):** ~£45 mld di tagli fiscali non finanziati senza previsione OBR; **il gilt a 30Y salì ~120bp in tre giorni**, la sterlina toccò 1,0350 (minimo storico), la BoE intervenne il 28 settembre con acquisti d'emergenza per evitare la spirale LDI dei fondi pensione. *Caso paradigmatico di credibilità fiscale che si rompe e si scarica su term premium e valuta.*
- **[FATTO] Turchia/Erdogan (2021–22):** Erdogan ("i tassi sono la madre di tutti i mali") forzò tagli con inflazione a doppia cifra licenziando tre governatori CBRT in ~2 anni; la **lira perse ~44% nel 2021**, l'inflazione superò l'80%. *Estremo di perdita totale d'indipendenza in un'economia emergente.*
- **[FATTO] BoE (1997):** la concessione dell'indipendenza operativa alla Bank of England è l'esempio opposto — un *aumento* di credibilità che abbassò le aspettative d'inflazione.

**[INTERPRETAZIONE] Applicazione al 2026:** alla notizia del tentativo di licenziare Cook (agosto 2025), le azioni hanno largamente "guardato oltre", ma **il dollaro ha ceduto e l'oro è salito** — coerente col canale term premium/valuta più che col canale tassi a breve. L'oro a >4.000 USD/oncia nel 2026 è, in parte, un'interpretazione di mercato sulle credenziali anti-inflazione di una Fed sotto pressione.

### 5. Divergenza Fed–BCE

**Il ciclo BCE 2023–2026.** **[FATTO]** Picco del tasso sui depositi al **4,00% (settembre 2023)**, dopo 450bp di rialzi dal luglio 2022. **Primo taglio il 6 giugno 2024** (−25bp), il primo dal 2019. Seguono tagli a settembre, ottobre, dicembre 2024 e nella prima metà del 2025: la BCE ha tagliato **otto volte**, portando il deposito **a 2,00% con effetto dall'11 giugno 2025** (comunicato BCE 5 giugno 2025: "the interest rates on the deposit facility, the main refinancing operations and the marginal lending facility will be decreased to 2.00%, 2.15% and 2.40% respectively, with effect from 11 June 2025"). Poi **hold prolungato**: la riunione del 18 dicembre 2025 ha lasciato il deposito al 2,00% (quarta pausa consecutiva), con inflazione vista stabilizzarsi al 2%.

**Tempistica relativa.** **[FATTO/INTERPRETAZIONE]**
- **2023 (in fase):** entrambe in modalità restrittiva (Fed al terminale a luglio, BCE a settembre).
- **Giugno–settembre 2024 (BCE in anticipo, poi convergenza):** la BCE taglia per prima (giugno), la Fed segue a settembre con un 50bp che riallinea le tempistiche.
- **2025–2026 (contro-fase crescente):** la BCE conclude il ciclo e si ferma al 2,0%, mentre la Fed, colpita dallo shock Hormuz, **inverte la traiettoria** verso un possibile rialzo. L'eurozona è anch'essa colpita dall'energia (CPI maggio 2026 +3,2%, con attese di mercato di un rialzo BCE a giugno 2026), ma la divergenza di *direzione attesa* è il driver.

**[INTERPRETAZIONE] Implicazioni per EUR/USD e flussi cross-Atlantico.** Quando la Fed è più hawkish della BCE (differenziale di tasso a favore del dollaro in allargamento), EUR/USD tende a scendere e i flussi vanno verso asset in dollari. Quando convergono o la Fed è più dovish, l'euro si rafforza. Nel 2026 si crea una situazione ambigua: il differenziale di tasso favorirebbe il dollaro (Fed potenzialmente in rialzo), ma il **rischio sull'indipendenza della Fed** spinge in direzione opposta (dollaro più debole). Per l'event study, EUR/USD nel regime 2026 risponde a **due forze contrapposte** — differenziale di policy vs premio per il rischio istituzionale USA — e non va modellato col solo carry.

### 6. Cosa NON trasferire (avvertenze metodologiche per l'event study)

**[INTERPRETAZIONE]** Il regime 2023–2026 contiene elementi specifici che rendono **rischioso** usarlo come analogo per cicli passati o futuri:

1. **Shock di offerta energetico esogeno (Stretto di Hormuz).** L'inflazione del 2026 è guidata da un *cost-push* geopolitico (core contenuto a 2,9%, headline a 4,2%), non da surriscaldamento della domanda. Mappare il 2026 su episodi di inflazione da domanda (es. 2021–22) confonde due meccanismi diversi: qui la Fed "non può abbassare il prezzo del petrolio", e la risposta di manuale sarebbe "guardare attraverso" lo shock. La reazione dei mercati al CPI di maggio (core freddo → reazione misurata) lo conferma.

2. **Attacco istituzionale all'indipendenza senza precedenti recenti USA.** *Trump v. Cook* è il **primo tentativo nella storia (113 anni) di rimuovere un governatore Fed**; l'indagine penale su un Chair in carica è anch'essa inedita nell'era moderna. I comovimenti dollaro/oro/term premium di questo regime riflettono un premio per il rischio istituzionale che **non esiste** nei dataset di FOMC "normali". Usare regressioni high-frequency stimate su campioni pre-2025 (Gürkaynak-Sack-Swanson, Nakamura-Steinsson) per prevedere reazioni nel 2026 sottostima la componente di rischio-coda.

3. **Transizione Powell→Warsh sotto pressione politica.** Il cambio di Chair coincide con un nuovo *bias* annunciato (Warsh favorevole a tassi più bassi ma anti-inflazione, critico del core PCE, intenzionato a ridurre la forward guidance/dot plot). **Le regole di comunicazione stesse potrebbero cambiare**: se Warsh ridimensiona il dot plot, il "path factor" — il principale motore di mercato nel 2023–24 — perde rilevanza come catalizzatore. Un event study calibrato sull'era Powell potrebbe non valere nell'era Warsh.

4. **Avvertenze tecniche generali:**
   - **Asset non in DB:** 2Y/front-end, fed funds futures/OIS, TIPS/breakeven (DFII10) non sono nel database; ma sono spesso i veri "luoghi" dove la sorpresa si manifesta per prima (Gürkaynak-Sack-Swanson). Le reazioni di ^TNX e IEF (10Y) catturano solo la parte lunga.
   - **Endogeneità (Bauer & Swanson 2023):** le sorprese di policy sono parzialmente prevedibili dai dati pre-annuncio (canale "Fed response to news"). Non trattare il movimento T+1 come puro shock esogeno.
   - **Finestre lunghe (T+5/T+10):** sono contaminate da altri eventi (dati macro, geopolitica). Più lunga la finestra, minore l'attribuzione causale all'evento FOMC.
   - **Dati CPI 2025 mancanti:** BLS non ha raccolto CPI per ottobre/novembre 2025 (shutdown); i confronti a/a che attraversano quel periodo usano stime imputate.

---

## Recommendations

**[INTERPRETAZIONE — indicazioni operative per il sistema di event study]**

1. **Pesare la sorpresa di guidance più di quella d'azione.** Per ogni evento FOMC, codificare due segnali separati: (a) sorpresa sull'azione (decisione vs consenso FedWatch) e (b) sorpresa sul *path*/dot plot (mediana e *dispersione* vs SEP precedente). Gli episodi di massimo impatto del periodo (13 dic 2023, 18 dic 2024, 10 dic 2025) sono stati guidati da (b). **Benchmark che cambia la regola:** se Warsh elimina o ridimensiona il dot plot (possibile dalla riunione del 16–17 giugno 2026), declassare il peso del fattore SEP e aumentare quello dei discorsi del Chair (coerente con Bauer-Swanson 2023, che raddoppiano il dataset includendo gli speech).

2. **Trattare gli eventi sull'indipendenza come shock di term premium/valuta, non di tasso.** Per Trump v. Cook, nomine/conferme, sviluppi DOJ: mappare la reazione attesa su **DXY (↓), oro (↑), curva 2s10s (steepening), breakeven (↑)** più che su ^TNX nominale o azioni. Usare gli analoghi Nixon-Burns, Truss e Turchia come riferimenti di magnitudine, distinguendo per grado di indipendenza residua.

3. **Nel regime "oil overhang", classificare gli shock CPI per composizione.** Separare headline vs core: un CPI headline alto ma core contenuto (come maggio 2026) produce reazioni *attenuate* perché i mercati anticipano che la Fed guarderà attraverso lo shock. **Soglia che cambierebbe lo scenario:** se il *core* accelera in modo persistente (>3,0–3,2% con dispersione in aumento), il rischio passa da "hold" a "rialzo" e la reazione dei tassi diventa molto più marcata.

4. **Modellare EUR/USD con due fattori in contro-tensione nel 2026.** Differenziale di policy Fed–BCE (pro-dollaro se la Fed è più hawkish) *vs* premio per il rischio istituzionale USA (anti-dollaro). Non usare il solo differenziale di tasso: nel 2026 può dare il segno sbagliato.

5. **Limitare le finestre lunghe per gli eventi recenti.** Per il regime 2025–26, privilegiare T+1/T+3 per l'attribuzione causale; usare T+5/T+10 solo con controllo esplicito per dati macro e sviluppi geopolitici (guerra Iran/Hormuz) intervenienti.

---

## Caveats

- **[FATTO/limite]** Alcune reazioni di mercato puntuali (livelli di indici, oro, DXY) provengono da fonti secondarie (CNBC, J.P. Morgan, Deriv, Benzinga) e si riferiscono alla reazione *intraday/giornaliera*, non a rendimenti cumulati T+N verificati. **Tutti i rendimenti cumulati esatti vanno ricalcolati nel Market Data Layer dell'utente.**
- **[Limite]** I dati e gli eventi del 2026 (CPI maggio, riunione aprile 8–4, conferma Warsh) sono recenti e provengono da fonti giornalistiche; vanno cross-checati con i comunicati primari federalreserve.gov e i dati BLS definitivi quando disponibili. La riunione del **16–17 giugno 2026 è prospettica**: tutte le probabilità citate (~89–98% di hold, odds di rialzo) sono *pricing di mercato* (CME FedWatch) e previsioni di analisti, **non esiti realizzati**.
- **[Conflitto di fonti segnalato]** Sul margine di conferma di Warsh, le fonti riportano sia **54–45** (CNBC, NPR, C-SPAN, Bloomberg) sia 55–45 (Consumer Finance Monitor); la cifra corroborata da più fonti primarie/dirette è **54–45**, con Fetterman unico Dem a favore e Gillibrand non votante.
- **[Conflitto di fonti segnalato]** Sul voto della riunione del 10 dicembre 2025, le fonti oscillano nel descrivere il conteggio (9–3 con tre dissensi formali è la lettura più coerente con i tre dissenzienti nominati: Miran, Schmid, Goolsbee); il dot plot mediana 2026 è riportato a 3,4%.
- **[Limite metodologico]** Le stime del term premium (ACM vs Kim-Wright) possono differire di centinaia di basis points; usare più stime congiuntamente. Il "Fed information effect" (Nakamura-Steinsson 2018) è contestato (Bauer-Swanson 2023): non assumere acriticamente che un rialzo a sorpresa alzi le aspettative di crescita.
- **[Avvertenza generale]** La distinzione FATTO/INTERPRETAZIONE è stata mantenuta nel testo. Le proiezioni su rialzi 2026, traiettoria Warsh ed evoluzione Hormuz sono scenari, non certezze.

```yaml
---
title: "Fed: reaction function, indipendenza e divergenza con la BCE (2023–2026)"
date_compiled: 2026-06-11
primary_theme: monetary_policy
sub_themes: [fed_reaction_function, dot_plot, forward_guidance, central_bank_independence, fed_ecb_divergence, term_premium, oil_overhang]
relevant_assets: [^TNX, IEF, ^GSPC, EURUSD=X, GC=F]
external_assets_mentioned:
  - "DXY / Dollar Index (proxy DX-Y.NYB) — citato come canale di trasmissione su indipendenza"
  - "2Y Treasury / front-end della curva — non in DB (in DB ^TNX 10Y e IEF 7-10Y)"
  - "Fed funds futures / OIS — non in DB"
  - "TIPS / breakeven d'inflazione (DFII10) — non in DB"
time_window:
  start: 2023-01-01
  end: 2026-12-31
regime_phases:
  - terminal_rate_plateau: 2023-08-01 to 2024-06-30
  - cut_expectations_and_false_starts: 2024-07-01 to 2025-06-30
  - oil_overhang_hawkish_repricing: 2025-07-01 to 2026-04-30
  - independence_pressure_and_transition: 2026-05-01 to 2026-12-31
keywords:
  - federal reserve
  - fomc
  - reaction function
  - taylor rule
  - dot plot
  - forward guidance
  - data dependence
  - dual mandate
  - rate cuts
  - hawkish hold
  - term premium
  - central bank independence
  - fed chair transition
  - fiscal dominance
  - fed ecb divergence
  - eur usd
  - dollar
  - breakeven inflation
  - high-frequency identification
  - fed information effect
  - oil overhang
---
```