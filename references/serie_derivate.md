# Serie derivate: spread BTP-Bund e OAT-Bund, crack spread

**Quando aprire questo file:** devi aggiornare `BTP_BUND_SPREAD` o `OAT_BUND_SPREAD`, o una
scheda tocca lo spread sovrano italiano/francese o i margini di raffinazione.

Sono le tre eccezioni alla regola "gli indicatori calcolati non si persistono": sono
*serie derivate* salvate come ticker, così l'event study le tratta come ogni altro asset.

## BTP_BUND_SPREAD

- **Cos'è**: Italia 10Y − Germania 10Y, in **punti base**, in `close`/`adj_close`.
  OHLC e volume sono NULL — uno spread di rendimento non ha candele.
- **Cadenza**: **giornaliera** dal 2026-06-04. ~8.800 righe dal 1991-11 a oggi.
  In event study i passi T+N sono **giorni di borsa**, come ogni altro asset:
  `event_study.py` rileva da solo la cadenza giornaliera (nessun warning mensile).
- **Uso**: indicatore primario di **frammentazione/rischio** della periferia eurozona.
- ⚠ **Non descriverlo come "non in DB" / "vuoto" / "mensile" / "placeholder".**
- **Fonte**: Stooq, rendimenti benchmark giornalieri (`10YITY.B`, `10YDEY.B`), via
  `fetch_daily_spread.py` (richiede `STOOQ_API_KEY` in `~/Claude/.env`).
- **Legacy**: `fetch_fred_data.py` (serie FRED **mensili** `IRLTLT01ITM156N` /
  `IRLTLT01DEM156N`) era la fonte precedente — resta solo come fallback, il fetch
  giornaliero Stooq la supera e sovrascrive lo stesso ticker.
- **Refresh**: né FRED né Stooq vengono toccati dall'incrementale giornaliero
  `update_market_data.py`. Va rilanciato `fetch_daily_spread.py` a mano.

### 🟡 Il fetch HTTP è morto — procedura manuale (diagnosi 2026-08-19)

Stooq sta dietro a un **proof-of-work JavaScript**: `urllib` prende un 404 senza
User-Agent e la pagina di verifica con uno. Il download automatico di
`fetch_daily_spread.py` **non può funzionare, a prescindere dalla API key**.

Nessun sostituto giornaliero per singolo paese: Eurostat e BCE danno l'Italia solo
mensile; la curva giornaliera BCE copre l'aggregato AAA, non l'Italia.

Procedura di lavoro (aggiornata il 2026-10-02): **da Chrome il CSV completo si scarica**.
Dentro la pagina `https://stooq.com/q/d/?s=<simbolo>` un `fetch('/q/d/l/?s=<simbolo>&i=d')`
restituisce lo storico intero, ma **solo per il simbolo della pagina aperta** (gli altri
rispondono «Access denied»). Quindi, con l'estensione Chrome:

1. Per ogni simbolo (`10yity.b`, `10ydey.b`, `10yfry.b`) apri la sua pagina, fai il fetch e
   salva il testo in `localStorage` (stessa origine, sopravvive alla navigazione).
2. Porta i tre CSV su disco attraverso gli appunti: `navigator.clipboard.writeText`
   vuole un clic vero, quindi inietta un bottone e cliccalo; poi `pbpaste > file`.
3. Importa: le righe dopo l'ultima data in DB, mai la seduta di oggi ancora aperta.
   ```bash
   V=news_impact_pipeline/venv/bin/python
   $V news_impact_pipeline/import_spread_csv.py IT.csv DE.csv
   $V news_impact_pipeline/import_spread_csv.py FR.csv DE.csv --ticker OAT_BUND_SPREAD
   ```

Prima di importare, confronta lo storico ricalcolato con quello in DB: il 2026-10-02
coincidevano 8.883 giorni su 8.884 (scarto massimo 1 pb). Per pochi giorni letti a mano
resta `fetch_daily_spread.py --pairs YYYY-MM-DD,IT,DE ...`, che vuole una data già in DB come
controllo.

La diagnosi del 2026-08-19 ha chiuso anche la via
Stooq per gilt/JGB/ACGB — da lì i proxy ETF aggiunti il 2026-08-18.

## OAT_BUND_SPREAD

- **Cos'è**: Francia 10Y − Germania 10Y, in **punti base**, come `BTP_BUND_SPREAD`.
  Giornaliero dal 2005-11-28 (inizio di `10YFRY.B` su Stooq). Aggiunto il 2026-10-02.
- **Uso**: rischio fiscale e politico **francese** (cadute di governo, bilanci col 49.3,
  declassamenti). Prima il proxy era `^STOXX50E`, che diluisce la Francia nell'area euro;
  `BTP_BUND_SPREAD` non lo sostituisce, perché il contagio verso l'Italia è ambiguo.
- **Refresh**: stessa procedura manuale del BTP-Bund, qui sopra.

## CRACK_321

- **Cos'è**: margine di raffinazione 3-2-1, in **USD al barile**, in `close`/`adj_close`
  (OHLC/volume NULL, come lo spread BTP). Aggiunto il 2026-08-11.
- **Formula** (`compute_crack_spread.py`): `(2*RB=F + 1*HO=F) * 42 / 3 − BZ=F`
  — il 42 converte i prodotti da $/gallone a $/barile.
- **Refresh**: ricalcolato **ogni giorno** da `update_market_data.py` partendo da
  ticker già in DB. Nessuna fonte esterna, quindi nessun rischio rate-limit o anti-bot.
- **Uso**: **blocchi/attacchi alle raffinerie**. Colpiscono prodotti e margini, non il
  greggio — il Brent da solo può perfino scendere mentre il diesel schizza.
- **Controllo di sanità storico**: mediana ~$9–17 in anni normali, $7 nel 2020
  (crollo domanda COVID), $32 nel 2022 (crisi diesel post-invasione), $43 nel 2026.
- **NB**: accoppia prodotti NYMEX con il **Brent** (non il WTI) di proposito — il
  canale di interesse è europeo/russo.
