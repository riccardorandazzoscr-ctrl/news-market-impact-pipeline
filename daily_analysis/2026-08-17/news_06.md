# Il Canada respinge l'offerta USA con i dazi al 50% in vigore mercoledi: Ottawa avverte che potrebbero far saltare il negoziato

**Data analisi**: 2026-08-17
**Fonte**: Morning Briefing 2026-08-17 (fin 09)
**Slug**: canada-50pct-tariffs-deadline

---

## Testo notizia (originale)

> I funzionari canadesi dicono di non essere soddisfatti dell'ultima proposta americana, che abbasserebbe alcuni dazi settoriali ma meno di quanto Ottawa chieda, e il capo negoziatore canadese ha avvertito le controparti che lasciar entrare in vigore i prelievi del 19 agosto potrebbe interrompere il negoziato. Washington chiede quote all'export su acciaio e alluminio, la rimozione dei dazi ritorsivi canadesi sull'auto, il ritorno degli alcolici americani sugli scaffali provinciali, la fine delle restrizioni sugli appalti provinciali e l'accettazione della lettura USA sulle quote sui latticini. Le due parti si incontrano quotidianamente a piu' livelli fino alla scadenza. E' la prima azione tariffaria da quando la Corte Suprema ha annullato i prelievi precedenti in febbraio, quindi mercoledi mette alla prova la base legale sostitutiva dell'amministrazione tanto quanto il Canada.

---

## In breve (in parole semplici)

Mercoledì 19 agosto entrano in vigore dazi americani al 50% sulle merci canadesi, salvo accordo dell'ultimo minuto. Un dazio è un'imposta che chi importa paga sulla merce che entra: alza il prezzo del bene straniero e, di fatto, riduce il commercio fra i due Paesi. Il Canada ha respinto l'ultima offerta americana, che riduceva alcuni dazi settoriali ma non abbastanza, e ha avvertito che lasciar scattare i prelievi potrebbe far saltare del tutto il tavolo.

Perché conta doppio: questa è la **prima azione tariffaria dopo che la Corte Suprema americana ha annullato i dazi precedenti a febbraio**. Quindi mercoledì non si testa solo la resistenza del Canada — si testa se la base giuridica alternativa su cui l'amministrazione ha ricostruito i dazi regge. Se regge, il precedente vale per ogni altro partner commerciale; se non regge, l'intera architettura tariffaria torna in discussione. È per questo che l'evento ha un'impronta molto più larga di un singolo rapporto bilaterale.

La domanda che ci poniamo: come si sono mossi dollaro canadese, azionario americano ed europeo, volatilità e rame dopo le precedenti escalation tariffarie?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | regulatory |
| `sub_themes` | tariff_escalation, trade_war |
| `sentiment` | risk-off |
| `confidence` | medium |
| `horizon` | 1-10 giorni di trading |

**Motivazione classificazione**: l'oggetto è una misura di politica commerciale con una data di entrata in vigore — un atto normativo, quindi `regulatory` (in alternativa `geopolitical`, e infatti il pool di analoghi è stato preso dal ramo geopolitico della libreria, che ha copertura molto più ampia sullo stesso token). Il sentiment è `risk-off`: i dazi riducono il commercio, comprimono i margini delle imprese esposte e aumentano l'incertezza. La `confidence` è **medium** perché l'esito resta aperto — le due parti si incontrano quotidianamente e c'è una possibilità concreta di accordo prima di mercoledì — e perché la scadenza è pubblica, quindi in parte già prezzata.

---

## Asset rilevanti

### Primary (canale diretto)
- **CAD=X** (cambio dollaro USA/dollaro canadese — quanti dollari canadesi per un dollaro americano; se il numero *sale*, il dollaro canadese si indebolisce) — è il canale più diretto e l'asset aggiunto al database il 2026-08-16 proprio per coprire gli attriti commerciali USA-Canada.
- **DX-Y.NYB** (indice del dollaro americano contro un paniere di valute) — canale aggregato delle misure commerciali.

