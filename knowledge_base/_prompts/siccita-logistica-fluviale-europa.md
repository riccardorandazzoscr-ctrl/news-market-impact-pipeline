# Prompt di deep research — Siccità, logistica fluviale e vincoli idrici all'energia in Europa

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** «Nessuna research copre siccità, logistica fluviale europea (Reno/Danubio/Po/Loira) e vincoli idrici alla generazione elettrica — un canale di offerta ricorrente ogni estate dal 2018, oggi al minimo storico dal 1880.»
- **Segnalata il:** 2026-08-17 (prima segnalazione); ricorrente il 2026-08-18 (Reno a Kaub a 16-17 cm, minimo assoluto della serie dal 1880; previste letture a una cifra entro meta settimana, disruption possibile fino a ottobre — priorita in aumento)
- **Tema canonico di destinazione:** commodity_energy
- **Asset in DB che lo studio deve poter servire:** TTF=F, EXH9.DE, ^GDAXI, ^STOXX50E, EURUSD=X, HO=F, RB=F, BZ=F, CRACK_321, IEAG.AS
- **Asset citabili ma NON in DB:** noli fluviali Rotterdam-Kaub (Argus/Platts), prezzi spot elettricità EPEX SPOT DE/FR, livelli idrometrici Kaub/Emmerich (WSV), indici settoriali chimica europea (es. STOXX Europe 600 Chemicals), API2 carbone ARA, EUA (permessi CO2 EU ETS)
- **Perché serve la research e non basta la tassonomia:** `analogues.py labels --theme commodity_energy` restituisce solo 4 episodi date-locali su `gas_europe` e 4 su `supply_disruption`; forzando il filtro con `--min-n 5` si arriva a 13 episodi, **nessuno dei quali è una siccità**. Il pool disponibile è dominato da Iran/Hormuz e Russia-Ucraina: shock energetici di origine politica, non climatica, e discreti anziché graduali. Il canale è quindi strutturalmente invisibile alla pipeline.

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**, in Markdown, su:

**Siccità europee, logistica fluviale e vincoli idrici alla generazione elettrica: regime ed episodi storici (2003–2026)**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**, non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

Un vincolo specifico e centrale per questo tema: **la siccità è un processo continuo, non un evento discreto**. Lo studio deve affrontare esplicitamente il problema di come si costruisce una "data-ancora" per un fenomeno graduale — per esempio la prima seduta dopo il superamento di una soglia idrometrica critica, l'annuncio di un sovrapprezzo da parte di un vettore, la comunicazione di una riduzione di potenza da parte di un operatore elettrico, o la pubblicazione di un bollettino ufficiale di allerta. Se la conclusione è che per alcuni canali l'event study **non è lo strumento giusto**, dillo in §1.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente **dove l'event study è affidabile e dove non lo è** su questo tema, con particolare attenzione al problema della gradualità.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale, in forma di **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`), con gli asset-proxy da usare fra: TTF=F, EXH9.DE, ^GDAXI, ^STOXX50E, EURUSD=X, HO=F, RB=F, BZ=F, CRACK_321, IEAG.AS. I canali da coprire come minimo:

1. **Logistica fluviale**: pescaggio insufficiente → chiatte a carico ridotto → noli in aumento e razionamento fisico → costo di consegna di prodotti petroliferi, carbone e chimici a monte del fiume → margini industriali tedeschi e prezzo consegnato dei carburanti.
2. **Generazione idroelettrica**: portate basse → minore produzione idro (rilevante per Italia, Francia, Norvegia, Alpi) → domanda residua servita da gas → prezzo TTF ed elettricità.
3. **Raffreddamento termico/nucleare**: portate basse e temperature d'acqua alte → limiti ambientali sugli scarichi termici → derating di centrali nucleari e termoelettriche (il caso francese dell'estate 2022 e quello ungherese di Paks nel 2026) → prezzo elettricità e utility.
4. **Agricoltura e prezzi alimentari** → componente alimentare dell'indice armonizzato dei prezzi al consumo dell'area euro.
5. **Trasmissione macro**: shock di offerta → inflazione e produzione che si muovono in direzioni opposte → dilemma della banca centrale → tassi e cambio.

Distingui i canali *direzionali* da quelli *redistributivi* (che muovono due asset in direzioni opposte — per esempio le utility con generazione propria guadagnano dai prezzi alti mentre gli industriali energivori perdono) e dagli *amplificatori*.

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Tabella con colonne: `Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead`.

