# Leggere la scorecard senza ingannarsi

**Quando aprire questo file:** stai leggendo o interpretando la scorecard settimanale, o
stai per scrivere la lettura direzionale di una scheda.

Tre cose scoperte il 2026-08-10, tutte già applicate nel codice. Qui c'è il **perché**,
che nel codice non si legge.

## 1. L'edge è spaccato per ASSET, non per tema

L'IC aggregato basso (~+0,07) **non significava "il sistema prevede poco"**: nascondeva
due popolazioni opposte. Analisi per-asset sul ledger (N=2.345), **stabile su entrambe le
metà del campione**:

**✅ Affidabili — rischio/equity**

| asset | IC | hit rate |
|---|---|---|
| `^VIX` | +0,27 | 63% |
| `EEM` | +0,17 | 62% |
| `^NDX` | +0,16 | |
| `^STOXX50E` | +0,16 | 58% |
| `^GSPC` | +0,09 (stabile +0,09→+0,08) | |

**❌ Controproducenti — rifugio/tassi/dollaro**

| asset | IC | nota |
|---|---|---|
| `IEF` | **−0,33** | |
| `^TNX` | −0,20 | instabile (−0,26→+0,06): rumoroso |
| `DX-Y.NYB` | −0,11 | **hit rate 31% = 3,4 sigma SOTTO il caso**, stabile |
| `GC=F` | −0,09 | in peggioramento (−0,00→−0,22) |
| `SOXX` | −0,06 | |

**Lettura:** la grammatica narrativa del "bene rifugio" è **sistematicamente rovesciata**
nel regime attuale, fatto di shock inflattivi e da offerta, non da crescita.

**Come si usa, in pratica:** prima di scrivere la lettura direzionale, leggi la sezione
**"5-bis. Su quali ASSET prevediamo meglio?"** della scorecard corrente. Sugli asset
marcati ❌, **dichiara inaffidabile il segno storico invece di prevederci sopra**.

⚠ **Sempre con rimando alla scorecard viva, mai a una lista fissa** copiata qui o
altrove. È la lezione del bug "17 asset": una lista trascritta invecchia e mente. La
tabella qui sopra è la fotografia del 10 agosto, serve a capire *il fenomeno* — non a
decidere su quale asset fidarsi oggi.

Meccanismo: `forecast_tracking.py`, soglia `ASSET_MIN_N=50`, giudizio ✅/⚠️/❌.

## 2. L'IC va calcolato DENTRO ciascun asset, non tutto insieme

Il calcolo "pooled" — tutte le righe insieme, asset, orizzonti e date mescolati —
**sovrastimava di circa 3 volte**. Premiava il fatto ovvio che `^VIX` si muove più di
`EURUSD=X`, non l'abilità di prevedere.

`_ic_within_assets()` in `forecast_tracking.py` calcola l'IC dentro ciascun asset
(soglia `IC_ASSET_MIN_N=15`), poi fa la media pesata per N. È il numero **ufficiale**;
il pooled resta come colonna in corsivo, per trasparenza.

**Effetto sulla settimana 33:** overall da +0,07 a **+0,02**. E soprattutto **T+10 crolla
da +0,13 a +0,03**.

⚠ **Conseguenza da non dimenticare:** l'idea che "l'orizzonte lungo fosse il migliore"
era in gran parte un **artefatto di scala, non edge**. Ogni conclusione passata basata
sull'IC alto a T+10 va rivista.

Per-orizzonte, onesto: T+1 +0,03 · T+3 −0,01 · T+5 −0,04 · T+10 +0,03.

## 3. C'è un effetto di selezione, e va tenuto presente

I rendimenti realizzati sono positivi solo nel **45% dei casi** (mediana −0,13%, che
peggiora a −0,37% a T+10).

Su oro e petrolio il nostro campione fa **molto peggio del mercato incondizionato**:

| | nostro campione | mercato normale |
|---|---|---|
| oro | −3,55% | −1,02% |
| Brent | −10,56% | −5,54% |

Il motivo: **scriviamo schede nei momenti drammatici**, che tendono a coincidere con
estremi locali.

⚠ Correggerlo sembra ovvio ma **non funziona**: è stato provato e misurato, vedi
[esperimenti_scartati.md](esperimenti_scartati.md).

## Il bug che aveva causato tutto

Il dollaro era previsto in rialzo nel 73% dei casi ma saliva davvero solo nel 27%. Su
`monetary_policy`: **previsto su 22 volte su 22 (100%), realizzato su 14%**.

Causa: `cmd_build` collassava le direzioni multiple di uno stesso (data, tema) in
**"mixed"**, distruggendo l'informazione — in `monetary_policy` 61 episodi su 102 erano
"mixed" e solo **5** restavano "pos". Combinato col vecchio filtro che lasciava passare
"mixed" sempre, ogni scheda monetaria pescava **lo stesso identico pool** a prescindere
da dovish o hawkish. Il segnale d'allarme: tre schede diverse, due delle quali dovish,
avevano mediane **identiche al centesimo**.

Corretto: `cmd_build` conserva `directions` come lista; `cmd_find` accetta l'episodio se
la direzione richiesta è fra quelle osservate — un giorno con notizia sia hawkish sia
dovish è analogo legittimo per entrambe.

Effetto: `monetary_policy` da pos=5/neg=17 a **pos=50/neg=78**, e la previsione sul
dollaro a T+10 da **+0,66% (segno sbagliato) a −0,20%/−0,05% (segno corretto)**.

## Cosa era già stato validato

**Il tetto di recency (`--max-pool 30`) e l'Opzione B funzionano**, verificato a
posteriori sul ledger. Copertura per ampiezza del pool, monotòna crescente:
34% (N<10) → 49% (10-19) → 47% (20-29) → **56% (30+)**.

Hit rate e IC hanno una forma a U e i bucket sono confusi col periodo (N<10 sono in
gran parte vecchie schede dell'Opzione A scelte a mano), ma il bucket **30+ è il migliore
su tutte e tre le metriche**.
