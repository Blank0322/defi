# DeFi Risk Radar

A lightweight DeFi monitoring scaffold for internship-ready research traces.

## What it tracks (MVP)
- protocol-level TVL trend
- APY dispersion and sudden jumps
- concentration risk proxy (top protocol share)
- simple risk score for daily watchlist
- time-series regime detection (normal / liquidity-shock / yield-shock / stress)

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_radar.py --mock
python scripts/run_regime_report.py --protocol MockLST
```
