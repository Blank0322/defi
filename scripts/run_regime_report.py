from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from defi_radar.timeseries import detect_regime


def make_mock(protocol: str, n: int = 120) -> pd.DataFrame:
    ts0 = datetime.utcnow() - timedelta(hours=n)
    tvl = 500_000_000.0
    apy = 0.09
    rows = []

    rng = np.random.default_rng(42)
    for i in range(n):
        tvl *= 1 + rng.normal(0.0002, 0.002)
        apy = max(0.0, apy + rng.normal(0.0, 0.002))

        # inject one synthetic shock near the end
        if i == n - 3:
            tvl *= 0.84
            apy *= 1.55

        rows.append(
            {
                "ts": (ts0 + timedelta(hours=i)).isoformat(),
                "protocol": protocol,
                "tvl_usd": tvl,
                "apy": apy,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--protocol", default="MockLST")
    p.add_argument("--csv", help="Optional csv with ts,protocol,tvl_usd,apy")
    p.add_argument("--out", default="output/regime_report.csv")
    args = p.parse_args()

    if args.csv:
        df = pd.read_csv(args.csv)
    else:
        df = make_mock(args.protocol)

    rp = detect_regime(df)

    report = pd.DataFrame(
        [
            {
                "protocol": rp.protocol,
                "tvl_z": rp.tvl_z,
                "apy_z": rp.apy_z,
                "is_tvl_shock": rp.is_tvl_shock,
                "is_apy_shock": rp.is_apy_shock,
                "regime": rp.regime,
            }
        ]
    )

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    report.to_csv(args.out, index=False)

    print("DeFi regime report")
    print(report.to_string(index=False))
    print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
