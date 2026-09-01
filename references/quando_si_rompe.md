# Quando si rompe

**Quando aprire questo file:** il report giornaliero non è uscito, il database sembra
vuoto, o qualcosa fallisce senza dirlo.

## ⚠ Il guasto silenzioso: login scaduto (401)

**È già successo: dal 25 al 27 giugno 2026 il report non è stato prodotto per tre
giorni, e nessuno se n'è accorto.**

La pipeline girava benissimo — database, analoghi, indice tutti a posto. A fallire era
solo la chiamata `claude -p` headless, con `401 Invalid authentication credentials`.

**Causa:** il token OAuth nel Keychain di macOS (voce `Claude Code-credentials`, account
`riccardo`/`bimbum1227`) era scaduto il 24 giugno, e **nei run launchd headless non si
rinnova da solo.**

**Come si risolve:** Riccardo rifà `claude /login` **dal proprio terminale**.

⚠ **Da dentro una sessione Claude Code il login non si verifica in modo affidabile**:
la sessione ha `ANTHROPIC_BASE_URL` impostato, quindi usa un percorso di autenticazione
diverso da quello di launchd. Può sembrare tutto a posto mentre il job automatico è
fermo.

**Protezioni già applicate a `run_daily_analysis.sh`:**
1. Se l'uscita è diversa da zero o manca `_index.md` → riga `ERROR` nel log **e notifica
   sul desktop** (riconosce il 401 e dice di rifare il login). Basta col guasto muto che
   dura giorni.
2. Accetta una **data come primo argomento** (`TODAY=${1:-$(date +%Y-%m-%d)}`) per
   recuperare a mano i giorni saltati.

**Se ricapita spesso**, l'opzione strutturale è una API key dedicata passata via
variabile d'ambiente nel plist: più stabile di OAuth per l'automazione.

## Certificati SSL su Mac

Python 3.12 installato da python.org richiede di lanciare **una volta**:

```
/Applications/Python 3.12/Install Certificates.command
```

Senza, la verifica dei certificati fallisce e **tutte** le chiamate HTTPS si bloccano,
FRED compreso.

## Ricostruire il database dei prezzi

⚠ **`market_data.db` non ha backup** ed è già stato azzerato una volta (29 maggio 2026,
durante una riorganizzazione di file: sovrascritto con un file vuoto da 0 byte).

Non è un dramma: è un artefatto **rigenerabile**, non una fonte primaria. Perderlo costa
tempo di ri-scaricamento, non dati irrecuperabili.

**Come accorgersene:** il file è a 0 byte, oppure mancano le tabelle `assets` e `prices`.

**Procedura:**

```bash
V=news_impact_pipeline/venv/bin/python

# 1. carico storico completo (~15 anni, tutti gli asset di ASSETS via yfinance)
$V news_impact_pipeline/bootstrap_market_data.py

# 2. verifica
sqlite3 market_data/market_data.db "SELECT COUNT(*) FROM assets;"
```

⚠ **Le due serie derivate non tornano da sole:**
- `CRACK_321` si ricalcola al primo `update_market_data.py`, perché parte da ticker già
  in DB. Nessun problema.
- `BTP_BUND_SPREAD` **va ricostruito a mano**: il download automatico da Stooq non
  funziona più. Procedura in [serie_derivate.md](serie_derivate.md).

⚠ **Non usare `fetch_fred_data.py`** per ricostruire lo spread: è la fonte **legacy** e
darebbe una serie **mensile** al posto di quella giornaliera, senza segnalarlo.

**Protezione mai implementata** (resta una buona idea): un dump CSV periodico, o una
copia `.db.bak` **fuori** dalla cartella di lavoro, così uno spostamento di file non
può azzerarla.

## La regola che vale per tutti e tre

Ogni volta che si sposta o riorganizza qualcosa in `~/Claude`, il database va verificato
**prima e dopo**, esplicitamente. Mai un `mv` "a occhio": è così che è sparito la prima
volta. Nel trasloco del 29 luglio la verifica è stata fatta (md5 invariato) ed è andata
bene.
