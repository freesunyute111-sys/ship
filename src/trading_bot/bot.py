from __future__ import annotations

import math
from dataclasses import dataclass

from .config import BotConfig
from .execution import PaperBroker
from .models import AccountState, Candle, Position
from .risk import RiskManager
from .strategy import MultiFactorStrategy


@dataclass
class BacktestResult:
    final_equity: float
    total_return: float
    max_drawdown: float
    sharpe_like: float
    trades: int


class TradingBot:
    def __init__(self, config: BotConfig | None = None):
        self.config = config or BotConfig()
        self.strategy = MultiFactorStrategy(self.config.strategy)
        self.risk = RiskManager(self.config.risk)
        self.broker = PaperBroker(self.config.fee_bps)

    def backtest(self, candles: list[Candle]) -> BacktestResult:
        closes: list[float] = []
        highs: list[float] = []
        lows: list[float] = []
        returns: list[float] = []

        account = AccountState(
            cash=self.config.initial_cash,
            equity=self.config.initial_cash,
            peak_equity=self.config.initial_cash,
            position=Position(),
        )

        trades = 0
        prev_equity = account.equity

        for candle in candles:
            closes.append(candle.close)
            highs.append(candle.high)
            lows.append(candle.low)

            account.equity = account.cash + account.position.units * candle.close
            account.peak_equity = max(account.peak_equity, account.equity)

            if self.risk.drawdown_breached(account):
                if account.position.units != 0:
                    self.broker.flatten(account, candle.close)
                    trades += 1
                continue

            if self.risk.stop_or_take_profit(account, candle.close):
                self.broker.flatten(account, candle.close)
                trades += 1

            signal = self.strategy.signal(closes, highs, lows)
            realized_vol = self._realized_vol(closes)
            target = self.risk.target_fraction(signal, realized_vol)

            before = account.position.units
            self.broker.rebalance_to_fraction(account, candle.close, target)
            if before != account.position.units:
                trades += 1

            step_return = (account.equity - prev_equity) / max(prev_equity, 1e-9)
            returns.append(step_return)
            prev_equity = account.equity

        total_return = (account.equity / self.config.initial_cash) - 1
        max_dd = 1 - (account.equity / account.peak_equity if account.peak_equity else 1.0)
        sharpe = self._sharpe_like(returns)

        return BacktestResult(
            final_equity=account.equity,
            total_return=total_return,
            max_drawdown=max_dd,
            sharpe_like=sharpe,
            trades=trades,
        )

    @staticmethod
    def _realized_vol(closes: list[float], period: int = 20) -> float:
        if len(closes) < period + 1:
            return 0.0
        rets = []
        for i in range(-period, 0):
            rets.append((closes[i] - closes[i - 1]) / max(closes[i - 1], 1e-9))
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / len(rets)
        return math.sqrt(var)

    @staticmethod
    def _sharpe_like(returns: list[float]) -> float:
        if len(returns) < 2:
            return 0.0
        mean = sum(returns) / len(returns)
        var = sum((r - mean) ** 2 for r in returns) / len(returns)
        std = math.sqrt(var)
        if std == 0:
            return 0.0
        return (mean / std) * math.sqrt(252)