### Secondary (effetti indiretti)
- **^GSPC** (indice azionario S&P 500) — le catene di fornitura nordamericane (auto, componentistica, ferrovie) sono integrate: un dazio al 50% colpisce anche produttori americani che comprano input canadesi.
- **^VIX** (indice di volatilità implicita sull'S&P 500) — l'incertezza sulla politica commerciale è storicamente uno dei principali driver della volatilità.
- **HG=F** (futures sul rame) — proxy della domanda industriale e delle materie prime scambiate nel blocco nordamericano.
- **^STOXX50E** (indice azionario Euro Stoxx 50) — canale di contagio: un precedente legale che regge in Canada aumenta la probabilità che lo stesso strumento venga usato verso l'Europa.

---

## Knowledge Base — research correlate

- [score=2] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/...md` — *Dazi e guerra commerciale USA*
  - Perché è rilevante: è la research dedicata a questo canale, con la mappa delle fasi (prima guerra commerciale 2018-2019, tregua 2020, seconda ondata dal 2025) e degli episodi datati usati come analoghi.
- [score=1] `PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/...md`
  - Perché è rilevante: gran parte degli episodi tariffari storici sono USA-Cina, e questa research fornisce il lato ricevente.

⚠ **Lacuna parziale**: la research sui dazi è centrata sull'asse USA-Cina. Il canale **USA-Canada/USMCA** (integrazione delle catene del valore nordamericane, energia, auto) e soprattutto la **dimensione giuridica** (quale autorità legale sostiene i dazi dopo la sentenza della Corte Suprema di febbraio 2026) non sono coperti. Segnalato in `_index.md`.

---

## Regime storico identificato

- **Regime**: `second_wave_tariffs_2025_2026` (2025-01-01 → oggi), dalla research sui dazi.
- **Caratterizzazione**: dal gennaio 2025 i dazi sono tornati a essere uno strumento di politica economica ricorrente e non eccezionale, applicato a più partner in parallelo e con scadenze ravvicinate usate come leva negoziale. La differenza rispetto alla prima guerra commerciale del 2018-2019 è duplice. Primo, il mercato si è **abituato**: le scadenze tariffarie hanno prodotto reazioni progressivamente più contenute man mano che diventava chiaro che molte venivano prorogate o rinegoziate all'ultimo (il pattern noto come "TACO trade" — il mercato scommette che l'escalation rientri). Secondo, e nuovo dal febbraio 2026, c'è un **vincolo giudiziario**: la Corte Suprema ha annullato la base legale dei prelievi precedenti, quindi ogni nuova azione è anche un test di tenuta della base giuridica sostitutiva. Questo secondo elemento non ha precedenti nel campione storico.

---

## Event study

### Episodi storici analoghi selezionati

Il tema `regulatory` ha una libreria piccola (19 episodi totali, 15 con il token `tariff_escalation`). Il ramo `geopolitical` della libreria porta lo stesso token con copertura molto maggiore (39 episodi date-locali), quindi il pool è stato preso da lì:

```bash
venv/bin/python analogues.py find --theme geopolitical --subtheme tariff_escalation \
  --direction neg --before 2026-08-17
# [30 episodi · sotto-tema 'tariff_escalation' su etichette date-locali: 39 episodi]
# [cap recency: tenuti i 30 più recenti]
```

Le 30 date si dividono in due blocchi di regime:
- **Prima guerra commerciale (2018-2020)**, 12 episodi: `2018-03-23` (dazi acciaio/alluminio Sezione 232), `2018-06-15`, `2018-07-02`, `2018-07-06` (entrata in vigore dei dazi su 34 miliardi di merci cinesi), `2018-10-10`, `2018-12-26`, `2019-05-13` (ritorsione cinese), `2019-08-01` (annuncio dei dazi sui restanti 300 miliardi), `2019-08-12`, `2019-09-01`, `2019-12-13` (accordo di "fase uno"), `2020-02-14`.
- **Seconda ondata (2024-2026)**, 18 episodi: `2024-12-15`, `2025-01-01`, `2025-01-14`, **`2025-02-01`** e **`2025-03-04`** — questi due sono i più pertinenti in assoluto, perché sono proprio le date dei dazi su Canada e Messico — `2025-02-10`, `2025-02-27`, `2025-03-26`, `2025-04-02` ("Liberation Day"), `2025-04-04`, `2025-04-08`, `2025-04-09` (la sospensione di 90 giorni), `2025-05-19`, `2025-07-30`, `2025-10-09`, `2025-10-30`, `2025-11-10`, `2026-07-13`.

Il pool è stato lasciato integro: potare i soli episodi USA-Cina avrebbe ridotto N a un livello non utilizzabile, e il canale di trasmissione (incertezza commerciale → risk-off, dollaro, volatilità) è comune.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'CAD=X,^GSPC,DX-Y.NYB,^STOXX50E,^VIX,HG=F' \
  --events 2018-03-23,2018-06-15,2018-07-02,2018-07-06,2018-10-10,2018-12-26,2019-05-13,2019-08-01,2019-08-12,2019-09-01,2019-12-13,2020-02-14,2024-12-15,2025-01-01,2025-01-14,2025-02-01,2025-02-10,2025-02-27,2025-03-04,2025-03-26,2025-04-02,2025-04-04,2025-04-08,2025-04-09,2025-05-19,2025-07-30,2025-10-09,2025-10-30,2025-11-10,2026-07-13 \
  --windows 1,3,5,10 \
  --markdown
```

### Risultati

**`CAD=X` — cambio USD/CAD** (N=30) — *un valore positivo = dollaro canadese più debole*

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.03% | -0.12% | -0.29% | -0.48% |
| mediana | **+0.11%** | **+0.02%** | **-0.11%** | **-0.09%** |
| dev std | 0.59% | 1.04% | 0.98% | 1.32% |
| p25 | -0.12% | -0.39% | -0.80% | -1.32% |
| p75 | +0.28% | +0.52% | +0.20% | +0.46% |

**`^GSPC` — S&P 500** (N=30)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.30% | +0.02% | +0.05% | -0.45% |
| mediana | **+0.23%** | **-0.17%** | **-0.61%** | **-0.05%** |
| dev std | 2.34% | 3.18% | 2.77% | 3.62% |
| p25 | -0.38% | -1.32% | -1.55% | -2.67% |
| p75 | +1.03% | +1.11% | +1.37% | +1.66% |

**`DX-Y.NYB` — indice del dollaro** (N=30)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.26% | -0.46% | -0.73% | -1.06% |
| mediana | **-0.16%** | **-0.48%** | **-0.67%** | **-0.65%** |
| dev std | 0.54% | 1.05% | 1.22% | 1.58% |

**`^STOXX50E` — Euro Stoxx 50** (N=30)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.07% | -0.08% | +0.31% | +0.37% |
| mediana | **+0.23%** | **+0.21%** | **+0.32%** | **+0.77%** |
| dev std | 1.82% | 3.32% | 3.37% | 5.26% |
| p25 | -0.98% | -1.51% | -1.22% | -1.28% |

**`^VIX` — volatilità implicita S&P 500** (N=30)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.44% | +4.37% | +3.41% | +6.42% |
| mediana | **-1.47%** | **-0.50%** | **-1.93%** | **-3.15%** |
| dev std | 14.32% | 28.62% | 26.58% | 37.04% |
| p25 | -7.45% | -12.75% | -16.91% | -14.25% |
| p75 | +3.63% | +12.74% | +14.83% | +17.92% |

**`HG=F` — rame** (N=30)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.94% | -0.95% | -0.28% | +0.28% |
| mediana | **-0.27%** | **+0.16%** | **-0.29%** | **-0.49%** |
| dev std | 4.66% | 6.10% | 6.77% | 8.18% |

---

## Considerazioni qualitative

**Il dollaro canadese: reazione minima e di segno controintuitivo dopo qualche giorno.** `CAD=X` ha mediana **+0,11% a T+1** (dollaro canadese leggermente più debole, come ci si aspetterebbe) ma già a T+5 e T+10 le mediane girano negative (**−0,11%** e **−0,09%**, cioè dollaro canadese che *recupera*). La dispersione è modesta (deviazione standard 1,3% a T+10) e il p25 arriva a −1,32%. La lettura più onesta: **nessun segnale direzionale utilizzabile**, con un lieve indebolimento nel primo giorno che si riassorbe. Due avvertenze importanti: (a) `CAD=X` è entrato nel database solo il 2026-08-16, quindi non compare nella scorecard e la sua affidabilità non è mai stata validata dal nostro processo; (b) la stragrande maggioranza degli episodi del pool riguarda dazi verso la **Cina**, non verso il Canada, e per un cambio bilaterale l'identità del paese colpito conta molto. Le due date davvero pertinenti — `2025-02-01` e `2025-03-04`, i dazi su Canada e Messico — sono solo 2 su 30.

**L'indice del dollaro scende, e questo è un risultato che va letto ma non usato.** `DX-Y.NYB` ha mediane negative e monotòne (**−0,65% a T+10**), cioè il dollaro si è indebolito dopo le escalation tariffarie. Economicamente ha senso: un dazio è una tassa sull'economia che lo impone quanto su quella che lo subisce, e i mercati valutari nel 2025 hanno reagito alle escalation trattando il dollaro come l'asset dell'incertezza, non come il rifugio. **Ma `DX-Y.NYB` è marcato ❌ controproducente nella scorecard 2026-W33** (IC −0,11, hit-rate **31%** su 130 previsioni — il peggior hit-rate della tabella). Riportiamo il numero e **dichiariamo che il segno storico è inaffidabile**: non se ne trae direzione attesa.

**L'azionario americano: il pattern "cedi e recupera".** `^GSPC` fa **+0,23% a T+1** (spesso l'annuncio arriva dopo che il mercato ha già scontato il peggio), poi **−0,17% a T+3** e **−0,61% a T+5**, per tornare piatto a T+10 (**−0,05%**). Il quartile inferiore però racconta il rischio: p25 a **−2,67% a T+10**. Tradotto: nella maggioranza dei casi l'S&P 500 non si muove in modo significativo, ma in un quarto degli episodi a due settimane perdeva quasi il 3%. È la firma di un evento con **distribuzione asimmetrica**: molte volte non succede nulla (l'accordo arriva, la scadenza slitta), poche volte succede molto. La scorecard marca `^GSPC` ⚠️ debole (IC +0,09, N=372): mediana da trattare come indicativa.

