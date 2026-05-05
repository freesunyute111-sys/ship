from __future__ import annotations

from .config import StrategyConfig
from .indicators import atr, ema, rsi


class MultiFactorStrategy:
    def __init__(self, config: StrategyConfig):
        self.config = config

    def signal(self, closes: list[float], highs: list[float], lows: list[float]) -> float:
        if len(closes) < max(self.config.ema_slow, self.config.rsi_period) + 2:
            return 0.0

        fast = ema(closes, self.config.ema_fast)
        slow = ema(closes, self.config.ema_slow)
        trend = (fast - slow) / max(slow, 1e-9)

        rsi_value = rsi(closes, self.config.rsi_period)
        mean_rev = (50.0 - rsi_value) / 50.0

        atr_value = atr(highs, lows, closes, self.config.atr_period)
        vol = atr_value / max(closes[-1], 1e-9)
        vol_regime = 1.0 if vol >= self.config.volatility_floor else 0.25

        score = (0.7 * trend + 0.3 * mean_rev) * vol_regime
        return max(min(score * 4.0, 1.0), -1.0)
