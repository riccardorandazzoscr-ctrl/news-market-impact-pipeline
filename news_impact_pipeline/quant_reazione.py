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