**L'Europa fa meglio dell'America, e non è un caso.** `^STOXX50E` ha mediane **positive a tutti gli orizzonti** (+0,77% a T+10) dove l'S&P 500 è piatto o negativo. Il meccanismo è il *reindirizzamento commerciale*: quando due grandi blocchi si tassano a vicenda, i flussi cercano percorsi alternativi e i terzi ne beneficiano marginalmente — oltre al fatto che i dazi USA-Cina non colpiscono direttamente le imprese europee. L'Euro Stoxx 50 è ✅ affidabile in scorecard (IC +0,16, N=157), quindi questa è la lettura direzionale meglio supportata della scheda. **Attenzione però al limite dell'analogia**: questa volta il precedente giuridico che si testa mercoledì potrebbe *estendersi* all'Europa. Se i dazi post-sentenza reggono in tribunale, l'Europa passa da terzo beneficiario a prossimo bersaglio — un canale che nessuno degli episodi storici cattura.

**La volatilità: mediana in calo, media in salita — la firma delle code.** `^VIX` ha mediana negativa a tutti gli orizzonti (**−3,15% a T+10**) ma media fortemente positiva (**+6,42%**), con deviazione standard 37% e un intervallo p25-p75 che a T+10 va da **−14,25% a +17,92%**. È la stessa asimmetria vista sull'S&P 500, ma amplificata: nella maggior parte dei casi la scadenza tariffaria passa e la volatilità si sgonfia; in una minoranza (aprile 2025, "Liberation Day") esplode. Poiché `^VIX` è l'asset più affidabile della scorecard (✅, IC +0,27), il segnale mediano — compressione della volatilità — merita peso, ma va accompagnato dall'avvertenza che è precisamente il tipo di evento in cui la mediana è la statistica meno interessante.

