# Trump congela per tre giorni i dazi al 50% sul Canada a meno di due ore dalla scadenza: 'c'e' un accordo', ma solo sulla carta

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (fin 01)
**Slug**: canada-tariff-pause-3days

---

## Testo notizia (originale)

> Poco prima della scadenza delle 00:01 di mercoledi', Trump ha annunciato su Truth Social di aver sospeso 'per un periodo di tre giorni' i dazi al 50% su circa 20 miliardi di dollari di importazioni canadesi, 'sulla base del fatto che Canada e Stati Uniti, subordinatamente alla finalizzazione dei documenti, hanno un ACCORDO!'. Il primo ministro Mark Carney ha confermato che la sospensione corre fino al 22 agosto e ha parlato di 'progressi sostanziali' con lavoro importante ancora da fare. Il dossier automobilistico - Washington ferma a un minimo del 15% contro il 10% chiesto da Ottawa - era l'ostacolo principale ancora lunedi'. I dazi sarebbero stati imposti in base alla Section 338, strumento legale sostitutivo dopo che la Corte Suprema a febbraio aveva annullato i dazi precedenti: il nuovo fondamento giuridico resta non testato. Una proroga di tre giorni e' un espediente negoziale, non una risoluzione: il rischio e' rinviato a sabato, non rimosso.

---

## In breve (in parole semplici)

A meno di due ore dalla scadenza di mezzanotte, il presidente americano ha annunciato su Truth Social di aver sospeso **per tre giorni** i dazi al 50% su circa 20 miliardi di dollari di merci canadesi, perché — scrive — "c'è un ACCORDO", subordinato però alla finalizzazione dei documenti. Il primo ministro canadese Mark Carney ha confermato la sospensione fino al 22 agosto, aggiungendo che "resta lavoro importante da fare".

Perché è meno tranquillizzante di quanto sembri: tre giorni non sono una soluzione, sono uno strumento negoziale. **Il rischio non è rimosso, è rinviato a sabato.** E il fondamento giuridico dei dazi — la Section 338, adottata dopo che a febbraio la Corte Suprema aveva annullato i dazi precedenti — non è mai stato testato in tribunale.

Ci chiediamo: come si sono comportati storicamente il dollaro canadese e la borsa di Toronto attorno a una svolta sui dazi?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | regulatory |
| `sub_themes` | tariff_escalation, nafta_usmca |
| `sentiment` | risk-on (ma di brevissima durata per costruzione) |
| `confidence` | low |
| `horizon` | 1-5 giorni di trading — con l'avvertenza che la scadenza vera è il 22 agosto |

**Motivazione classificazione**: `regulatory` è la categoria del progetto per dazi e misure commerciali, ed è quella che nella mappa asset associa direttamente **CAD=X** e **^GSPTSE** (entrambi aggiunti al database rispettivamente il 2026-08-16 e il 2026-08-18, proprio perché il canale dazi USA-Canada era diventato ricorrente e strutturalmente invisibile). Il sotto-tema canonico è `tariff_escalation`, con 17 episodi a etichetta date-locale nella libreria. Sentiment `risk-on` perché la notizia rimuove — temporaneamente — un rischio noto e datato. **Confidence `low`** ed è la scelta più importante della scheda: una sospensione di tre giorni ha per costruzione un orizzonte inferiore alla finestra dell'event study, quindi la nostra finestra a T+5 e T+10 misura un mondo in cui la scadenza è **già passata di nuovo**. Il segnale che possiamo estrarre è debole per ragioni strutturali, non statistiche.

---

## Asset rilevanti

### Primary (canale diretto)
- **CAD=X** (cambio dollaro USA/dollaro canadese) — il canale valutario diretto degli attriti commerciali USA-Canada. ⚠ Attenzione al verso della quotazione: CAD=X è **USD per CAD invertito**, cioè quanti dollari canadesi per un dollaro USA. Un valore **in salita** significa **dollaro canadese più debole**.
- **^GSPTSE** (indice azionario S&P/TSX Composite, borsa di Toronto) — l'asset azionario più esposto ai dazi USA: banche, ferrovie, componentistica auto ed energia canadesi.

