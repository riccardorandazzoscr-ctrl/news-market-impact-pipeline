# Copertura asset: criteri e cronologia

**Quando aprire questo file:** stai valutando se aggiungere un asset al DB, o vuoi
capire perché un certo asset c'è (o non c'è).

Conteggio corrente: `sqlite3 market_data/market_data.db "SELECT COUNT(*) FROM assets;"`
— **non trascriverlo da nessuna parte.** È cambiato 10 volte in agosto 2026 e ogni
copia è diventata stale: al 2026-08-29 la mappa diceva ancora 68 con 78 in DB.

## I due modi di aggiungere un asset

**Reattivo** — una scheda si chiude senza asset misurabile, quindi si colma la lacuna.
È il modo con cui è cresciuto quasi tutto il DB fino a metà agosto 2026. Funziona ma
arriva sempre un giorno tardi.

**Audit non reattivo** — si cerca la lacuna prima che si manifesti. Primo caso il
2026-08-19 (14 asset in un colpo: tutti buchi già segnalati fra il 5 e il 14 agosto e
mai colmati). Secondo caso il 2026-08-29 (NZD=X, SEK=X a completare il G10 valutario),
deciso dopo la **terza istanza in dieci giorni** della stessa classe di scarto —
Corea 12-27/08 → Australia 20-26/08 → RBNZ 28/08.

Il segnale che serve un audit: **la stessa classe di scarto in triage si ripete.**
Non il singolo caso, la ripetizione.

## Cronologia delle aggiunte

Base: 17 asset originali.

| data | aggiunti | motivo |
|---|---|---|
| 2026-06-05 | `^NDX` `SOXX` `URA` `LIT` `EEM` `HYG` `^VIX` `HG=F` `DX-Y.NYB` | audit strato 2 |
| 2026-07-07 | `TTF=F` `EXH9.DE` | canale energetico UE: gas europeo, utility/proxy elettricità |
| 2026-07-13 | `CNY=X` | canale valuta cinese / dazi |
| 2026-07-19 | `EWZ` `BRL=X` | canale LatAm |
| 2026-07-30 | `THB=X` `SGD=X` `MYR=X` `IDR=X` `THD` `EWS` `EIDO` | `EEM` troppo diluito per il Sud-Est asiatico |
| 2026-08-10 | `SHLD.L` `EWY` `EWT` | difesa globale/NATO-Europa, Corea, Taiwan: canali difesa europea e memoria/HBM-Taiwan segnalati ripetutamente come strutturalmente invisibili |
| 2026-08-16 | `CAD=X` | dazi/attriti USA-Canada, assente mentre i dazi erano diventati strumento ricorrente |
| 2026-08-18 | `^TYX` `IGLT.L` `1482.T` `VGB.AX` `^GSPTSE` `EXV7.DE` | dopo il selloff sincronizzato sulle curve: 30Y USA, gilt, JGB, ACGB, azionario canadese, chimica europea |
| 2026-08-19 | `IGV` `XLE` `IYT` `XLV` `ITA` `REMX` `TAN` `INDA` `INR=X` `KRW=X` `NOK=X` `ILS=X` `^FVX` `^MOVE` | **primo audit non reattivo** |
| 2026-08-26 | `KWEB` `CQQQ` | canale CONSUMO cinese: la domanda interna non era misurabile (`CNY=X` compresso dal fixing PBOC, `EEM` troppo diluito, `HG=F` prezza le infrastrutture) al punto che una trimestrale PDD era entrata come evidenza macro |
| 2026-08-27 | `AUD=X` `^AXJO` | un dato RBA scartato in triage per sola assenza di asset, con `VGB.AX` unico proxy — un prezzo di ETF obbligazionario, né cambio né azionario |
| 2026-08-27 | `XLY` `XLP` `XRT` | consumo USA: seconda volta in agosto che una scheda sul consumatore americano si chiudeva senza asset (il PCE di luglio, beni −49,9 mld contro servizi +86,2 mld, non era misurabile) |
| 2026-08-29 | `NZD=X` `SEK=X` | **completano il G10 valutario** (audit non reattivo, vedi sopra) |
| 2026-08-29 | `IWM` `GDX` `XLU` | fattore dimensione/small cap, minatori auriferi, utility USA per il vincolo elettrico del capex AI |

## Lacune aperte

**🔴 Rame LME — la dislocazione tariffaria non è misurabile** (verificato 2026-08-27).
`HG=F` è il contratto **Comex**, cioè il lato *interno* alla dislocazione; lo spread
LME-Comex — la variabile che esprime la distorsione da dazi — richiede il riferimento
londinese, che yfinance non espone.

Candidati testati e **scartati**: `COPA.L` (WisdomTree Copper) e `CPER` tracciano
entrambi il Bloomberg Copper Subindex, **basato su Comex** — correlazione dei
rendimenti giornalieri `COPA.L`↔`HG=F` **0,88** dal 2024, performance cumulata
sovrapponibile: replicano l'asset che abbiamo invece di completarlo. `LME=F`, `3MCU.L`,
`CUKC.L`, `JJC` non esistono su yfinance. Serve una fonte esterna — stessa classe di
problema dello spread BTP-Bund.

⚠ **Non aggiungere un ETC "sul rame" credendo di aver colmato la lacuna.**

**Equipaggiamento di rete e turbine** — `XLU` misura la *domanda* elettrica, non chi
vende gli impianti. `GRID` è stato valutato e **scartato** il 2026-08-29: correlava
0,80 con `SOXX`, cioè confondeva i due canali invece di separarli.

## Trappole note

- Un ETF "sul tema X" spesso traccia lo stesso sottostante di un asset già in DB.
  **Misura la correlazione dei rendimenti giornalieri prima di aggiungerlo**: sopra
  ~0,85 è un duplicato, non una copertura nuova.
- Un ETF obbligazionario non è un proxy né per il cambio né per l'azionario di quel
  paese (caso `VGB.AX` per l'Australia).
