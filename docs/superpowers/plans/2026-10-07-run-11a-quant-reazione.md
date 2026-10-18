# Run 11a — Protocollo + replay esplorativo: piano operativo

> **Per gli agenti esecutori:** SUB-SKILL RICHIESTA: superpowers:subagent-driven-development (consigliata)
> o superpowers:executing-plans per eseguire il piano task per task. I passi usano checkbox (`- [ ]`).

**Obiettivo:** registrare il protocollo del cancello sul seguito (`protocol-1.0.0.json`) **prima** di
qualunque codice, poi rendere rieseguibili, in sola lettura, le misure esplorative 1–4 che hanno motivato
il Run 11.

**Architettura:** un file JSON in `experiments/quant_reazione/` (stesso schema dei protocolli del
laboratorio CPI), committato da solo. Poi uno script in `news_impact_pipeline/quant_reazione.py`, stessa
collocazione di `cpi_lab.py`, che legge le definizioni dal protocollo e calcola le misure su ledger,
libreria episodi e DB prezzi aperto in sola lettura. Funzioni pure (σ60, baseline, z, cancello, voto)
testate su serie sintetiche; caricatori con il prezzo iniettato; misure e comando `replay` verificati sui
dati veri del repo. Nessun output su disco: si stampa e basta.

**Stack:** Python del venv (`news_impact_pipeline/venv/bin/python`), numpy 2.4, pandas 3.0, PyYAML,
unittest. **Niente scipy** (non è installato): la binomiale si calcola con `math.comb`.

**Spec:** `PIANO_REVISIONE_PIPELINE.md`, sezione «Run 11 — Quantitativo «reazione, non seguito»: SPEC»
(commit `1249fac`). Chi esegue legge **anche** quella sezione.

**Prova del codice:** il modulo e i test qui sotto sono stati eseguiti su un prototipo il 2026-10-07:
16 test verdi, con i warning trattati come errori (`-W error`), replay sui dati veri in ~5 s.

## Vincoli globali

- **Nessuna modifica alla pipeline nell'11a:** `event_study.py`, `forecast_tracking.py`, `analogues.py`,
  template, runbook, `render_report.py` e plist launchd restano intatti. Si importano, non si toccano.
- **Il protocollo si committa da solo, prima di ogni codice che lo legge**, e non si modifica mai più: una
  variante è un file nuovo (`protocol-1.1.0.json`).
- **Sola lettura:** DB aperto con `file:{DB_PATH}?mode=ro`; ledger e `_episodes.yaml` solo letti; nessun
  file di output. Gli indicatori calcolati non si persistono mai (CLAUDE.md).
- **Commit chirurgici:** il working tree ha modifiche del maintainer non committate
  (`daily_analysis/forecast_ledger.csv`, `knowledge_base/_direction_reviews.yaml`, `_episodes.yaml`,
  `catalog.yaml`, `news_impact_pipeline/glossario.md`, la scorecard W41, la cartella KB «Gas europeo…»).
  **Mai `git add -A` o `git add .`:** si aggiungono solo i file elencati nel task.
- Messaggi di commit **in inglese** e chiusi da `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`;
  documenti, commenti e output in italiano.
- L'output riporta sempre la numerosità (celle, giorni). È marcato «ESPLORATIVO: … non conta come prova».
- Soglie del protocollo (dalla spec, testuali): `|z| ≥ 2` **e** `N ≥ 10`; orizzonte primario **T+5**;
  α = 0,05; decisione a **60 giorni** (portata da 40 a 60 dal maintainer il 2026-10-07, per la potenza); σ su **60** sedute; baseline su **250** sedute.
- I test sono `unittest`, non distruttivi, registrati in `run_tests.sh` sotto il filtro `quant`.

## Focus della revisione

Ingressi che la spec implica ma che nessun caso felice esercita, dal più probabile:

1. **Serie mensile o rada** (una serie FRED derivata): va esclusa, non deve dare una σ60 calcolata su
   cinque anni. Test: `test_serie_mensili_assenti_o_con_buchi` (Task 3).
2. **Prezzi ≤ 0 nella finestra** (spread o crack vicini allo zero): la cella è esclusa, niente `inf` o
   `NaN` che finiscono nelle mediane. Test: `test_prezzi_non_positivi_escludono_la_cella` (Task 2).
3. **`anchor_date` congelata assente dalla serie di oggi** (buco o storico riscritto): la riga è esclusa,
   non riallineata in silenzio a un'altra seduta. Test: `test_righe_escluse_dal_ledger`, caso «sabato» (Task 3).
4. **Storia corta prima dell'ancora** (meno di 250+h sedute): la cella resta per la misura 1 ma esce dalle
   misure 2 e 4. Test: `test_storia_corta_o_banda_mancante_restano_solo_per_la_misura_1` (Task 3).
5. **Il replay non scrive niente** e non stampa `nan`. Test: `test_replay_sui_dati_del_repo_in_sola_lettura`,
   che confronta l'hash del ledger prima e dopo (Task 4).

---

### Task 1: Registrare il protocollo 1.0.0 (prima di qualsiasi codice)

**File:**
- Crea: `experiments/quant_reazione/protocol-1.0.0.json`

**Interfacce:**
- Produce: le chiavi lette dal codice nei Task 2–4. Sono `protocol_version`, `sigma_window_sessions` (60),
  `baseline_window_sessions` (250), `primary_horizon_sessions` (5), `gate.z_min` (2.0), `gate.n_min` (10),
  `test.alpha` (0.05), `decision.days` (60) e `decision.critical_days_above` (37).

- [ ] **Passo 1: Scrivere il protocollo**

Crea `experiments/quant_reazione/protocol-1.0.0.json` con esattamente questo contenuto:

