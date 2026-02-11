from __future__ import annotations

from collections import defaultdict

from .models import ProtocolPoint, RiskSignal


def score(points: list[ProtocolPoint]) -> list[RiskSignal]:
    total_tvl = sum(max(p.tvl_usd, 0) for p in points) or 1.0
    out: list[RiskSignal] = []

    chain_tvl = defaultdict(float)
    for p in points:
        chain_tvl[p.chain] += max(p.tvl_usd, 0)

    for p in points:
        s = 0.0
        reasons = []

        # concentration proxy
        share = max(p.tvl_usd, 0) / total_tvl
        if share > 0.25:
            s += min(3.0, share / 0.25)
            reasons.append(f"high tvl share ({share:.1%})")

        # chain concentration proxy
        cshare = chain_tvl[p.chain] / total_tvl
        if cshare > 0.6:
            s += 1.0
            reasons.append(f"chain concentration ({p.chain} {cshare:.1%})")

        # APY anomaly proxy
        if p.apy is not None and p.apy > 0.8:
            s += 2.0
            reasons.append(f"extreme APY ({p.apy:.0%})")

        if s > 0:
            out.append(RiskSignal(protocol=p.protocol, risk_score=s, reason=", ".join(reasons)))

    return sorted(out, key=lambda x: x.risk_score, reverse=True)