**Il rame: nessun segnale.** `HG=F` ha mediane sotto lo 0,5% in valore assoluto con deviazione standard fra 4,7% e 8,2%. Il rame è il termometro della domanda industriale globale ed è troppo lontano dal canale bilaterale USA-Canada per reagire in modo riconoscibile.

**La lettura che conta è quella giuridica, e l'event study non la può misurare.** Il briefing individua il punto: mercoledì testa "l'autorità legale sostitutiva dell'amministrazione tanto quanto il Canada". Nessuno dei 30 episodi storici contiene questa dimensione — tutti si svolgono in un mondo in cui la base giuridica dei dazi non era in discussione. Un esito che confermi la nuova base legale è, in prospettiva, molto più rilevante del 50% sul Canada: rende lo strumento tariffario nuovamente disponibile e prevedibile verso ogni partner, Europa inclusa. Un esito che la metta in dubbio rimette in discussione l'intero impianto. **Questo è il vero contenuto informativo della settimana, ed è un rischio binario e di lungo periodo che una finestra 1-10 giorni non cattura.**

---

## Glossario — sigle e termini

- **Dazio / tariffa** — imposta applicata sulle merci importate; la paga l'importatore e in larga parte si scarica sul prezzo finale.
- **Dazi ritorsivi** — dazi imposti in risposta a quelli di un altro Paese.
- **Sezione 232** — norma commerciale americana che consente dazi per motivi di sicurezza nazionale (usata su acciaio e alluminio nel 2018). **Sezione 301** — norma che consente dazi in risposta a pratiche commerciali sleali (usata contro la Cina).
- **USMCA** — l'accordo commerciale fra Stati Uniti, Messico e Canada che ha sostituito il NAFTA nel 2020.
- **"Liberation Day"** — il 2 aprile 2025, giorno dell'annuncio dei dazi generalizzati statunitensi; uno degli episodi più violenti del campione.
- **Quote all'export** — limiti quantitativi che il Paese esportatore accetta di auto-imporre, alternativa negoziale al dazio.
- **CAD=X** — cambio USD/CAD: quanti dollari canadesi per un dollaro americano. Numero che **sale** = dollaro canadese che si **indebolisce**.
- **DX-Y.NYB** — indice del dollaro (*Dollar Index*), il dollaro contro un paniere di sei valute.
- **^GSPC / ^STOXX50E / ^VIX / HG=F** — S&P 500 / Euro Stoxx 50 / indice di volatilità implicita / futures sul rame.
- **Reindirizzamento commerciale** (*trade diversion*) — quando dazi fra due Paesi spostano i flussi commerciali verso Paesi terzi.
- **p25 / p75** — i valori che separano rispettivamente il quarto peggiore e il quarto migliore degli episodi; misurano la dispersione meglio della sola deviazione standard quando la distribuzione ha code.
- **IC (Information Coefficient)** — correlazione fra direzione prevista e realizzata; negativo = previsione sistematicamente rovesciata.

