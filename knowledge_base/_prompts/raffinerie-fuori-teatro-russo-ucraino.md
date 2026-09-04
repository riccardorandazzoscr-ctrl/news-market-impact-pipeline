# Prompt di deep research — Attacchi alle infrastrutture di raffinazione fuori dal teatro russo-ucraino

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** «Attacchi a infrastrutture di raffinazione fuori dal teatro russo-ucraino. La knowledge base ha una research dedicata alle raffinerie russe (2022–2026) e una su Hormuz, ma non copre il caso mediorientale/iracheno — Al-Doura di oggi non trova un regime di riferimento. […] gli episodi disponibili con etichetta `refinery_strike` (17 date-locali) sono quasi tutti ucraini contro raffinerie russe, un contesto di sanzioni e capacità sostituibile molto diverso da un impianto irakeno che serve il mercato domestico.» (2026-09-01, lacuna 1)
- **Segnalata il:** 2026-02-27 (prima occorrenza, testo non più in retention — la cartella `daily_analysis/2026-02-27/` non esiste più) e 2026-09-01 (seconda occorrenza esplicita, sull'incendio al complesso di Al-Doura a Baghdad). **Ricorrenza: 2.**
- **Tema canonico di destinazione:** `commodity_energy`
- **Asset in DB che lo studio deve poter servire:** `CRACK_321` (margine di raffinazione — il canale primario), `HO=F` (diesel/gasolio — prodotto più esposto), `RB=F` (benzina RBOB), `BZ=F` (Brent — per separare l'effetto "raffinazione" dall'effetto "greggio"), `GC=F` (oro, controllo regime inflazionistico), `XLE` (energia azionaria USA), `^GSPC`, `INDA` (India, importatore netto molto esposto a shock sui prodotti raffinati), `EURUSD=X`
- **Asset citabili ma NON in DB:** crack spread diesel-Brent singolo (isolerebbe la componente diesel, oggi solo il crack 3-2-1 aggregato è in DB — stesso limite già dichiarato nello studio russo-ucraino); differenziale Dubai/Oman-Brent (misurerebbe lo sconto del greggio mediorientale in caso di interruzione locale della raffinazione); indice di utilizzo della capacità di raffinazione OPEC/JODI per la regione, se disponibile con frequenza utile.
- **Perché serve la research e non basta la tassonomia:** `analogues.py labels --theme commodity_energy` (misurato il 2026-09-02) dà `refinery_strike` con **17 episodi date-locali** — sopra soglia, quindi il pool *si forma*, ma proviene quasi interamente dallo studio dedicato «Attacchi alle raffinerie e alla capacità di raffinazione russa (guerra Russia-Ucraina)» (`knowledge_base/Attacchi alle raffinerie…/`). Non è un problema di soglia come nel caso del vincolo elettrico AI: qui il **token esiste e il pool si popola**, ma il regime che descrive (sanzioni occidentali, capacità russa parzialmente sostituibile da import, guerra convenzionale fra stati) non è l'analogo giusto per un attacco a un impianto che rifornisce il mercato interno di un paese terzo, spesso ad opera di attori non statali o in contesti di guerra civile/insurrezione. Serve una libreria di episodi separata per isolare il regime giusto quando la notizia del giorno non è russo-ucraina.

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**,
in Markdown, su:

**Attacchi alle infrastrutture di raffinazione fuori dal teatro russo-ucraino: Medio Oriente e altri teatri — regime ed episodi storici (2012–presente)**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia
odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset
a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**,
  non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

### La domanda a cui lo studio deve rispondere

**In che modo un attacco alla capacità di raffinazione muove i prezzi quando il contesto NON è la guerra russo-ucraina — e quanto questo dipende dal fatto che l'impianto colpito rifornisce il mercato domestico invece di alimentare un flusso di export sanzionabile?** Lo studio esistente sulla Russia (in KB, non riprodurlo) tratta un caso specifico: un esportatore di prodotti raffinati sotto embargo occidentale, dove il danno riduce l'offerta *export* mentre il paese colpito può in parte compensare con import o riallocazione. Il caso mediorientale/iracheno è diverso per costruzione: un impianto come Al-Doura (Baghdad) o le raffinerie irachene colpite durante la campagna contro l'ISIS (Baiji, 2014-2015) riforniscono la **domanda interna**, spesso in un paese che è anche esportatore netto di greggio grezzo — quindi il danno può produrre carenza di prodotto raffinato e code alla pompa **senza muovere il Brent**, l'opposto della logica "meno raffinazione = più export di greggio grezzo compensativo" che si osserva altrove. Isola questa distinzione come oggetto centrale: il canale non è uniforme, dipende dal ruolo del paese colpito nella catena (esportatore di greggio vs importatore di prodotto, capacità sostituibile vs no).

Copri almeno questi teatri, escludendo esplicitamente la guerra russo-ucraina (già coperta altrove) e trattando ciascuno come sotto-caso con la propria nota su chi sia l'attore (stato, milizia, gruppo non statale) e su cosa distingua il regime:
- **Attacchi Houthi contro impianti Saudi Aramco** (Abqaiq/Khurais 14 settembre 2019 — il caso meglio documentato e di gran lunga il più grande per impatto istantaneo sul Brent; Jeddah, Ras Tanura, Yanbu e altri tentativi 2020-2022);
- **Iraq**: campagna ISIS contro la raffineria di Baiji (2014-2015) e attacchi/incidenti più recenti su impianti che riforniscono il mercato interno, incluso il complesso di Al-Doura a Baghdad;
- **Libia**: blocchi e attacchi a impianti e terminal petroliferi durante la guerra civile e le dispute fra governi rivali (2013-2020), come caso di interruzione prolungata per motivi politico-istituzionali più che militari;
- **Nigeria**: sabotaggi/vandalismo di oleodotti e incendi di raffinerie nel Delta del Niger, come caso di attore non statale endemico (non un singolo shock ma una serie ricorrente);
- qualunque altro episodio verificabile (Yemen, Venezuela, Messico) purché sia un **attacco o un'interruzione discreta e datata**, non un declino strutturale della capacità.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente
**dove l'event study è affidabile e dove non lo è** su questo tema, e in particolare
se e come il canale si distingue da quello russo-ucraino già in libreria.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale. Ogni canale
in forma di **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`)
e con l'indicazione degli asset-proxy da usare fra questi: `CRACK_321`, `HO=F`, `RB=F`,
`BZ=F`, `GC=F`, `XLE`, `^GSPC`, `INDA`, `EURUSD=X`. Distingui esplicitamente:
- il canale **export-compensabile** (danno alla raffinazione che il paese colpito compensa esportando più greggio grezzo invece di prodotto — muove il crack, non necessariamente il Brent) dal canale **domanda-interna-scoperta** (il paese colpito è anche importatore netto di prodotto, o non ha capacità di export alternativa — muove entrambi, o crea razionamento locale senza effetto misurabile sui benchmark globali);
- il canale **stato-contro-stato** (Houthi/Arabia Saudita, come proxy di un conflitto Iran-Golfo) dal canale **attore non statale endemico** (Nigeria, insurrezione ISIS in Iraq), perché il primo porta premio di rischio geopolitico più ampio (contagio ad altri impianti del Golfo), il secondo tende a restare localizzato;
- eventuali episodi in cui l'attacco ha innescato un **premio di rischio anticipatorio** sull'intera regione del Golfo (contagio Abqaiq→altri impianti sauditi) distinti da quelli rimasti puramente locali.

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Una tabella con
colonne: `Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead`.

La colonna "Direzione attesa" va in forma **canonica** (`pos`/`neg`/`neutral`),
riferita esplicitamente a **ciascun** asset-canale quando il verso diverge fra loro
(es. `CRACK_321: pos / BZ=F: neutral`) — non una prosa libera.

Requisiti sulle date, **critici**:
- almeno **15-25** episodi;
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non
  quella dell'attacco: se la notizia esce a mercato chiuso o in un festivo,
  usa la prima seduta utile del proxy e **spiegalo nella colonna Note**;
- se una data è incerta fra due fonti (frequente per attacchi in zone di guerra,
  dove il danno reale è spesso oscurato o gonfiato dalle parti), riportale entrambe
  e dichiaralo — vale lo stesso standard di verifica adottato nello studio russo-ucraino
  (annuncio iniziale vs conferma di danno strutturale);
- **una data che NON deve diventare un episodio** (inizio di una campagna, stima di
  capacità disabilitata cumulata) va scritta in forma **non-ISO** ("dal 2014",
  "campagna 2019-2022") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

**§4 Statistiche indicative.** Cosa è successo mediamente a `CRACK_321`, `HO=F`,
`RB=F` e `BZ=F` dopo gli episodi del §3, separando **per canale** (export-compensabile
vs domanda-interna-scoperta) e **per teatro**. Riporta **sempre N** accanto a ogni
statistica; marca "INDICATIVE ONLY" ogni statistica con N < 10 — probabile per
alcuni sotto-teatri (es. Nigeria, Libia) dove il campione sarà piccolo.

**§5 Fasi di regime.** 2-5 fasi con confini datati (es. `pre_abqaiq`, `post_abqaiq_gulf_premium`,
`isis_iraq_campaign`, `post_2022_multipolar_disruption` se utile a distinguere il periodo
in cui più teatri sono diventati attivi contemporaneamente), ciascuna con: cosa cambia
strutturalmente e **se gli analoghi di quella fase siano usabili nel regime corrente**
(in particolare: quanto lo shock Hormuz/Iran del 2026, già coperto da uno studio
dedicato in KB, renda il Golfo un contesto diverso da prima del 2019). Nomi delle
fasi in `snake_case` inglese.

**§6 Caveat metodologici.** Come minimo: l'attendibilità delle fonti in zone di
conflitto attivo (governi e milizie hanno incentivo a minimizzare o gonfiare il
danno, analogamente al caso russo già documentato in KB); la difficoltà di isolare
un attacco alla raffinazione da uno shock upstream concomitante (produzione di
greggio, chiusura di un giacimento) nello stesso teatro; la sovrapposizione con lo
studio Hormuz/Iran già in KB quando l'episodio riguarda il Golfo — dichiara
esplicitamente dove i due studi si sovrappongono e quale usare per un canale
ambiguo; N strutturalmente piccolo per singolo teatro; fonti e incertezze residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo
formato esatto:

    ---
    title: "<titolo completo>"
    date_compiled: <YYYY-MM-DD>
    primary_theme: commodity_energy
    sub_themes: [refinery_strike, infrastructure_attack, non_state_actor_attack, domestic_supply_disruption]
    relevant_assets: [CRACK_321, HO=F, RB=F, BZ=F, GC=F, XLE, ^GSPC, INDA, EURUSD=X]
    external_assets_mentioned:
      - "crack spread diesel-Brent singolo — isolerebbe la componente diesel, oggi solo il crack 3-2-1 aggregato è in DB"
      - "differenziale Dubai/Oman-Brent — misurerebbe lo sconto del greggio mediorientale in caso di interruzione locale"
    time_window:
      start: 2012-01-01
      end: present
    regime_phases:
      - <nome_fase>: <YYYY-MM-DD> to <YYYY-MM-DD|present>
    keywords: [raffineria, refinery attack, Abqaiq, Khurais, Houthi, Aramco, Baiji, Iraq, Al-Doura, Libia, Nigeria Delta del Niger, sabotaggio, drone strike, insurgency, crack spread, margine di raffinazione]

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/<Titolo>/<Titolo>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] valutare se `refinery_strike` da solo basta a distinguere il pool dal caso russo-ucraino, o se serve un token che isoli il teatro (es. `non_state_actor_attack` vs `state_conflict_attack`) — oggi la libreria non lo distingue
- [ ] `venv/bin/python analogues.py labels --theme commodity_energy` → la copertura di `refinery_strike` è cambiata (più episodi, più varietà geografica)?
- [ ] `venv/bin/python pipeline_tools.py match "<notizia tipo: attacco a raffineria in Iraq/Golfo/Nigeria>"` → esce questo studio e non (solo) quello russo-ucraino
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