```json
{
  "protocol_version": "1.0.0",
  "experiment": "Run 11 — seguito oltre il normale: il cancello |z| ≥ 2 indica quando la mediana del pool dice qualcosa sul seguito a T+5",
  "registered_at": "2026-10-07",
  "spec": "PIANO_REVISIONE_PIPELINE.md, sezione «Run 11 — Quantitativo «reazione, non seguito»» (approvata il 2026-10-07)",
  "hypothesis": "Nelle celle in cui la mediana del pool di analoghi si stacca dalla mediana normale dell'asset di almeno 2 errori standard, con N ≥ 10, il rendimento realizzato a T+5 si stacca dalla mediana normale nello stesso verso più spesso che nel verso opposto. Unità di prova: il giorno di analisi.",
  "price_column": "adj_close con fallback su close (event_study.load_price_series); solo sedute con prezzo valido; serie mensili escluse (event_study.detect_monthly_data); prezzi ≤ 0 nella finestra → cella esclusa",
  "sigma_window_sessions": 60,
  "baseline_window_sessions": 250,
  "primary_horizon_sessions": 5,
  "secondary_horizons_sessions": [1, 3, 10],
  "gate": {
    "z_min": 2.0,
    "n_min": 10,
    "rule": "|z| ≥ z_min e N ≥ n_min; z non definito → sotto cancello"
  },
  "definitions": {
    "a": "seduta-ancora: prima seduta con prezzo ≥ data di analisi (made_date); coincide con l'anchor_date congelato nel ledger",
    "sigma60": "deviazione standard campionaria (ddof=1) dei log-rendimenti ln(P[t]/P[t−1]) per t = a−60 … a−1; nessun prezzo ≥ a",
    "R0_z0": "R0 = (P[a]/P[a−1] − 1)·100; z0 = ln(P[a]/P[a−1]) / sigma60 (solo descrittivi in questa versione)",
    "mediana_normale": "mediana dei rendimenti (P[t]/P[t−h] − 1)·100 delle 250 finestre di h sedute che terminano in t = a−250 … a−1, calcolata alla data di analisi (non degli episodi); con meno storia la cella è esclusa",
    "z": "(mediana_pool − mediana_normale) / (|p75_pool − p25_pool| / 1,349 / √N); IQR nullo → z non definito",
    "N": "n_analogues della tabella: episodi dopo il dedup per giorno-ancora di event_study.compute_returns",
    "realizzato": "realized_return congelato da forecast_tracking evaluate (ancora a, T+h)",
    "scostamento_indovinato": "1 se segno(realizzato − mediana_normale) = segno(mediana_pool − mediana_normale), 0 altrimenti; cella esclusa se una delle due differenze è esattamente zero"
  },
  "cells": "Righe del ledger con scenario base, registrazione originale (non recovered), uso diverso da ritirata, ingestion_status diverso da quarantine, baseline_median valorizzata, realizzato maturo a T+5 e data di analisi ≥ go-live. Contano tutte le celle sopra cancello, [previsione] o [descrittiva]: il cancello si ricalcola dai numeri della tabella, non dall'etichetta.",
  "go_live": "Prima data di analisi con baseline_median valorizzata nel ledger; si scrive in PIANO_REVISIONE_PIPELINE.md alla chiusura del Run 11d. Nessuna riga precedente conta.",
  "metric": "Voto per giorno: quota delle celle sopra cancello a T+5 con scostamento indovinato. Il giorno è «sopra» se la quota è > 0,5, «sotto» se < 0,5, «pari» se = 0,5.",
  "test": {
    "kind": "binomiale esatto unilaterale sui giorni sopra contro sotto (pari esclusi), H0 p = 0,5, H1 p > 0,5",
    "alpha": 0.05
  },
  "decision": {
    "days": 60,
    "critical_days_above": 37,
    "when": "Una sola volta, quando almeno 60 giorni non pari hanno tutte le celle T+5 mature; contano i primi 60 in ordine di data. Nessuna analisi intermedia.",
    "confermato": "Il cancello resta la regola per [previsione].",
    "non_confermato": "Nessuna previsione sul seguito: la parte quantitativa resta reazione + già prezzato + «seguito non distinguibile»; annotazione in references/esperimenti_scartati.md, distinta dalla «correzione per rendimento anomalo» scartata il 2026-08-10."
  },
  "robustness": "Dichiarati qui, riportati accanto all'esito: (1) autocorrelazione lag-1 dei voti in ordine di data; se supera +0,2 il test decisivo si rifà, con lo stesso alfa, sui soli voti fra i primi 60 distanti almeno 5 sedute dal voto tenuto prima (diradamento cronologico) e decide quello; (2) controllo: stesso voto sulle celle con |z| < 1 e N ≥ 10 a T+5, solo descrittivo; (3) orizzonti secondari e sole tabelle [previsione], solo descrittivi.",
  "evidence_at_registration": "Già visto, NON valido come prova. Misurato il 2026-10-07 col prototipo del replay (stesse definizioni di questo protocollo; committato subito dopo come news_impact_pipeline/quant_reazione.py) sul ledger del 2026-10-07: 63 giorni di analisi con celle mature a T+5, 47 con almeno una cella sopra cancello; giorni sopra 34, sotto 11, pari 2 (76% dei non pari; 269 celle); autocorrelazione lag-1 dei voti −0,06; controllo |z| < 1: sopra 21, sotto 20, pari 9. Prima misura (script usa e getta, N ≥ 5, tutti gli orizzonti): sopra 46, sotto 17. Ritmo atteso: circa 3 giorni di analisi su 4 hanno una cella sopra cancello, quindi 60 giorni non pari in circa 85–90 giorni di analisi. Potenza del test a 60 giorni: 45% se la quota vera di giorni sopra è 0,60; 75% se 0,65; 88% se 0,68; 98% se 0,73 (a 40 giorni sarebbe stata 32/57/72/90%: per questo il maintainer ha portato la decisione da 40 a 60 giorni prima della registrazione). Un effetto trovato guardando i dati di solito si restringe: aspettativa a priori moderata.",
  "revision_rule": "Il protocollo non si modifica dopo la registrazione: una variante è un file nuovo (protocol-1.1.0.json, …)."
}
```

- [ ] **Passo 2: Verificare che sia JSON valido e che la soglia critica torni**

Esegui:
```bash
news_impact_pipeline/venv/bin/python -m json.tool experiments/quant_reazione/protocol-1.0.0.json > /dev/null && echo JSON_OK
news_impact_pipeline/venv/bin/python -c "import math; n=60; t=lambda k: sum(math.comb(n,i) for i in range(k,n+1))/2**n; print(round(t(37),4), round(t(36),4))"
```
Atteso: `JSON_OK`, poi `0.0462 0.0775`. Cioè 37 su 60 è la prima soglia con p ≤ 0,05.

- [ ] **Passo 3: Commit (solo il protocollo)**

```bash
git add experiments/quant_reazione/protocol-1.0.0.json
git commit -m "$(cat <<'EOF'
Pre-register the Run 11 follow-through gate protocol (1.0.0) before any code reads it

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
git show --stat HEAD   # deve elencare SOLO il protocollo
```

---

### Task 2: Definizioni del protocollo (funzioni pure) e suite `quant`

**File:**
- Crea: `news_impact_pipeline/quant_reazione.py`
- Crea: `news_impact_pipeline/tests/test_quant_reazione.py`
- Modifica: `news_impact_pipeline/run_tests.sh`, aggiungendo la riga di commento nell'intestazione e il
  blocco del filtro `quant` dopo quello del filtro `cpi`

