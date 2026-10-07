# Esperimenti provati e scartati

**Quando aprire questo file:** stai per proporre un miglioramento al metodo. Controlla
prima se è già stato provato e misurato — qui ci sono le idee che sembrano buone e non
funzionano, con il motivo.

⚠ **Non ri-implementare nulla di quanto segue senza nuove evidenze.**

## Correzione per "rendimento anomalo" — scartata il 2026-08-10

**L'idea.** Le schede si scrivono nei momenti drammatici, che tendono a coincidere con
estremi locali di mercato. Sembra quindi sensato sottrarre la "deriva normale"
dell'asset — la mediana dei rendimenti a T+N su una finestra di stima di 250 giorni di
borsa **prima** dell'ancora (nessun look-ahead) — per neutralizzare quella distorsione.

**Testata in due modi, entrambi falliti.**

| variante | effetto su IC per-asset | hit rate |
|---|---|---|
| asimmetrica (solo lato realizzato) | +0,021 → **+0,008** (peggiora) | 51,3% → 49,6% |
| simmetrica e rigorosa (entrambi i lati, liste `--events` reali ricostruite dalle schede, 1.405 righe) | −0,015 → −0,012 (nulla) | 49,0% → 50,3% |

**Perché non funziona** — è una spiegazione, non una scusa. La distorsione da selezione
colpisce **allo stesso modo** il pool storico e il rendimento realizzato: entrambi sono
campionati in momenti drammatici. Quindi si **cancella nella correlazione di rango**.
La correzione sposta le *magnitudini*, non i *ranghi* — e l'IC misura i ranghi.

Coerente col fatto che la copertura delle bande è già ~45-50%, cioè ben tarata.

**Conclusione:** complessità non giustificata. Il vero problema era un altro — il bug
sulla direzione, vedi sotto.

## Cancello sul seguito «|z| ≥ 2 dal normale» — scartato il 2026-10-07, prima del go-live

**L'idea** (Run 11). Il segno del seguito T+h non ha informazione (~50%), ma forse ce l'ha quando la
mediana del pool si stacca molto dal comportamento normale dell'asset:
z = (mediana pool − mediana dei rendimenti a h sedute delle 250 sedute prima) / (IQR/1,349/√N).
Solo con |z| ≥ 2 e N ≥ 10 una tabella poteva diventare `[previsione]`.

**Cosa è successo.** Sui dati già visti (ledger al 2026-10-07, T+5, un voto per giorno) il cancello
fa 34 giorni sopra il 50% e 11 sotto. La regola cieca «sempre sotto la mediana normale», sulle
stesse celle, fa 33/11. Permutando i segni del pool dentro il giorno p ≈ 0,1; con «normale» = 0 il
cancello fa 24/16 (p 0,13).

**Perché.** Nel periodo il realizzato sta sotto la mediana delle 250 sedute precedenti in due celle su
tre, e il pool (vicino a zero) ci sta sotto nel 75%: la mediana delle 250 sedute incorpora la deriva
dell'anno prima, e quando la deriva rallenta «sotto il normale» indovina comunque. Stesso difetto di
fondo della «correzione per rendimento anomalo» qui sopra (lì si correggeva la stima, qui si sceglieva
quando parlare): la mediana delle 250 sedute non è un riferimento neutro.

**Riproducibile:** `news_impact_pipeline/venv/bin/python news_impact_pipeline/quant_reazione.py replay`
(righe «benchmark sempre sotto/sopra il normale»). Protocollo `experiments/quant_reazione/protocol-1.0.0.json`
registrato e mai eseguito.

**Regola che ne esce:** un segnale direzionale si confronta con un benchmark costante sulle stesse
celle (o con una permutazione), mai solo con il 50%.

## Ipotesi escluse nell'indagine "perché il rifugio è rovesciato" (2026-08-10)

La causa vera era un **bug** (`cmd_build` collassava le direzioni multiple in "mixed",
rendendo le previsioni cieche alla direzione). Già corretto. Ma lungo la strada tre
spiegazioni plausibili sono state testate e **scartate con i dati**. Sono documentate
qui per non ri-testarle:

1. **Ancoraggio post-spike** — il movimento nel giorno-ancora è solo ~1,2x il normale.
   Troppo poco.
2. **Disallineamento temporale fra schede e knowledge base** — differenze piccole e
   incoerenti fra loro: oro −0,53pp ma petrolio +2,28pp. Nessun pattern.
3. **Cambio di regime del dollaro** — esiste ma è graduale: da +0,04% a −0,33% dal
   pre-2024 al 2025. Troppo poco per spiegare un errore del 100%.

Per il dettaglio del bug e della catena diagnostica vedi
[leggere_lo_scorecard.md](leggere_lo_scorecard.md).

## La regola generale che ne è uscita

Un difetto può restare **invisibile per mesi** se manca la vista che lo mostrerebbe.
L'edge spaccato per asset è rimasto nascosto finché la scorecard non ha avuto una vista
per-asset: prima c'erano solo le viste per orizzonte, confidenza e tema.

Quando un risultato aggregato è mediocre, **chiediti quale scomposizione non stai
guardando** prima di concludere che il sistema non funziona.
