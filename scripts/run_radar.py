from __future__ import annotations

import argparse

from defi_radar.models import ProtocolPoint
from defi_radar.scoring import score


def mock_points() -> list[ProtocolPoint]:
    return [
        ProtocolPoint("LendX", "ethereum", 1_200_000_000, 0.12),
        ProtocolPoint("YieldY", "ethereum", 2_300_000_000, 0.95),
        ProtocolPoint("StableZ", "arbitrum", 420_000_000, 0.08),
        ProtocolPoint("PerpQ", "base", 180_000_000, 0.35),
    ]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mock", action="store_true")
    _ = p.parse_args()

    pts = mock_points()
    signals = score(pts)

    print("DeFi Risk Radar")
    for s in signals:
        print(f"- {s.protocol}: score={s.risk_score:.2f} | {s.reason}")


if __name__ == "__main__":
    main()