**Interfacce:**
- Consuma: `experiments/quant_reazione/protocol-1.0.0.json` (Task 1).
- Produce, in `quant_reazione` (`p` è un `np.ndarray` di prezzi, `a` l'indice posizionale della seduta-ancora):
  - `load_protocol() -> dict`, che legge il modulo-globale `PROTOCOL_PATH`;
  - `sigma(p, a, window) -> float | None`;
  - `reaction(p, a, window) -> tuple[float, float] | None`, che restituisce `(R0 %, z0)`;
  - `baseline(p, a, h, window) -> np.ndarray | None`;
  - `abs_z_all_sessions(s: pd.Series, window) -> pd.Series`;
  - `deviation_z(med, p25, p75, n, normal_median) -> float | None`;
  - `passes_gate(z, n, gate: dict) -> bool`;
  - `deviation_hit(med, normal_median, realized) -> int | None`;
  - `daily_votes(cells: list[dict]) -> pd.Series`, con indice giorno e valore la quota delle celle con
    `hit` = 1;
  - `binom_one_sided(k, n) -> float`;
  - `vote_test(votes) -> dict`, con chiavi `above`, `below`, `ties` e `p`;
  - `lag1_autocorr(votes) -> float`;
  - `spearman(a, b) -> float`.

- [ ] **Passo 1: Scrivere i test che falliscono**

Crea `news_impact_pipeline/tests/test_quant_reazione.py`. Il blocco di import è già quello finale: i Task
3 e 4 aggiungono solo classi.

```python
"""Run 11a — definizioni del protocollo «reazione, non seguito» e replay esplorativo (sola lettura)."""
import contextlib
import hashlib
import io
import math
import re
import sqlite3
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import quant_reazione as q

GATE = {"z_min": 2.0, "n_min": 10}
PROTO = {"sigma_window_sessions": 60, "baseline_window_sessions": 250}


def series(n=400, seed=0):
    rng = np.random.default_rng(seed)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))),
                     index=pd.bdate_range("2020-01-01", periods=n), name="AAA")


class Definizioni(unittest.TestCase):
    def test_sigma_vede_solo_le_60_sedute_fino_ad_a_meno_1(self):
        p, a = series().to_numpy().copy(), 300
        s0 = q.sigma(p, a, 60)
        self.assertAlmostEqual(s0, np.std(np.diff(np.log(p[a - 61:a])), ddof=1))
        futuro = p.copy(); futuro[a:] *= 1.5
        self.assertEqual(q.sigma(futuro, a, 60), s0)
        fuori = p.copy(); fuori[a - 62] *= 1.5
        self.assertEqual(q.sigma(fuori, a, 60), s0)
        dentro = p.copy(); dentro[a - 61] *= 1.5
        self.assertNotEqual(q.sigma(dentro, a, 60), s0)
        self.assertIsNone(q.sigma(p, 60, 60))
        self.assertIsNotNone(q.sigma(p, 61, 60))

    def test_reazione_r0_e_z0(self):
        p, a = series().to_numpy().copy(), 300
        p[a - 1], p[a] = 100.0, 102.0
        r0, z0 = q.reaction(p, a, 60)
        self.assertAlmostEqual(r0, 2.0)
        self.assertAlmostEqual(z0, math.log(1.02) / q.sigma(p, a, 60))

    def test_prezzi_non_positivi_escludono_la_cella(self):
        p, a = series().to_numpy().copy(), 300
        zero = p.copy(); zero[a - 5] = 0.0
        self.assertIsNone(q.reaction(zero, a, 60))
        self.assertIsNone(q.baseline(zero, a, 5, 250))
        neg = p.copy(); neg[a] = -1.0
        self.assertIsNone(q.reaction(neg, a, 60))

    def test_baseline_250_finestre_che_finiscono_in_a_meno_1(self):
        p, a = series().to_numpy().copy(), 300
        base = q.baseline(p, a, 5, 250)
        self.assertEqual(len(base), 250)
        self.assertAlmostEqual(base[-1], (p[299] / p[294] - 1) * 100)
        self.assertAlmostEqual(base[0], (p[50] / p[45] - 1) * 100)
        futuro = p.copy(); futuro[a:] *= 1.5
        np.testing.assert_array_equal(q.baseline(futuro, a, 5, 250), base)
        self.assertIsNone(q.baseline(p, 254, 5, 250))
        self.assertIsNotNone(q.baseline(p, 255, 5, 250))

    def test_z_di_tutte_le_sedute_coincide_con_reaction(self):
        s = series()
        p, z = s.to_numpy(), q.abs_z_all_sessions(s, 60)
        self.assertNotIn(s.index[60], z.index)
        for t in (61, 200, 399):
            self.assertAlmostEqual(z.loc[s.index[t]], abs(q.reaction(p, t, 60)[1]))

    def test_indice_di_scostamento(self):
        self.assertAlmostEqual(q.deviation_z(1.0, -0.5, 1.5, 16, 0.2), 0.8 / (2.0 / 1.349 / 4))
        self.assertAlmostEqual(q.deviation_z(1.0, 1.5, -0.5, 16, 0.2), q.deviation_z(1.0, -0.5, 1.5, 16, 0.2))
        self.assertIsNone(q.deviation_z(1.0, 0.3, 0.3, 16, 0.2))

    def test_cancello(self):
        self.assertTrue(q.passes_gate(2.0, 10, GATE))
        self.assertTrue(q.passes_gate(-2.0, 10, GATE))
        self.assertFalse(q.passes_gate(1.99, 10, GATE))
        self.assertFalse(q.passes_gate(2.5, 9, GATE))
        self.assertFalse(q.passes_gate(None, 30, GATE))

    def test_scostamento_indovinato(self):
        self.assertEqual(q.deviation_hit(1.0, 0.2, 0.5), 1)
        self.assertEqual(q.deviation_hit(1.0, 0.2, 0.1), 0)
        self.assertEqual(q.deviation_hit(-1.0, 0.2, -0.3), 1)
        self.assertIsNone(q.deviation_hit(1.0, 0.2, 0.2))
        self.assertIsNone(q.deviation_hit(0.2, 0.2, 1.0))

    def test_voto_per_giorno_e_test_binomiale(self):
        cells = [{"day": "d1", "hit": 1}, {"day": "d1", "hit": 1}, {"day": "d2", "hit": 1},
                 {"day": "d2", "hit": 0}, {"day": "d3", "hit": 0}, {"day": "d4", "hit": 1},
                 {"day": "d4", "hit": None}]
        v = q.daily_votes(cells)
        self.assertEqual(v.to_dict(), {"d1": 1.0, "d2": 0.5, "d3": 0.0, "d4": 1.0})
        self.assertEqual(q.vote_test(v), {"above": 2, "below": 1, "ties": 1, "p": 0.5})

    def test_soglia_critica_del_protocollo(self):
        proto = q.load_protocol()
        k, n, alpha = proto["decision"]["critical_days_above"], proto["decision"]["days"], proto["test"]["alpha"]
        self.assertLessEqual(q.binom_one_sided(k, n), alpha)
        self.assertGreater(q.binom_one_sided(k - 1, n), alpha)
        self.assertEqual((proto["gate"]["z_min"], proto["gate"]["n_min"], proto["primary_horizon_sessions"]),
                         (2.0, 10, 5))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Passo 2: Verificare che falliscano**

Esegui: `news_impact_pipeline/venv/bin/python news_impact_pipeline/tests/test_quant_reazione.py -v`
Atteso: errore all'import, `ModuleNotFoundError: No module named 'quant_reazione'`.

- [ ] **Passo 3: Scrivere il modulo con le definizioni**

Crea `news_impact_pipeline/quant_reazione.py`. Il blocco di import è già quello finale: alcuni moduli
servono solo ai Task 3–4, ed è voluto, per non riscrivere l'intestazione a ogni task.

```python
#!/usr/bin/env python3
"""Replay esplorativo del Run 11 — Quantitativo «reazione, non seguito» (sola lettura).

Riproduce le misure 1–4 di «Il problema, misurato» (PIANO_REVISIONE_PIPELINE.md, Run 11) su
ledger, libreria episodi e DB prezzi. ESPLORATIVO: sono dati già visti, non conta come prova.
Le definizioni (σ60, baseline normale, z, cancello, orizzonte primario) si leggono dal protocollo
experiments/quant_reazione/protocol-1.0.0.json; la prova vera è prospettica (Run 11e).

    venv/bin/python quant_reazione.py replay
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sqlite3
import sys
from datetime import date
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from analogues import LIB_PATH
from bootstrap_market_data import DB_PATH
from event_study import detect_monthly_data, load_price_series
from forecast_tracking import FLAT_THRESHOLD, LEDGER_PATH

PROTOCOL_PATH = Path(__file__).resolve().parents[1] / "experiments/quant_reazione/protocol-1.0.0.json"
HORIZONS = [1, 3, 5, 10]
EXPLORATIVE_N_MIN = 5         # soglia della fotografia del 2026-10-07 (il protocollo usa gate.n_min)
SPLIT_DAY = "2026-08-15"      # stabilità prima/dopo, come nella fotografia
ANY_DAY_ABS_Z = 0.674         # mediana di |N(0,1)|: «un giorno qualsiasi» in teoria


def load_protocol() -> dict:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


# --- definizioni del protocollo (pure) --------------------------------------------------------

def sigma(p: np.ndarray, a: int, window: int) -> float | None:
    """σ campionaria dei log-rendimenti delle `window` sedute che finiscono in a−1; mai prezzi ≥ a."""
    if a - window - 1 < 0:
        return None
    seg = p[a - window - 1:a]
    if (seg <= 0).any():
        return None
    s = float(np.std(np.diff(np.log(seg)), ddof=1))
    return s if s > 0 else None


def reaction(p: np.ndarray, a: int, window: int) -> tuple[float, float] | None:
    """(R0 in %, z0) della seduta a contro a−1; None se σ non è calcolabile."""
    s = sigma(p, a, window)
    if s is None or p[a] <= 0:
        return None
    return (p[a] / p[a - 1] - 1) * 100, math.log(p[a] / p[a - 1]) / s


def baseline(p: np.ndarray, a: int, h: int, window: int) -> np.ndarray | None:
    """Rendimenti a h sedute (%) delle `window` finestre che terminano in a−window … a−1."""
    if a - window - h < 0:
        return None
    seg = p[a - window - h:a]
    if (seg <= 0).any():
        return None
    return (seg[h:] / seg[:-h] - 1) * 100


def abs_z_all_sessions(s: pd.Series, window: int) -> pd.Series:
    """|z0| di ogni seduta della serie, con la stessa σ di `sigma` (controllo «giorno qualsiasi»)."""
    lr = np.log(s.where(s > 0)).diff()
    return (lr / lr.rolling(window).std().shift(1)).abs().dropna()


def deviation_z(med: float, p25: float, p75: float, n: int, normal_median: float) -> float | None:
    iqr = abs(p75 - p25)
    if iqr == 0 or n < 1:
        return None
    return (med - normal_median) / (iqr / 1.349 / math.sqrt(n))


def passes_gate(z: float | None, n: int, gate: dict) -> bool:
    return z is not None and abs(z) >= gate["z_min"] and n >= gate["n_min"]


def deviation_hit(med: float, normal_median: float, realized: float) -> int | None:
    """1 se il realizzato si scosta dal normale nel verso della mediana del pool; None se uno scarto è zero."""
    d_pool, d_real = med - normal_median, realized - normal_median
    if d_pool == 0 or d_real == 0:
        return None
    return int((d_pool > 0) == (d_real > 0))


def daily_votes(cells: list[dict]) -> pd.Series:
    """Quota giornaliera di celle con hit = 1 (hit None escluse), in ordine di giorno."""
    df = pd.DataFrame([c for c in cells if c["hit"] is not None], columns=["day", "hit"])
    return df.groupby("day")["hit"].mean().sort_index()


def binom_one_sided(k: int, n: int) -> float:
    """P(X ≥ k) con X ~ Binomiale(n, 0,5)."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def vote_test(votes: pd.Series) -> dict:
    above, below = int((votes > 0.5).sum()), int((votes < 0.5).sum())
    return {"above": above, "below": below, "ties": len(votes) - above - below,
            "p": binom_one_sided(above, above + below) if above + below else float("nan")}


def lag1_autocorr(votes: pd.Series) -> float:
    x = (votes[votes != 0.5] > 0.5).to_numpy(dtype=float)
    if len(x) < 3 or x[:-1].std() == 0 or x[1:].std() == 0:
        return float("nan")
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def spearman(a, b) -> float:
    return pd.Series(list(a)).rank().corr(pd.Series(list(b)).rank())
```

- [ ] **Passo 4: Verificare che passino**

Esegui: `news_impact_pipeline/venv/bin/python -W error news_impact_pipeline/tests/test_quant_reazione.py -v`
Atteso: `Ran 10 tests` … `OK`, senza warning.

- [ ] **Passo 5: Registrare la suite in `run_tests.sh`**

Nell'intestazione, dopo la riga `#   ./run_tests.sh brief …`, aggiungi:

```bash
#   ./run_tests.sh quant        # solo il Run 11: definizioni del protocollo e replay esplorativo
```

Dopo il blocco del filtro `cpi` (quello che lancia `tests/test_cpi_lab.py`), aggiungi:

```bash
[ "$FILTRO" = "tutto" ] || [ "$FILTRO" = "quant" ] && \
  run "quant — Run 11: definizioni del protocollo e replay esplorativo (sola lettura)" \
      tests/test_quant_reazione.py
```

Esegui: `cd news_impact_pipeline && ./run_tests.sh quant`
Atteso: `→ quant — …: OK` e `TUTTE LE SUITE VERDI`.

- [ ] **Passo 6: Commit**

```bash
git add news_impact_pipeline/quant_reazione.py news_impact_pipeline/tests/test_quant_reazione.py news_impact_pipeline/run_tests.sh
git commit -m "$(cat <<'EOF'
Run 11a: protocol definitions (sigma60, normal baseline, deviation z, gate, daily vote) with synthetic tests

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Caricatori in sola lettura (ledger, libreria, prezzi)

**File:**
- Modifica: `news_impact_pipeline/quant_reazione.py`, aggiungendo una sezione in coda
- Modifica: `news_impact_pipeline/tests/test_quant_reazione.py`, aggiungendo una classe prima di
  `if __name__`

**Interfacce:**
- Consuma: `sigma`, `reaction`, `baseline`, `deviation_z` e `deviation_hit` (Task 2).
- Produce:
  - `price_loader(conn) -> Callable[[str], pd.Series | None]`. Restituisce la serie delle sedute con
    prezzo valido, oppure `None` se l'asset è assente o la serie è mensile.
  - `ledger_cells(rows: list[dict], prices, proto: dict) -> list[dict]`. Ogni cella ha le chiavi `day`,
    `card`, `asset`, `h`, `med`, `n`, `p25`, `p75`, `uso`, `realized`, `realized_prev`, `z_prev`,
    `normal_median`, `normal_p25`, `normal_p75`, `z` e `hit`; i campi non calcolabili valgono `None`.
  - `library_pairs(episodes: list[dict], prices, proto: dict) -> list[dict]`. Ogni coppia ha le chiavi
    `date`, `theme`, `asset`, `verso` (±1), `r0`, `z0`, `src` (`"kb"` o `"card"`), `r1`, `r3`, `r5` e
    `r10`.

- [ ] **Passo 1: Scrivere i test che falliscono**

In `test_quant_reazione.py`, prima di `if __name__ == "__main__":`, aggiungi:

```python
def row(s, pos=300, **kw):
    d = s.index[pos].date().isoformat()
    r = {"scenario": "base", "registration": "", "uso": "", "ingestion_status": "ok",
         "expected_median": "0.8", "hist_p25": "-0.5", "hist_p75": "1.5", "n_analogues": "16",
         "realized_return": "0.5", "anchor_date": d, "made_date": d, "horizon": "5",
         "card_path": f"{d}/news_01.md", "asset": "AAA"}
    r.update(kw)
    return r


class Dati(unittest.TestCase):
    def setUp(self):
        self.s = series()
        self.p = self.s.to_numpy()
        self.prices = lambda asset: self.s if asset == "AAA" else None

    def test_cella_valida_del_ledger(self):
        (c,) = q.ledger_cells([row(self.s)], self.prices, PROTO)
        base = q.baseline(self.p, 300, 5, 250)
        self.assertAlmostEqual(c["normal_median"], float(np.median(base)))
        self.assertAlmostEqual(c["z"], q.deviation_z(0.8, -0.5, 1.5, 16, c["normal_median"]))
        self.assertEqual(c["hit"], q.deviation_hit(0.8, c["normal_median"], 0.5))
        self.assertAlmostEqual(c["realized_prev"], (self.p[304] / self.p[299] - 1) * 100)
        self.assertAlmostEqual(c["z_prev"], q.reaction(self.p, 299, 60)[1])

    def test_righe_escluse_dal_ledger(self):
        sabato = "2021-02-06"   # non è una seduta della serie sintetica
        rows = [row(self.s, registration="recovered"), row(self.s, scenario="escalation"),
                row(self.s, realized_return=""), row(self.s, uso="ritirata"),
                row(self.s, ingestion_status="quarantine"), row(self.s, asset="ZZZ"),
                row(self.s, anchor_date=sabato)]
        self.assertEqual(q.ledger_cells(rows, self.prices, PROTO), [])

    def test_storia_corta_o_banda_mancante_restano_solo_per_la_misura_1(self):
        corta, senza_banda = q.ledger_cells([row(self.s, pos=100), row(self.s, hist_p25="")], self.prices, PROTO)
        self.assertIsNone(corta["normal_median"]); self.assertIsNone(corta["z"]); self.assertIsNone(corta["hit"])
        self.assertIsNone(senza_banda["z"]); self.assertIsNotNone(senza_banda["hit"])

    def test_coppie_della_libreria(self):
        d = self.s.index[300].date().isoformat()
        ep = lambda date, dirs, src="kb:x/y.md": {"date": date, "theme": "t",
                                                  "directions_by_reference": {"AAA": dirs},
                                                  "direction_sources": {"AAA": [src]}}
        eps = [ep(d, ["pos"]), ep(d, ["pos", "neg"]), ep(d, ["neutral"]),
               ep(self.s.index[395].date().isoformat(), ["neg"]), ep("2019-06-01", ["pos"])]
        (c,) = q.library_pairs(eps, self.prices, PROTO)
        self.assertEqual((c["verso"], c["src"]), (1, "kb"))
        self.assertAlmostEqual(c["z0"], q.reaction(self.p, 300, 60)[1])
        self.assertAlmostEqual(c["r5"], (self.p[305] / self.p[300] - 1) * 100)
        (c,) = q.library_pairs([ep(d, ["neg"], "card:2026-10-03/news_03.md")], self.prices, PROTO)
        self.assertEqual((c["verso"], c["src"]), (-1, "card"))

    def test_serie_mensili_assenti_o_con_buchi(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE prices (ticker TEXT, date TEXT, close REAL, adj_close REAL)")
        for i, d in enumerate(pd.bdate_range("2020-01-01", periods=100)):
            conn.execute("INSERT INTO prices VALUES ('DAY', ?, ?, ?)", (d.date().isoformat(), 100 + i, None if i == 7 else 100 + i))
        conn.execute("INSERT INTO prices VALUES ('DAY', '2020-06-01', NULL, NULL)")
        for d in pd.date_range("2015-01-31", periods=60, freq="ME"):
            conn.execute("INSERT INTO prices VALUES ('MON', ?, 1.5, NULL)", (d.date().isoformat(),))
        prices = q.price_loader(conn)
        self.assertEqual(len(prices("DAY")), 100)      # adj mancante → close; riga tutta NULL esclusa
        self.assertIsNone(prices("MON"))
        self.assertIsNone(prices("NONE"))
```

Note per chi esegue:
- `series()` copre 400 giorni lavorativi dal 2020-01-01 (fino a metà 2021). Il 2021-02-06 è un sabato,
  quindi non è una seduta.
- Con l'ancora a 395 manca T+10, quindi la coppia è esclusa.
- Il 2019-06-01 cade prima della serie, quindi l'ancora sarebbe a più di 4 giorni e la coppia è esclusa.

- [ ] **Passo 2: Verificare che falliscano**

Esegui: `news_impact_pipeline/venv/bin/python news_impact_pipeline/tests/test_quant_reazione.py -v`
Atteso: i 5 test di `Dati` in errore con `AttributeError: module 'quant_reazione' has no attribute 'ledger_cells'`
(oppure `library_pairs` o `price_loader`); i 10 di `Definizioni` restano verdi.

- [ ] **Passo 3: Scrivere i caricatori**

In coda a `quant_reazione.py` aggiungi:

```python
# --- dati (sola lettura) ----------------------------------------------------------------------

def price_loader(conn):
    """prices(asset) → serie delle sedute con prezzo valido; None se assente o mensile."""
    @lru_cache(maxsize=None)
    def prices(asset: str) -> pd.Series | None:
        try:
            s = load_price_series(conn, asset).dropna()
        except ValueError:
            return None
        return None if detect_monthly_data(s) else s
    return prices


def _num(x: str) -> float | None:
    return float(x) if x not in ("", None) else None


def ledger_cells(rows: list[dict], prices, proto: dict) -> list[dict]:
    """Celle del ledger: scenario base, registrazione originale, realizzato congelato e prezzi validi."""
    sw, bw = proto["sigma_window_sessions"], proto["baseline_window_sessions"]
    out = []
    for r in rows:
        if (r["scenario"] != "base" or r["registration"] == "recovered" or r["uso"] == "ritirata"
                or r["ingestion_status"] == "quarantine" or not r["expected_median"]
                or not r["realized_return"] or not r["anchor_date"]):
            continue
        s = prices(r["asset"])
        if s is None:
            continue
        anchor = pd.Timestamp(r["anchor_date"])
        a = int(s.index.searchsorted(anchor))
        if a >= len(s) or s.index[a] != anchor:
            continue                                   # ancora congelata assente dalla serie di oggi
        p, h = s.to_numpy(), int(r["horizon"])
        base = baseline(p, a, h, bw)
        prev = reaction(p, a - 1, sw)
        c = {"day": r["made_date"], "card": r["card_path"], "asset": r["asset"], "h": h,
             "med": float(r["expected_median"]), "n": int(r["n_analogues"] or 0),
             "p25": _num(r["hist_p25"]), "p75": _num(r["hist_p75"]), "uso": r["uso"],
             "realized": float(r["realized_return"]),
             "realized_prev": (p[a - 1 + h] / p[a - 1] - 1) * 100 if 1 <= a <= len(p) - h and p[a - 1] > 0 else None,
             "z_prev": prev[1] if prev else None,
             "normal_median": float(np.median(base)) if base is not None else None,
             "normal_p25": float(np.percentile(base, 25)) if base is not None else None,
             "normal_p75": float(np.percentile(base, 75)) if base is not None else None}
        ok = None not in (c["p25"], c["p75"], c["normal_median"])
        c["z"] = deviation_z(c["med"], c["p25"], c["p75"], c["n"], c["normal_median"]) if ok else None
        c["hit"] = deviation_hit(c["med"], c["normal_median"], c["realized"]) if c["normal_median"] is not None else None
        out.append(c)
    return out


def library_pairs(episodes: list[dict], prices, proto: dict) -> list[dict]:
    """Coppie (data, asset) con verso univoco pos/neg: reazione del giorno-ancora e seguito T+h."""
    sw = proto["sigma_window_sessions"]
    out = []
    for e in episodes:
        for asset, dirs in (e.get("directions_by_reference") or {}).items():
            if len(set(dirs)) != 1 or dirs[0] not in ("pos", "neg"):
                continue
            s = prices(asset)
            if s is None:
                continue
            d = pd.Timestamp(e["date"])
            a = int(s.index.searchsorted(d))
            if a + max(HORIZONS) >= len(s) or s.index[a] - d > pd.Timedelta(days=4):
                continue                               # seguito non osservabile o ancora troppo lontana
            p = s.to_numpy()
            rz = reaction(p, a, sw)
            if rz is None:
                continue
            srcs = (e.get("direction_sources") or {}).get(asset, [])
            out.append({"date": e["date"], "theme": e["theme"], "asset": asset,
                        "verso": 1 if dirs[0] == "pos" else -1, "r0": rz[0], "z0": rz[1],
                        "src": "kb" if any(str(x).startswith("kb:") for x in srcs) else "card",
                        **{f"r{h}": (p[a + h] / p[a] - 1) * 100 for h in HORIZONS}})
    return out
```

Perché il realizzato viene dal ledger e non dai prezzi:
- È il valore **congelato** con cui il sistema giudica davvero, ed è lo stesso che userà il Run 11e.
- I prezzi servono solo per σ, baseline e la variante con ancora in a−1.

- [ ] **Passo 4: Verificare che passino**

Esegui: `news_impact_pipeline/venv/bin/python -W error news_impact_pipeline/tests/test_quant_reazione.py -v`
Atteso: `Ran 15 tests` … `OK`.

- [ ] **Passo 5: Commit**

```bash
git add news_impact_pipeline/quant_reazione.py news_impact_pipeline/tests/test_quant_reazione.py
git commit -m "$(cat <<'EOF'
Run 11a: read-only loaders for ledger cells, library pairs and daily price series

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Le misure 1–4, il comando `replay` e la documentazione

**File:**
- Modifica: `news_impact_pipeline/quant_reazione.py`, aggiungendo due sezioni in coda
- Modifica: `news_impact_pipeline/tests/test_quant_reazione.py`, aggiungendo la classe `Replay`
- Modifica: `PIANO_REVISIONE_PIPELINE.md`, nella sezione Run 11: la riga «Rieseguibile» e la spunta
  dell'11a
- Modifica: `MEMORY.md`, aggiungendo il nuovo filone in coda

**Interfacce:**
- Consuma: tutto quanto prodotto dai Task 2 e 3.
- Produce: `main(argv=None) -> int`, con il sottocomando unico `replay`, e `replay() -> str`, che
  restituisce il markdown stampato.

- [ ] **Passo 1: Scrivere il test che fallisce**

In `test_quant_reazione.py`, prima di `if __name__ == "__main__":`, aggiungi:

```python
class Replay(unittest.TestCase):
    @unittest.skipUnless(Path(q.DB_PATH).exists(), "DB prezzi assente")
    def test_replay_sui_dati_del_repo_in_sola_lettura(self):
        prima = hashlib.sha256(q.LEDGER_PATH.read_bytes()).hexdigest()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(q.main(["replay"]), 0)
        out = buf.getvalue()
        self.assertIn("ESPLORATIVO", out)
        for n in range(1, 5):
            self.assertIn(f"## {n}.", out)
        self.assertIsNone(re.search(r"\bnan\b", out))
        self.assertEqual(hashlib.sha256(q.LEDGER_PATH.read_bytes()).hexdigest(), prima)
```

- [ ] **Passo 2: Verificare che fallisca**

Esegui: `news_impact_pipeline/venv/bin/python news_impact_pipeline/tests/test_quant_reazione.py -v`
Atteso: `test_replay_sui_dati_del_repo_in_sola_lettura` in errore con `AttributeError: … has no attribute 'main'`.

- [ ] **Passo 3: Scrivere le misure e il comando**

In coda a `quant_reazione.py` aggiungi:

```python
# --- misure ----------------------------------------------------------------------------------

def sign_hit(pred: pd.Series, real: pd.Series) -> tuple[float, int]:
    """Quota di segno indovinato, escluse le chiamate piatte (|pred| < FLAT) e i realizzati nulli."""
    m = (pred.abs() >= FLAT_THRESHOLD) & real.notna() & (real != 0)
    return float((np.sign(pred[m]) == np.sign(real[m])).mean()), int(m.sum())


def ic_within(df: pd.DataFrame, x: str, y: str, min_n: int = 15) -> tuple[float, int]:
    """Correlazione di rango dentro asset×orizzonte, media pesata per numerosità."""
    g = [(len(v), spearman(v[x], v[y])) for _, v in df.groupby(["asset", "h"]) if len(v) >= min_n]
    g = [(n, r) for n, r in g if not math.isnan(r)]
    if not g:
        return float("nan"), 0
    return float(np.average([r for _, r in g], weights=[n for n, _ in g])), len(g)


def misura_1(cells: list[dict]) -> list[str]:
    df = pd.DataFrame(cells)
    out = ["## 1. Il segno del seguito: mediana del pool contro realizzato",
           f"celle {len(df)} · schede {df.card.nunique()} · giorni {df.day.nunique()} · asset {df.asset.nunique()}",
           "", "| Orizzonte | N | segno indovinato | realizzato su | ancora a−1 |", "|---|---|---|---|---|"]
    for h, g in df.groupby("h"):
        hit, n = sign_hit(g.med, g.realized)
        prev, _ = sign_hit(g.med, g.realized_prev.astype(float))
        up = (g.realized[(g.med.abs() >= FLAT_THRESHOLD) & (g.realized != 0)] > 0).mean()
        out.append(f"| T+{h} | {n} | {hit:.1%} | {up:.0%} | {prev:.1%} |")
    ic, k = ic_within(df, "med", "realized")
    out += ["", f"IC dentro asset×orizzonte (gruppi ≥ 15 celle: {k}): {ic:+.3f}", "",
            "Per numerosità del pool:"]
    df["nb"] = pd.cut(df.n, [0, 9, 19, 29, 10_000], labels=["<10", "10-19", "20-29", "30+"])
    for nb, g in df.groupby("nb", observed=True):
        hit, n = sign_hit(g.med, g.realized)
        out.append(f"- N {nb}: {hit:.1%} (celle {n}, giorni {g.day.nunique()})")
    big = df[df.z_prev.astype(float).abs() >= 1.5]
    cont = (np.sign(big.z_prev.astype(float)) == np.sign(big.realized))[big.realized != 0].mean()
    out += ["", f"Mossa già avvenuta (ultima seduta chiusa, |z| ≥ 1,5): il seguito continua nel {cont:.1%} "
                f"dei casi (celle {len(big)}, giorni {big.day.nunique()})"]
    return out


def misura_2(cells: list[dict]) -> list[str]:
    b = pd.DataFrame([c for c in cells if c["p25"] is not None and c["normal_median"] is not None])
    lo, hi = b[["p25", "p75"]].min(axis=1), b[["p25", "p75"]].max(axis=1)
    b["in_pool"] = (b.realized >= lo) & (b.realized <= hi)
    b["in_norm"] = (b.realized >= b.normal_p25) & (b.realized <= b.normal_p75)
    b["w_pool"], b["w_norm"] = hi - lo, b.normal_p75 - b.normal_p25
    out = ["## 2. Il pool contro il comportamento normale dell'asset (250 sedute prima)",
           f"celle {len(b)} · giorni {b.day.nunique()} (atteso per una banda p25–p75 tarata: 50%)", "",
           "| Orizzonte | N | copertura pool | copertura normale | ampiezza pool | ampiezza normale |",
           "|---|---|---|---|---|---|"]
    for h, g in b.groupby("h"):
        out.append(f"| T+{h} | {len(g)} | {g.in_pool.mean():.0%} | {g.in_norm.mean():.0%} | "
                   f"{g.w_pool.median():.2f} pp | {g.w_norm.median():.2f} pp |")
    out += ["", "Errore assoluto medio del realizzato contro:"]
    for lab, ref in (("mediana del pool", b.med), ("mediana normale", b.normal_median), ("zero", 0.0)):
        out.append(f"- {lab}: {(b.realized - ref).abs().mean():.3f} pp")
    return out


def misura_3(pairs: list[dict], any_day: float) -> list[str]:
    d = pd.DataFrame(pairs)
    out = ["## 3. Il giorno della notizia: libreria episodi con verso univoco",
           f"coppie (data, asset) {len(d)} · date {d.date.nunique()} · asset {d.asset.nunique()}",
           f"|z0| mediano del giorno-ancora: {d.z0.abs().median():.2f} — giorno qualsiasi: "
           f"{ANY_DAY_ABS_Z} in teoria, {any_day:.2f} misurato sugli stessi asset", "",
           "| Fonte del verso | N | giorno-ancora | T+1 | T+3 | T+5 | T+10 |", "|---|---|---|---|---|---|---|"]
    for lab, g in (("tutte", d), ("research KB", d[d.src == "kb"]), ("schede", d[d.src == "card"])):
        cols = ["r0"] + [f"r{h}" for h in HORIZONS]
        rates = [(np.sign(g[c]) == g.verso)[g[c] != 0].mean() for c in cols]
        out.append(f"| {lab} | {len(g)} | " + " | ".join(f"{x:.0%}" for x in rates) + " |")
    return out


def _votes_line(label: str, cells: list[dict]) -> str:
    t = vote_test(daily_votes(cells))
    return (f"- {label}: giorni sopra {t['above']}, sotto {t['below']}, pari {t['ties']} "
            f"(p unilaterale {t['p']:.3f}; celle {sum(c['hit'] is not None for c in cells)})")


def misura_4(cells: list[dict], proto: dict) -> list[str]:
    gate, hp = proto["gate"], proto["primary_horizon_sessions"]
    b = [c for c in cells if c["z"] is not None and c["hit"] is not None]
    exp = [c for c in b if c["n"] >= EXPLORATIVE_N_MIN]
    out = ["## 4. Il cancello: la mediana del pool lontana dal normale",
           f"Definizione esplorativa (N ≥ {EXPLORATIVE_N_MIN}, tutti gli orizzonti) — celle {len(exp)}", "",
           "| abs(z) | celle | giorni | scostamento indovinato | segno della mediana |", "|---|---|---|---|---|"]
    for lo, hi in ((0, 1), (1, 2), (2, 3), (3, math.inf)):
        g = pd.DataFrame([c for c in exp if lo <= abs(c["z"]) < hi])
        if g.empty:
            continue
        sh, _ = sign_hit(g.med, g.realized)
        lab = f"≥ {lo}" if hi == math.inf else f"{lo}–{hi}"
        out.append(f"| {lab} | {len(g)} | {g.day.nunique()} | {g.hit.mean():.1%} | {sh:.1%} |")
    hi2 = [c for c in exp if abs(c["z"]) >= 2]
    out += ["", "Un voto per giorno:", _votes_line("abs(z) ≥ 2", hi2),
            _votes_line("abs(z) < 1", [c for c in exp if abs(c["z"]) < 1])]
    for lab, part in (("prima del " + SPLIT_DAY, [c for c in hi2 if c["day"] < SPLIT_DAY]),
                      ("dal " + SPLIT_DAY, [c for c in hi2 if c["day"] >= SPLIT_DAY])):
        if part:
            out.append(f"  - {lab}: {np.mean([c['hit'] for c in part]):.1%} "
                       f"(celle {len(part)}, giorni {len({c['day'] for c in part})})")
    prim = [c for c in b if c["h"] == hp]
    strict = [c for c in prim if passes_gate(c["z"], c["n"], gate)]
    days_all = len({c["day"] for c in cells if c["h"] == hp})
    v = daily_votes(strict)
    out += ["", f"Regola del protocollo {proto['protocol_version']} (abs(z) ≥ {gate['z_min']}, "
                f"N ≥ {gate['n_min']}, T+{hp}) sui dati già visti:",
            f"- giorni con almeno una cella sopra cancello: {len(v)} su {days_all}",
            _votes_line("sopra cancello", strict),
            f"- autocorrelazione lag-1 dei voti: {lag1_autocorr(v):+.2f}",
            _votes_line("controllo abs(z) < 1, stessa N", [c for c in prim if abs(c["z"]) < 1 and c["n"] >= gate["n_min"]]),
            _votes_line("solo tabelle [previsione]", [c for c in strict if c["uso"] == "previsione"])]
    return out


# --- comando ---------------------------------------------------------------------------------

def replay() -> str:
    proto = load_protocol()
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        prices = price_loader(conn)
        with open(LEDGER_PATH, newline="", encoding="utf-8") as f:
            cells = ledger_cells(list(csv.DictReader(f)), prices, proto)
        episodes = yaml.safe_load(LIB_PATH.read_text(encoding="utf-8"))["episodes"]
        pairs = library_pairs(episodes, prices, proto)
        assets = sorted({p["asset"] for p in pairs})
        any_day = float(pd.concat([abs_z_all_sessions(prices(a), proto["sigma_window_sessions"])
                                   for a in assets]).median())
        lines = [f"# Replay esplorativo — Run 11 «reazione, non seguito» ({date.today()})",
                 f"⚠ ESPLORATIVO: dati già visti, non conta come prova. La prova è prospettica "
                 f"(protocollo {proto['protocol_version']}, Run 11e).", "",
                 *misura_1(cells), "", *misura_2(cells), "", *misura_3(pairs, any_day), "",
                 *misura_4(cells, proto)]
    finally:
        conn.close()
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("replay", help="misure esplorative 1–4 del Run 11 (sola lettura)")
    ap.parse_args(argv)
    print(replay())
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Il sottocomando `replay` serve a non dover cambiare il comando quando il Run 11e aggiungerà la
valutazione prospettica.

- [ ] **Passo 4: Verificare che passino, poi la suite completa**

Esegui:
```bash
news_impact_pipeline/venv/bin/python -W error news_impact_pipeline/tests/test_quant_reazione.py -v
cd news_impact_pipeline && ./run_tests.sh
```
Atteso: `Ran 16 tests` … `OK` (circa 5 s), poi `TUTTE LE SUITE VERDI`. Se fallisce una suite diversa
da `quant`, nessun file che testa è stato toccato qui: riportala al maintainer come problema preesistente,
non correggerla in questo run. Non usare `git stash`: ci sono modifiche del maintainer non committate.

- [ ] **Passo 5: Lanciare il replay e confrontarlo con la fotografia della spec**

Esegui: `news_impact_pipeline/venv/bin/python news_impact_pipeline/quant_reazione.py replay`

Atteso sul ledger del 2026-10-07; dopo la valutazione del lunedì i numeri si spostano di poco:

| Misura | Valore atteso |
|---|---|
| 1 | segno indovinato fra 49% e 52% a ogni orizzonte; IC ≈ +0,01 |
| 2 | copertura del pool 51–53%; copertura normale 52/52/48/41% (T+1…T+10); errore assoluto: pool > normale > zero |
| 3 | 874 coppie; \|z0\| mediano ≈ 1,09 contro 0,60 misurato; giorno-ancora ≈ 74%, T+1 ≈ 58% |
| 4 | fasce di \|z\| crescenti, da ~50,6% (0–1) a ~60% (≥ 3) |
| 4, regola del protocollo | 47 giorni su 63; sopra 34, sotto 11, pari 2; controllo \|z\| < 1 ≈ 21/20 |

**Condizione di arresto:** se la regola del protocollo dà giorni sopra ≤ giorni sotto, oppure se la misura
1 si allontana dal 50% di più di 3 punti, **fermati e riporta al maintainer** prima del Passo 6. In quel
caso la premessa del Run 11 va rivista.

- [ ] **Passo 6: Aggiornare `PIANO_REVISIONE_PIPELINE.md`**

Nella sezione Run 11, dopo il punto 5 di «Il problema, misurato» (che finisce con «…non va trasformato in
uno).») e prima di «### Obiettivo e criteri di successo», aggiungi questo paragrafo. Se l'output del
Passo 5 è diverso, sostituisci i numeri con quelli dell'output:

```markdown
**Rieseguibile** (Run 11a, 2026-10-07): `news_impact_pipeline/venv/bin/python news_impact_pipeline/quant_reazione.py replay`
— misure 1–4 con le definizioni del protocollo 1.0.0 e il realizzato congelato del ledger; esplorativo.
Rispetto alla fotografia sopra, i punti 1, 3 e 4 sono confermati; sul punto 2 la banda «normale» copre
il 41% a T+10 (il pool il 51%), quindi sugli orizzonti lunghi il pool è tarato meglio.
```

Poi, nella «Sequenza dei run», cambia `- [ ] **11a — Protocollo + replay esplorativo.**` in
`- [x] **11a — Protocollo + replay esplorativo.**` e aggiungi alla fine del punto:
` Fatto il 2026-10-07: protocollo nel commit <hash>.` Ricava l'hash con
`git log --format=%h -1 -- experiments/quant_reazione/protocol-1.0.0.json`.

- [ ] **Passo 7: Aggiungere il filone in `MEMORY.md`**

In coda a `MEMORY.md` aggiungi (il filone resta sotto le 10 righe):

```markdown

---

## Quantitativo «reazione, non seguito» (Run 11)

- **Stato** — 11a chiuso il 2026-10-07: protocollo `experiments/quant_reazione/protocol-1.0.0.json` registrato prima del codice; misure esplorative con `news_impact_pipeline/quant_reazione.py replay`.
- **Deciso** — (07/10) il segno del seguito T+h non ha informazione (~50%); l'informazione sta nella reazione del giorno della notizia. Unico segnale da confermare: il cancello |z| ≥ 2 e N ≥ 10 sulla distanza fra mediana del pool e mediana normale (T+5, un voto per giorno, decisione a 60 giorni non pari dal go-live).
- **Prossimo passo** — Run 11b: reazione, baseline e cancello in `event_study.py`, con il comportamento di default invariato. Le definizioni di `quant_reazione.py` sono il riferimento da riusare, non da riscrivere.

Spec e sequenza: [PIANO_REVISIONE_PIPELINE.md](PIANO_REVISIONE_PIPELINE.md) (Run 11)
```

- [ ] **Passo 8: Commit**

```bash
git add news_impact_pipeline/quant_reazione.py news_impact_pipeline/tests/test_quant_reazione.py PIANO_REVISIONE_PIPELINE.md MEMORY.md
git commit -m "$(cat <<'EOF'
Run 11a: re-runnable exploratory replay of measures 1-4, labelled as not evidence

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
git log --oneline -4   # protocollo, definizioni, caricatori, replay: in quest'ordine
git status --short     # le modifiche del maintainer elencate nei vincoli devono essere ancora lì, non committate
```
