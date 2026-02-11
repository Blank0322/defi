from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProtocolPoint:
    protocol: str
    chain: str
    tvl_usd: float
    apy: float | None = None


@dataclass(frozen=True)
class RiskSignal:
    protocol: str
    risk_score: float
    reason: str
