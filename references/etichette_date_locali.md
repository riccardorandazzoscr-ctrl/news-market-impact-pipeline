# Etichette date-locali: i quattro livelli e i difetti corretti

**Quando aprire questo file:** stai aggiungendo un'etichetta canonica, calibrando un
pattern in `analogues.py`, o un pool di episodi restituisce risultati che non tornano.

Il problema di fondo: una scheda cita **una data** ma ne contiene **molte**. Attribuire
sotto-tema, geografia e verso alla data giusta è ciò che rende utile la libreria episodi.

Comandi di riferimento:
```bash
news_impact_pipeline/venv/bin/python news_impact_pipeline/analogues.py stats
news_impact_pipeline/venv/bin/python news_impact_pipeline/analogues.py labels --theme <t>
```

## I quattro livelli del VERSO, dal più debole al più forte

1. **`sentiment` della scheda** — il verso unico della scheda, stampato su *ogni* data
   citata. Solo fallback.
2. **`directions_local`** (dal 2026-08-19) — dedotto dal testo attorno a quella data
   specifica; vocabolario in `DIRECTION_PATTERNS` dentro `analogues.py`.
3. **`subthemes_local`** (dal 2026-08-15) — l'equivalente per i sotto-temi, confrontato
   con la tassonomia canonica in `subtheme_taxonomy.yaml`. `find --subtheme` li
   preferisce ai `subthemes` a livello di documento, che restano come recall di riserva.
4. **`directions_declared`** (dal 2026-08-29) — **il più forte**: i versi scritti a mano
   nella colonna "Verso" del blocco episodi. Nessuna euristica può contaminarli.

`find --direction` preferisce il verso date-locale e **dichiara in stderr** quando
degrada a livello di scheda.

### Perché è servito il quarto livello

Prima dichiarazione ed euristica finivano nello **stesso insieme**. Bastava che una
seconda scheda citasse l'episodio solo in prosa perché la regex gli appiccicasse il
verso opposto.

Misurati **171 episodi su 984 con `pos` e `neg` insieme**, di cui **152 dichiarati**,
tutti citati da più schede (fino a 24).

È la causa comune di errori finora trattati come problemi di vocabolario — imporre vs
revocare una sanzione (20/08), `hormuz` escalation vs de-escalation (29/08). ⚠ **Non
erano token da calibrare: allargare il vocabolario non li avrebbe risolti.**

Il livello dichiarato **cresce da solo** mentre le schede compilano il blocco, senza
regex da mantenere. `analogues.py stats` ne traccia l'adozione.

### Prima del quarto livello: perché `--direction` era nominale

Il `sentiment` unico veniva stampato su ogni data citata, incluse le 20-30 analogie
storiche. Risultato: **367 episodi su 844 con 2-3 direzioni insieme**, e
`macro_data/activity_growth` restituiva 28 episodi identici su 29 sia per `pos` che
per `neg`.

## Tre difetti di attribuzione corretti il 2026-08-26

Emersi tutti indagando una lacuna del 25/08: su `EURUSD=X` la mediana risultava
**positiva** dopo un dato europeo debole, perché il pool `pmi` era in larga parte fatto
di release americane.

Riguardavano `analogues.py`, **non la tassonomia**, e valevano per **ogni** etichetta —
sulla geografia erano solo più visibili, perché in un elenco omogeneo il vicino dice
spesso la stessa cosa del vero episodio.

**1. Righe corte ma complete** (`_has_own_text`)
`_contexts` estendeva alle righe vicine ogni riga sotto i 60 caratteri, per ricucire i
bullet spezzati. Ma non distingueva una riga *troncata* da una *corta e già completa*,
che assorbiva i vicini ed ereditava le loro etichette.
→ Ora si estende solo se, tolta la data e i marcatori di lista, restano meno di tre parole.

**2. Prosa lunga** (`_narrow`)
Una riga di prosa può nominare un episodio e poi cambiare argomento. Caso reale, dal §6
di una research: «L'episodio 2008-12-05 (payroll −533k) ha reazione intraday non
verificata puntualmente. Il ZEW "34,2" è di agosto 2026…» — un payroll USA etichettato
come europeo per via di uno ZEW citato due frasi dopo. Il filtro sulle righe con più
date ISO non lo intercetta: "agosto 2026" non è ISO.
→ Ora sopra i 200 caratteri si tiene la sola frase che contiene la data. **Esenti**
tabelle e bullet: lì tutte le frasi descrivono lo stesso episodio. Il marcatore di lista
richiede lo spazio dopo, altrimenti un `**Grassetto**` a inizio paragrafo passa per bullet.

**3. Nomi di etichetta troppo corti**
In `local_labels` un'etichetta dichiarata dal documento vale localmente se **tutte** le
sue parole compaiono nel contesto, ma quelle di ≤2 caratteri vengono scartate.
`eu_release` e `uk_release` si riducevano quindi entrambi alla sola parola "release":
qualunque contesto la contenesse li attivava tutt'e due.
→ Rinominati **`eurozone_release`** e **`britain_release`**.

Effetto complessivo: 61 episodi su 929 toccati, 79 etichette rimosse e 23 aggiunte
(1.617 → 1.561 etichette locali). I tre falsi positivi noti spariti, pool
`eurozone_release` pulito su tutti gli episodi verificabili.

## Trappole note

- ⚠ **Non usare prefissi di 1-2 lettere** nei nomi delle etichette canoniche (difetto 3).
- La fonte affidabile della **geografia** è il campo **dichiarato** nel blocco della
  scheda, non l'euristica. Template e runbook lo prescrivono dal 2026-08-26.
- Calibra i pattern nuovi sui contesti **reali**: le schede scrivono inglese tecnico
  — `FOMC`, `75bp`, `dot plot` — non italiano.
- Prima di scegliere un token per `--subtheme`, controlla la copertura con
  `analogues.py labels --theme <t>`.
- Aggiungere un'etichetta canonica = modificare `subtheme_taxonomy.yaml`, poi
  `analogues.py build`.
