# Convenzioni di lettura degli asset

**Quando aprire questo file:** stai scrivendo una scheda che tocca obbligazionario,
small cap, oro/minatori, spesa AI o consumo USA. Sono i casi in cui **il livello di
un asset da solo dice la cosa sbagliata.**

## ⚠ Obbligazionario: la convenzione di segno è mista, di proposito

**Rendimenti** (salgono in un selloff): `^TNX` 10Y, `^FVX` 5Y, `^TYX` 30Y.

**Prezzi di ETF** (scendono nello stesso selloff): `IEF`, `IEAG.AS`, `EXX6.DE`,
`IGLT.L` (gilt), `1482.T` (JGB), `VGB.AX` (ACGB).

Un selloff obbligazionario globale sincronizzato stampa quindi `^TYX` **positivo** e
gli altri **negativi**: è **accordo, non divergenza**. Ogni scheda che ne tocca due
deve dirlo esplicitamente.

## ⚠ Tre asset da leggere come SPREAD, non come livello

Dal 2026-08-29.

| coppia | cosa misura | perché il livello non basta |
|---|---|---|
| `IWM`/`^GSPC` | fattore dimensione | `IWM` correla **0,87** con l'indice: da solo non dice nulla. Lo spread ha dev.std 0,81%/giorno e supera l'1% nel 19% delle sedute |
| `GDX`/`GC=F` | leva dei minatori sull'oro | β **1,58**. Agosto 2026: oro +15,6%, `GDX` +36,3% |
| `SOXX`/`XLU` | dove va la spesa AI: chip o rete elettrica | `XLU` è ortogonale al tech (0,31; residuo −0,21 al netto del mercato) |

**Il caso `GDX` ha un secondo livello**: in un vero deleveraging `GDX` è **equity** e
può scendere col mercato invece che col metallo. Quella divergenza **è essa stessa il
segnale**, non un errore di lettura.

`GRID` è stato valutato e **scartato** il 2026-08-29: correlava 0,80 con `SOXX`, cioè
confondeva i due canali invece di separarli.

## ⚠ Consumo USA: leggi il RAPPORTO, non il livello

Dal 2026-08-27. La rotazione difensiva sta in **`XLY`/`XLP`** — i livelli sono
dominati dal beta di mercato.

- `XLY` è cap-weighted e dominato da Amazon+Tesla: **correla 0,89 con `^GSPC`**. Da
  solo non è il consumatore, è mezzo mega-cap tech.
- `XRT` (retail, pesi distribuiti) correla 0,76 con `XLY` e 0,71 con `^GSPC`. È la
  **correzione di quella distorsione, non un duplicato**: su una notizia di spesa
  delle famiglie usali insieme e commenta la divergenza.
- `XLY` e `XLP` correlano solo **0,54** fra loro — sono davvero due cose diverse.

## 🔴 Rame: la dislocazione tariffaria non è misurabile

`HG=F` è **Comex**, il lato interno alla dislocazione. Manca il riferimento LME.
Dettaglio e candidati già scartati in [copertura_asset.md](copertura_asset.md).
