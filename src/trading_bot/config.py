from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:
    ema_fast: int = 12
    ema_slow: int = 26
    rsi_period: int = 14
    atr_period: int = 14
    volatility_floor: float = 0.002


@dataclass(frozen=True)
class RiskConfig:
    max_gross_exposure: float = 1.0
    max_drawdown: float = 0.20
    stop_loss_pct: float = 0.03
    take_profit_pct: float = 0.06
    vol_target: float = 0.10


@dataclass(frozen=True)
class BotConfig:
    initial_cash: float = 100_000.0
    fee_bps: float = 1.0
    strategy: StrategyConfig = StrategyConfig()
    risk: RiskConfig = RiskConfig()
