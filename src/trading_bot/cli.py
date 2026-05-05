from __future__ import annotations

import argparse

from .bot import TradingBot
from .io import load_candles


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced Trading Bot backtest runner")
    parser.add_argument("--candles", required=True, help="Path to OHLCV CSV")
    args = parser.parse_args()

    candles = load_candles(args.candles)
    bot = TradingBot()
    result = bot.backtest(candles)

    print("Backtest complete")
    print(f"Final equity : {result.final_equity:,.2f}")
    print(f"Total return : {result.total_return:.2%}")
    print(f"Max drawdown : {result.max_drawdown:.2%}")
    print(f"Sharpe-like  : {result.sharpe_like:.2f}")
    print(f"Trades       : {result.trades}")


if __name__ == "__main__":
    main()
