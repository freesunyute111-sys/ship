# Advanced Trading Bot

A modular algorithmic trading bot with:

- Multi-factor signal engine (momentum + mean-reversion + volatility filter)
- Position sizing using volatility targeting
- Risk controls (max drawdown guard, stop loss, take profit, exposure caps)
- Event-driven paper execution simulator
- Backtesting utility with summary metrics

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m trading_bot.cli --candles data/sample_candles.csv
```

## Run tests

```bash
pytest -q
```

## Strategy overview

The strategy computes:

- Fast/slow EMA spread for trend/momentum
- RSI for mean-reversion pressure
- ATR-normalized volatility regime filter

Signals are combined into a confidence score in `[-1, 1]`, then translated into target position size with risk and portfolio constraints.