---

## Caveat

- **Il pool è quasi tutto USA-Cina.** Solo 2 delle 30 date (`2025-02-01`, `2025-03-04`) riguardano dazi su Canada e Messico. Per `CAD=X` — un cambio bilaterale — questo è un limite grave: gli altri 28 episodi misurano la reazione del dollaro canadese a eventi che non lo riguardavano direttamente. Le mediane su `CAD=X` vanno lette come "reazione del CAD al rumore tariffario generale", non come "reazione a un dazio sul Canada".
- **`CAD=X` non è mai stato validato.** È entrato nel database il 2026-08-16 e non compare nella scorecard (serve un minimo di 50 previsioni mature). Non abbiamo alcuna misura della sua affidabilità nel nostro processo.
- **`DX-Y.NYB`: segno storico inaffidabile** — marcato ❌ controproducente nella scorecard 2026-W33, con il peggior hit-rate della tabella (31%). Nessuna direzione attesa viene tratta sul dollaro.
- **Mixing di regimi.** 12 episodi appartengono alla prima guerra commerciale (2018-2020), 18 alla seconda ondata (2024-2026). Nella seconda il mercato ha imparato che molte scadenze slittano, e le reazioni si sono progressivamente attenuate: mescolarle abbassa artificialmente l'ampiezza attesa delle reazioni "vere".
- **Distribuzione fortemente asimmetrica.** Su `^VIX` e `^GSPC` la mediana suggerisce "non succede nulla" mentre il p25 e la media raccontano una coda pesante. Su questo tipo di evento la tendenza centrale è la statistica meno utile: conviene ragionare sulla distribuzione, non sul valore atteso.
- **La dimensione giuridica non è nel campione.** Nessuno dei 30 episodi si è svolto dopo una sentenza che invalidava la base legale dei dazi. È l'elemento più rilevante di mercoledì ed è, per costruzione, fuori dall'event study.
- **Evento a scadenza pubblica e possibile accordo dell'ultimo minuto.** Le parti si incontrano quotidianamente: l'esito modale storico in questo regime è la proroga o l'accordo parziale, non l'entrata in vigore piena.
- **Lacuna di KB** sul canale USA-Canada/USMCA e sulla dimensione giuridica dei dazi post-sentenza (vedi `_index.md`).
- Correlazione ≠ causazione.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-16T19:11:12
- Scorecard consultata: `daily_analysis/_scorecard/2026-W33.md`, sezione 5-bis
