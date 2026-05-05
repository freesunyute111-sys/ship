from trading_bot.bot import TradingBot
from trading_bot.io import load_candles


def test_backtest_runs_on_sample_data():
    candles = load_candles("data/sample_candles.csv")
    bot = TradingBot()
    result = bot.backtest(candles)

    assert result.final_equity > 0
    assert -1.0 < result.total_return < 2.0
    assert 0.0 <= result.max_drawdown <= 1.0
    assert result.trades >= 0
