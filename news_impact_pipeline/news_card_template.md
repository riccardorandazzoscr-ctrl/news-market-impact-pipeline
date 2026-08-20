# {{TITLE}}

**Data analisi**: {{DATE}}
**Fonte**: {{SOURCE}}
**Slug**: {{SLUG}}

---

## Testo notizia (originale)

> {{NEWS_TEXT}}

---

## In breve (in parole semplici)

<!-- 2-4 frasi PRIMA del gergo: cos'è successo, perché conta per i mercati, e quale
     domanda ci poniamo. Niente sigle non spiegate qui. Pensa a un lettore sveglio ma
     non specialista. Es: "La banca centrale europea sta per alzare il costo del
     denaro mentre l'economia rallenta: una mossa rischiosa. Ci chiediamo come hanno
     reagito i mercati in situazioni simili del passato." -->

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | {{PRIMARY_THEME}} |
| `sub_themes` | {{SUB_THEMES}} |
| `sentiment` | {{SENTIMENT}} <!-- hawkish/dovish, bullish/bearish, risk-on/risk-off, neutral --> |
| `confidence` | {{CONFIDENCE}} <!-- low / medium / high --> |
| `horizon` | {{HORIZON}} <!-- da category_asset_map.yaml --> |

**Motivazione classificazione**: <!-- 1-3 frasi: perché questo theme, sentiment e confidence. -->

---

## Asset rilevanti

### Primary (canale diretto)
<!-- da `pipeline_tools.py assets <theme> --level primary`, poi filtra/aggiungi -->
- TICKER1 — motivo
- TICKER2 — motivo

### Secondary (effetti indiretti)
- TICKER3 — motivo
- TICKER4 — motivo

---

## Knowledge Base — research correlate

<!-- da `pipeline_tools.py match --theme X --keyword ... --asset ...` -->

- [score=NN] `nome_file.md` — Titolo della research
  - Perché è rilevante: <!-- 1 frase. -->

---

## Regime storico identificato

<!-- Quale `regime_phase` della research correlata mappa il momento attuale?
     Citare la fase (es. "post_brexit / reset_starmer"). Se nessuna research
     correlata, descrivere il regime in base alla conoscenza generale. -->

- Regime: <!-- nome fase + range date -->
- Caratterizzazione: <!-- 2-3 righe sul perché siamo in questo regime. -->

---

## Event study

### Episodi storici analoghi selezionati

<!-- L'analista (Claude o utente) propone gli episodi confrontabili in base a:
     theme + sub-theme, regime macro, sentiment direzionale.
     Giustificare brevemente per ciascuno PERCHÉ è analogo.
     Ricordare il vincolo no-look-ahead bias (§7 Design Doc):
     usare solo info disponibile alla data dell'episodio. -->

**Blocco dichiarato** (obbligatorio dal 2026-08-19). La libreria legge QUESTA tabella:
i campi qui sono presi come sono, senza che `analogues.py` debba dedurli dalla prosa.
È la correzione a monte del difetto che generava una lacuna quasi ogni giorno.

- `Verso`: `pos` / `neg` / `neutral` — il verso **di quell'episodio**, non della notizia
  di oggi. Se la giornata storica fu genuinamente ambivalente, scrivi `pos, neg`.
- `Meccanismo`: uno o più token canonici di `subtheme_taxonomy.yaml`, separati da virgola.
  Verifica la copertura con `analogues.py labels --theme <t>` prima di sceglierli.
- Righe con verso non riconoscibile vengono ignorate (si ricade sull'euristica), quindi
  una tabella malformata degrada senza rompere nulla.

| Data | Verso | Meccanismo | Descrizione |
|---|---|---|---|
| `YYYY-MM-DD` | neg | token_canonico | evento in una riga — perché è analogo |
| `YYYY-MM-DD` | pos | token_a, token_b | ... |

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'TICKER1,TICKER2' \
  --events YYYY-MM-DD,YYYY-MM-DD,... \
  --windows 1,3,5,10 \
  --markdown
```

### Risultati

<!-- Incolla qui l'output --markdown di event_study.py.
     Il sistema flagga automaticamente "INDICATIVE ONLY" se N<10. -->

_Incolla qui le tabelle generate._

---

## Considerazioni qualitative

<!-- Sintesi narrativa: cosa ci dice questa notizia letta attraverso la lente
     della research correlata e del regime corrente. Tono DIDATTICO e accessibile:
     spiega i meccanismi causali (non solo gli esiti), espandi le sigle, interpreta
     i numeri dell'event study a parole (cfr. runbook §"Stile e chiarezza"). Nessun
     cap di lunghezza: la chiarezza viene prima della brevità. Materia prima per
     post LinkedIn. -->

---

## Glossario — sigle e termini

<!-- Elenca QUI ogni sigla/termine tecnico usato nella scheda, con spiegazione di
     una riga. Includi dati macro (CPI, NFP, PCE, ISM, PMI, GDP/PIL, HICP, JOLTS),
     strumenti di policy (TPI, OMT, PEPP, QT, forward guidance) e i ticker citati
     (es. ^TNX = Treasury USA 10Y; BTP_BUND_SPREAD = spread BTP-Bund). Ometti la
     sezione solo se la scheda non contiene NESSuna sigla. -->

- **SIGLA** — spiegazione in una riga.

---

## Caveat

<!-- Quali limiti metodologici applicare alla lettura di questa scheda.
     Ricordare: correlation ≠ causation; regime-dependence; campione limitato;
     se l'event study (quando ci sarà) è basato su N piccolo, flaggarlo qui. -->

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / build_catalog.py (project news_impact_pipeline)
- Catalog timestamp: {{CATALOG_TIMESTAMP}}