### Secondary (effetti indiretti)
- **^GSPC** (indice S&P 500) — il canale USA: i dazi sono un costo di input per gli industriali e i distributori americani.
- **DX-Y.NYB** (indice del dollaro) — canale aggregato delle misure commerciali. *Escluso dall'analisi direzionale*: è ❌ controproducente in scorecard.
- **^VIX** (indice della volatilità implicita sull'S&P 500) — misura se il rinvio riduce la domanda di protezione.

---

## Knowledge Base — research correlate

- [score=1] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/…md`
  - Perché è rilevante: è l'unica research del catalogo che copre il tema dazi, e fornisce la cronologia degli episodi 2018-2026.
  - ⚠ **Punteggio bassissimo (1) e nessun match sugli asset**: la research esistente è costruita sul canale **USA-Cina**, non su quello **USA-Canada**. Nessun documento del knowledge base copre il quadro USMCA/NAFTA, la Section 338, né la trasmissione dei dazi al dollaro canadese e alla borsa di Toronto. **È una lacuna di knowledge base, annotata in `_index.md`.**
- [score=1] `ASEAN : Sud-Est asiatico- shock geopolitici (2010–2026)/…md` — match puramente lessicale sul termine "tariff", non rilevante nel merito.

---

## Regime storico identificato

- **Regime**: dazi come strumento negoziale ricorrente e a scadenze brevi (2025-2026), con incertezza giuridica sul fondamento normativo.
- **Caratterizzazione**: rispetto al 2018-2019, quando i dazi erano annunciati come misure durature con tabelle di marcia pluriennali, il regime attuale usa la **scadenza breve** come leva: si annuncia una data, la si sposta di pochi giorni, si estrae una concessione. Questo cambia la natura statistica dell'evento: non è uno shock di regime, è una **mossa in una trattativa ripetuta**. Il briefing lo dice senza giri di parole: *"una proroga di tre giorni è un espediente negoziale, non una risoluzione"*.
- Elemento specifico e non trascurabile: la Corte Suprema ha annullato a febbraio 2026 i dazi precedenti, e l'amministrazione ha ripiegato sulla **Section 338**, una norma del Tariff Act del 1930 mai usata in epoca moderna. Il rischio non è quindi solo commerciale ma **giuridico**: anche se i dazi entrassero in vigore, potrebbero essere annullati. Questo aggiunge un secondo strato di incertezza che gli analoghi 2018-2019 non contengono.
- Nodo negoziale aperto: il settore automobilistico, con Washington ferma a un minimo del 15% contro il 10% chiesto da Ottawa.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria (Opzione B) con:
`--theme regulatory --subtheme tariff_escalation --direction pos --before 2026-08-19`
→ 13 episodi (il token ha 17 episodi a etichetta date-locale, ridotti dal filtro temporale).

⚠ **Filtro di direzione fallito — da dichiarare in modo esplicito.** La diagnostica della libreria riporta: *"direzione 'pos' stretta dava solo **0** episodi (<12) → incluso mixed/sconosciuto"*. Cioè: **nella libreria non esiste nemmeno un episodio di dazi etichettato come direzionalmente positivo**. Il pool che stiamo usando è quindi un insieme di **giornate di notizie sui dazi**, in maggioranza escalation. Usarlo come analogo di una *distensione* è metodologicamente scorretto se non lo si dichiara. Lo dichiariamo, e presentiamo due tabelle:

**(A) Pool completo della libreria (N=13)** — da leggere come *profilo di volatilità attorno a un titolo sui dazi*, non come previsione direzionale:
`2018-03-22` (annuncio dei dazi Section 301 → escalation), `2018-06-15` (lista da 50 miliardi → escalation), `2018-07-02`, `2018-09-17` (dazi su 200 miliardi al 10%, **meno del temuto** → sollievo parziale), `2018-10-10` (selloff), `2018-12-26` (rimbalzo di Santo Stefano), `2019-05-13` (ritorsione cinese → escalation), `2019-08-12`, `2024-12-15`, `2025-01-14` (indiscrezione su dazi graduali → sollievo), `2025-02-27`, `2025-04-02` ("Liberation Day", **la più grande escalation del campione**), `2025-04-30`.

**(B) Sottoinsieme di distensione/sollievo (N=7, INDICATIVE ONLY)** — potatura dell'analista che tiene solo gli episodi in cui la notizia era *meno grave del temuto* o rappresentava un passo indietro: `2018-09-17`, `2018-12-26`, `2019-08-12`, `2024-12-15`, `2025-01-14`, `2025-02-27`, `2025-04-30`. Il meccanismo comune è: **rimozione o attenuazione di un rischio già prezzato → rientro del premio per il rischio, non miglioramento dei fondamentali**.

Nessun episodio è specifico al Canada: il campione è dominato dal canale USA-Cina (vedi lacuna di knowledge base sopra).

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme regulatory --subtheme tariff_escalation \
  --direction pos --before 2026-08-19

# (A) pool completo
venv/bin/python event_study.py --ticker 'CAD=X,^GSPTSE,^GSPC,DX-Y.NYB,^VIX' \
  --events 2018-03-22,2018-06-15,2018-07-02,2018-09-17,2018-10-10,2018-12-26,2019-05-13,2019-08-12,2024-12-15,2025-01-14,2025-02-27,2025-04-02,2025-04-30 \
  --windows 1,3,5,10 --markdown

# (B) sottoinsieme di distensione
venv/bin/python event_study.py --ticker 'CAD=X,^GSPTSE,^GSPC,^VIX' \
  --events 2018-09-17,2018-12-26,2019-08-12,2024-12-15,2025-01-14,2025-02-27,2025-04-30 \
  --windows 1,3,5,10 --markdown
```

### Risultati — (A) pool completo della libreria, N=13

### Event study — `CAD=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.19% | +0.30% | +0.07% | -0.16% |
| mediana | +0.16% | +0.23% | +0.02% | +0.18% |
| dev std | +0.40% | +0.74% | +0.65% | +1.29% |
| p25 | -0.08% | -0.07% | -0.39% | -1.11% |
| p75 | +0.30% | +0.70% | +0.29% | +0.76% |
| **N** | **13** | **13** | **13** | **13** |



### Event study — `^GSPTSE`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.13% | -0.82% | +0.08% | -0.08% |
| mediana | +0.40% | +0.45% | +0.78% | -0.22% |
| dev std | +1.32% | +3.05% | +2.34% | +3.04% |
| p25 | -0.19% | -1.39% | -0.21% | -1.25% |
| p75 | +0.70% | +0.82% | +1.44% | +1.57% |
| **N** | **13** | **13** | **13** | **13** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.18% | -0.69% | +0.21% | -0.47% |
| mediana | +0.54% | -0.44% | +0.84% | -0.34% |
| dev std | +1.88% | +3.51% | +2.08% | +4.10% |
| p25 | -0.49% | -1.25% | -0.89% | -3.17% |
| p75 | +0.86% | +1.46% | +1.12% | +3.04% |
| **N** | **13** | **13** | **13** | **13** |



### Event study — `DX-Y.NYB`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.13% | -0.14% | -0.28% | -0.28% |
| mediana | -0.04% | -0.46% | -0.26% | +0.28% |
| dev std | +0.61% | +0.80% | +1.07% | +1.79% |
| p25 | -0.47% | -0.63% | -0.80% | -1.16% |
| p75 | +0.22% | +0.36% | +0.32% | +0.84% |
| **N** | **13** | **13** | **13** | **13** |



### Event study — `^VIX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.83% | +7.77% | -3.55% | -0.57% |
| mediana | -0.40% | -4.29% | -14.44% | -8.39% |
| dev std | +14.38% | +39.92% | +23.28% | +25.16% |
| p25 | -7.10% | -14.29% | -19.29% | -14.84% |
| p75 | +6.56% | +6.76% | +14.23% | +16.71% |
| **N** | **13** | **13** | **13** | **13** |

### Risultati — (B) sottoinsieme di distensione, N=7 (INDICATIVE ONLY)

### Event study — `CAD=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.10% | +0.42% | -0.03% | -0.12% |
| mediana | +0.06% | +0.26% | +0.02% | +0.27% |
| dev std | +0.33% | +0.83% | +0.64% | +1.37% |
| p25 | -0.09% | +0.10% | -0.42% | -0.69% |
| p75 | +0.15% | +0.89% | +0.33% | +0.74% |
| **N** | **7** | **7** | **7** | **7** |

> ⚠ **INDICATIVE ONLY** — campione N=7 < 10. Non trattare come evidenza robusta.


### Event study — `^GSPTSE`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.48% | -0.29% | +0.48% | +0.98% |
| mediana | +0.70% | +0.45% | +0.78% | +0.14% |
| dev std | +0.47% | +1.87% | +1.80% | +3.20% |
| p25 | +0.15% | -1.80% | -0.59% | -0.92% |
| p75 | +0.76% | +1.05% | +1.57% | +3.40% |
| **N** | **7** | **7** | **7** | **7** |

> ⚠ **INDICATIVE ONLY** — campione N=7 < 10. Non trattare come evidenza robusta.


### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.94% | +0.15% | +0.46% | +0.93% |
| mediana | +0.86% | +1.45% | +1.06% | +1.24% |
| dev std | +0.77% | +2.18% | +2.16% | +4.31% |
| p25 | +0.58% | -1.32% | -1.22% | -1.66% |
| p75 | +1.55% | +1.52% | +1.27% | +4.29% |
| **N** | **7** | **7** | **7** | **7** |

> ⚠ **INDICATIVE ONLY** — campione N=7 < 10. Non trattare come evidenza robusta.


### Event study — `^VIX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -5.46% | +3.80% | -5.59% | -8.26% |
| mediana | -6.51% | -4.29% | -10.82% | -11.49% |
| dev std | +8.46% | +28.32% | +15.67% | +19.90% |
| p25 | -10.47% | -14.19% | -17.80% | -18.45% |
| p75 | -0.94% | +5.85% | +4.79% | +4.16% |
| **N** | **7** | **7** | **7** | **7** |

> ⚠ **INDICATIVE ONLY** — campione N=7 < 10. Non trattare come evidenza robusta.

**In pratica, cosa dicono questi numeri.**

Prima di tutto il verso di CAD=X, perché è la fonte di errore più facile: **CAD=X in salita = dollaro canadese che si indebolisce**. Quindi una mediana positiva su CAD=X significa CAD più debole, non più forte.

**Pool completo (A), N=13** — è il profilo di una giornata qualsiasi di titoli sui dazi:
- **CAD=X**: mediana +0,16% a T+1, +0,23% a T+3, poi sostanzialmente piatta. Tradotto: **dollaro canadese lievemente più debole** attorno a un titolo sui dazi. Non sorprende, dato che il pool è dominato da escalation.
- **^GSPTSE (Toronto)**: mediana +0,40% a T+1 e +0,78% a T+5, ma media **negativa** (−0,13% e +0,08%): la divergenza fra media e mediana segnala che pochi episodi molto brutti (2018-10-10, 2025-04-02) trascinano giù la media. Con deviazione standard fino al 3,1%, il segnale è debolissimo.
- **^GSPC**: stesso quadro, mediana +0,54% a T+1 ma media −0,18%, e a T+10 media −0,47%.
- **^VIX**: mediana −0,40% a T+1 e **−14,44% a T+5**, ma media +7,77% a T+3 con deviazione standard del **39,9%**. Questa è la dispersione più alta di tutte le schede di oggi: attorno ai titoli sui dazi la volatilità fa qualsiasi cosa.
- **DX-Y.NYB**: ❌ controproducente in scorecard (IC −0,16, hit-rate 32%): riportato ma non interpretato.

**Sottoinsieme di distensione (B), N=7 — ⚠ INDICATIVE ONLY**, sotto la soglia di N=10:
- **^GSPTSE**: mediana +0,70% a T+1, con **primo quartile positivo** (+0,15%) e deviazione standard di soli 0,47% — di gran lunga il risultato più pulito delle due tabelle. In parole povere: nei sette episodi di sollievo, il giorno dopo Toronto era in guadagno in almeno tre casi su quattro, con dispersione minima.
- **^GSPC**: mediana +0,86% a T+1, primo quartile +0,58%, stesso profilo compatto.
- **^VIX**: mediana **−6,51% a T+1** e **−11,49% a T+10**, con terzo quartile negativo a T+1 (−0,94%): in almeno tre casi su quattro il premio per la paura si è sgonfiato subito. ✅ ^VIX è "affidabile" in scorecard (IC +0,17, hit-rate 63%), ed è quindi la lettura direzionale su cui questa scheda poggia meglio — pur con N=7.
- **CAD=X**: mediana +0,06% a T+1, +0,26% a T+3 — praticamente nulla. Il campione non contiene episodi Canada-specifici, quindi non c'era ragione di aspettarsi altro.

**La sintesi onesta**: la lettura direzionale che questa scheda può sostenere è **una sola e limitata**: dopo una distensione sui dazi il premio per il rischio (^VIX) si sgonfia rapidamente, e l'azionario nordamericano recupera modestamente nella prima seduta. Su tutto il resto — e in particolare sul dollaro canadese, che è l'asset che il briefing indica come il più direttamente coinvolto — **il campione non ha nulla da dire**, perché non contiene episodi canadesi.

**Regime misto — da dichiarare.** Il campione copre due regimi distinti: la guerra commerciale USA-Cina 2018-2019 (dazi come politica strutturale, con tabelle pluriennali) e il regime 2024-2026 (dazi come leva negoziale a scadenza breve). Solo il secondo è confrontabile con oggi, e vi appartengono 5 dei 13 episodi.

---

## Considerazioni qualitative

Questa scheda vale soprattutto per ciò che **non** riesce a dire, e vale la pena spiegare perché.

**Il problema dell'orizzonte.** Una sospensione dei dazi di tre giorni scade il 22 agosto, che è un sabato — quindi il primo giorno di borsa dopo la scadenza è lunedì 24, cioè **T+3** rispetto a oggi. Ne segue che le colonne T+5 e T+10 del nostro event study misurano un mondo in cui la scadenza è già arrivata, e in cui quindi o c'è un accordo firmato o ci sono dazi al 50%. Non c'è modo di distinguere i due scenari con questo strumento. **L'event study, qui, misura in larga parte l'esito di un evento futuro che non conosciamo.** È il motivo della confidence `low`, ed è un limite di disegno, non di campione.

**Il meccanismo, comunque.** Un dazio è un'imposta sull'importazione. Se gli Stati Uniti applicano il 50% su 20 miliardi di dollari di merci canadesi, tre cose accadono in sequenza. Primo: gli importatori americani pagano di più, e o comprimono i margini o alzano i prezzi al consumatore — ecco perché il briefing segnala che "le indicazioni sui costi di input transfrontalieri da parte di distributori e industriali USA hanno ancora una coda viva". Secondo: gli esportatori canadesi perdono volumi, il che colpisce direttamente ferrovie, componentistica auto e le banche che li finanziano — cioè il cuore dell'indice di Toronto. Terzo: il dollaro canadese si indebolisce, sia perché le prospettive di crescita peggiorano sia perché il mercato sconta un possibile allentamento della banca centrale canadese. È per questo che **CAD=X e ^GSPTSE sono gli asset giusti**, anche se il nostro campione storico non li illumina.

**Il nodo auto.** L'ostacolo principale è la soglia minima sui veicoli: Washington a 15%, Ottawa a 10%. Sembra un dettaglio, ma l'industria automobilistica nordamericana è integrata a livello di singolo componente — un'auto attraversa il confine più volte prima di essere finita. Una differenza di cinque punti percentuali applicata a una catena che attraversa il confine ripetutamente si compone, e il costo effettivo è molto maggiore del differenziale nominale. È il motivo per cui questo file è l'ultimo a chiudersi.

**Il rischio giuridico, che è il vero elemento nuovo.** A febbraio la Corte Suprema ha annullato i dazi precedenti. L'amministrazione ha ripiegato sulla Section 338 del Tariff Act del 1930, una norma sostanzialmente inutilizzata in epoca moderna. Questo significa che, anche se i dazi entrassero in vigore sabato, la loro sopravvivenza è incerta. Per un mercato questo è **un rischio a due code**: l'annuncio può essere seguito da un'ingiunzione che lo blocca, oppure da una conferma che lo rende duraturo. Nessuno dei 13 episodi del nostro campione contiene questa dimensione: nel 2018-2019 il fondamento giuridico dei dazi (Section 301, Section 232) non era in discussione.

**Cosa guardare.** Non i prezzi di oggi, ma **venerdì 21 agosto**: se entro la chiusura della settimana i documenti non sono firmati, il fine settimana si apre con un rischio binario aperto e il lunedì può riprezzare in modo brusco. Il pattern del campione (B) — sollievo immediato e volatilità che si sgonfia — descrive ciò che accade quando un rischio viene **rimosso**, non quando viene **rinviato di tre giorni**. La differenza è tutta lì.

---

## Glossario — sigle e termini

- **Dazio (tariff)** — imposta applicata all'importazione di un bene, pagata dall'importatore nel paese di destinazione (non dall'esportatore, contrariamente a come viene spesso descritta).
- **Section 338** — disposizione del Tariff Act statunitense del 1930 che consente al presidente di imporre dazi in risposta a discriminazioni contro il commercio USA. Sostanzialmente inutilizzata in epoca moderna; adottata dopo l'annullamento dei dazi precedenti da parte della Corte Suprema nel febbraio 2026.
- **Section 301 / Section 232** — le basi giuridiche usate nei dazi 2018-2019 (pratiche commerciali sleali e sicurezza nazionale rispettivamente).
- **USMCA** — United States-Mexico-Canada Agreement, l'accordo commerciale nordamericano entrato in vigore nel 2020 in sostituzione del **NAFTA** (North American Free Trade Agreement).
- **CAD=X** — cambio dollaro USA/dollaro canadese: **quanti dollari canadesi per un dollaro USA**. In salita = dollaro canadese più debole.
- **^GSPTSE** — indice S&P/TSX Composite della borsa di Toronto, il principale indice azionario canadese.
- **^GSPC** — indice azionario S&P 500 (USA).
- **^VIX** — indice CBOE della volatilità implicita a 30 giorni sull'S&P 500.
- **DX-Y.NYB** — indice del dollaro USA contro un paniere di sei valute principali.
- **Truth Social** — piattaforma su cui è stato pubblicato l'annuncio; rilevante perché rende l'annuncio verificabile e datato al minuto, il che è ciò che serve per un event study.
- **T+N** — N giorni di **borsa** dopo il giorno dell'evento.
- **INDICATIVE ONLY** — flag automatico che il sistema applica quando N<10: il campione è troppo piccolo per un'inferenza robusta.
- **Information Coefficient (IC)** — correlazione di rango fra previsione e risultato, calcolata dalla scorecard settimanale.

---

## Caveat

1. **Filtro di direzione fallito.** La libreria non contiene **nemmeno un** episodio di dazi etichettato come direzionalmente positivo: il pool (A) è di fatto un insieme di escalation. Usarlo come analogo di una distensione è improprio, ed è il motivo per cui abbiamo aggiunto il sottoinsieme (B) potato a mano.
2. **Il sottoinsieme (B) è INDICATIVE ONLY.** N=7 < 10. Il sistema flagga automaticamente ogni tabella. Nessuna conclusione quantitativa va tratta da lì; al massimo un'indicazione di direzione su ^VIX, che è l'unico asset ✅ affidabile coinvolto.
3. **Nessun episodio Canada-specifico.** Tutti i 13 episodi appartengono al canale USA-Cina. Il campione non dice nulla su CAD=X e ^GSPTSE che non sia riflesso generico del rischio commerciale globale. **Questa è la lacuna di knowledge base annotata in `_index.md`.**
4. **Orizzonte incompatibile con lo strumento.** Una sospensione di tre giorni scade prima di T+5. Le colonne T+5 e T+10 misurano un mondo post-scadenza il cui esito è ignoto. Questo, e non la numerosità, è il limite fondamentale della scheda — da cui la confidence `low`.
5. **Regime misto.** Guerra commerciale strutturale 2018-2019 contro dazi come leva negoziale 2024-2026: solo 5 episodi su 13 appartengono al secondo regime, l'unico confrontabile.
6. **Verso della quotazione.** CAD=X è quotato come dollari canadesi per dollaro USA: in salita = CAD più **debole**. Leggere il segno al contrario è l'errore più facile su questo asset.
7. **Un asset su cui NON traiamo direzione.** Scorecard 2026-W34: **DX-Y.NYB** è ❌ controproducente (IC −0,16, N=156, hit-rate 32%). Riportato solo a fini descrittivi. **^GSPTSE** e **CAD=X** non hanno ancora abbastanza previsioni mature per un giudizio (in database rispettivamente dal 2026-08-18 e dal 2026-08-16).
8. **Rischio giuridico non rappresentato nel campione.** L'incertezza sulla tenuta della Section 338 non ha precedenti negli episodi 2018-2019, dove il fondamento normativo non era contestato.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B), filtro date-locale `tariff_escalation`, direzione `pos` (fallita → mixed, dichiarato), no-look-ahead `--before 2026-08-19`; più sottoinsieme potato a mano
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