Copertura minima richiesta: le estati di **2003, 2011, 2015, 2018, 2020, 2022, 2023, 2025 e 2026** per il Reno; il derating nucleare francese dell'estate 2022 e dell'estate 2018; le magre del Po del 2003, 2017 e 2022; la siccità iberica 2017-2018 e 2022-2023; le magre del Danubio del 2003, 2018 e 2022; la crisi del Canale di Panama del 2023-2024 come **controllo esterno** (stessa meccanica di chokepoint idrico, mercato diverso).

Requisiti sulle date, **critici**:
- almeno **20** episodi;
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non quella dell'annuncio: se la notizia esce a mercato chiuso o in un festivo, usa la prima seduta utile e **spiegalo nella colonna Note**;
- per questo tema in particolare, dichiara nella colonna Note **quale criterio** ha generato la data-ancora (soglia idrometrica, annuncio di sovrapprezzo, comunicato di derating, bollettino ufficiale);
- se una data è incerta fra due fonti, riportale entrambe e dichiaralo;
- **una data che NON deve diventare un episodio** (picco di una serie, inizio di una fase, riferimento generico) va scritta in forma **non-ISO** ("estate 2018", "primavera 2022") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

**§4 Statistiche indicative.** Cosa è successo mediamente agli asset dopo gli episodi del §3, per canale. Riporta **sempre N**; marca "INDICATIVE ONLY" ogni statistica con N < 10. Includi, se possibile, la stima dell'impatto macro (i circa 0,3 punti percentuali di PIL tedesco attribuiti da ING alla siccità del 2018 sono il riferimento più citato: verificalo e confrontalo con altre stime).

**§5 Fasi di regime.** 2-5 fasi con confini datati, nomi in `snake_case` inglese. Come minimo va distinta la fase **pre-2022** (energia europea abbondante e a buon mercato, siccità come evento eccezionale) dalla fase **post-invasione russa** (sistema energetico teso, capacità di rigassificazione del gas naturale liquefatto costruita d'urgenza, siccità come rischio stagionale ricorrente). Per ciascuna fase dichiara **se gli analoghi siano usabili nel regime corrente**.

**§6 Caveat metodologici.** Come minimo: la gradualità del fenomeno e il problema della data-ancora; la stagionalità (le magre cadono quasi tutte in luglio-settembre, quindi il campione ha un *drift* stagionale sistematico su gas ed elettricità che va isolato); episodi multi-causa (l'estate 2022 mescola siccità, guerra e crisi del gas — indicare quale asset usare come controllo); la sostituzione parziale su gomma e rotaia che attenua l'effetto; il fatto che il danno si materializzi nelle trimestrali e nei dati macro autunnali, fuori dalla finestra 1-10 giorni; serie citate ma non disponibili nel nostro universo; fonti e incertezze residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo formato esatto:

    ---
    title: "<titolo completo>"
    date_compiled: <YYYY-MM-DD>
    primary_theme: commodity_energy
    sub_themes: [<snake_case, minuscolo>]
    relevant_assets: [<solo ticker della lista asset in DB>]
    external_assets_mentioned:
      - "<ticker o serie citata ma NON disponibile — con il motivo per cui conterebbe>"
    time_window:
      start: <YYYY-MM-DD>
      end: present
    regime_phases:
      - <nome_fase>: <YYYY-MM-DD> to <YYYY-MM-DD|present>
    keywords: [<termini italiani E inglesi con cui una notizia potrebbe pescare questo studio>]

Nelle `keywords` includi almeno: siccità, drought, reno, rhine, kaub, danubio, danube, po, loira, loire, low water, pescaggio, chiatte, barge, freight, noli, idroelettrico, hydropower, derating, raffreddamento, cooling water, nucleare francese, french nuclear, paks, ttf, elettricità, power prices, shock di offerta, supply shock, chimica tedesca, german chemicals, copernicus.

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/<Titolo>/<Titolo>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py labels --theme commodity_energy` → `gas_europe` e i nuovi token hanno copertura?
- [ ] aggiungere i token nuovi (es. `hydrology_supply`, `river_logistics`, `nuclear_derating`) a `subtheme_taxonomy.yaml` se assenti
- [ ] `venv/bin/python pipeline_tools.py match --theme commodity_energy --keyword drought --keyword rhine` → lo studio esce primo
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
