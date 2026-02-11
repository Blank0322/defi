from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RegimePoint:
    protocol: str
    tvl_z: float | None
    apy_z: float | None
    is_tvl_shock: bool
    is_apy_shock: bool
    regime: str


def _z_last(series: pd.Series, lookback: int = 30) -> float | None:
    s = series.dropna()
    if len(s) < max(10, lookback):
        return None
    w = s.iloc[-lookback:]
    std = float(w.std(ddof=1))
    if std <= 1e-12:
        return None
    return float((w.iloc[-1] - w.mean()) / std)


def detect_regime(df: pd.DataFrame, *, tvl_z_th: float = 2.0, apy_z_th: float = 2.0) -> RegimePoint:
    """Detect protocol regime from time-series snapshot.

    Required columns:
    - ts
    - protocol
    - tvl_usd
    - apy
    """
    if df.empty:
        raise ValueError("empty frame")

    protocol = str(df["protocol"].iloc[-1])
    tvl_z = _z_last(df["tvl_usd"])
    apy_z = _z_last(df["apy"])

    tvl_shock = (tvl_z is not None) and (abs(tvl_z) >= tvl_z_th)
    apy_shock = (apy_z is not None) and (abs(apy_z) >= apy_z_th)

    if tvl_shock and apy_shock:
        regime = "stress"
    elif apy_shock:
        regime = "yield-shock"
    elif tvl_shock:
        regime = "liquidity-shock"
    else:
        regime = "normal"

    return RegimePoint(
        protocol=protocol,
        tvl_z=tvl_z,
        apy_z=apy_z,
        is_tvl_shock=tvl_shock,
        is_apy_shock=apy_shock,
        regime=regime,
    )
