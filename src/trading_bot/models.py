from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Position:
    units: float = 0.0
    avg_price: float = 0.0


@dataclass
class AccountState:
    cash: float
    equity: float
    peak_equity: float
    position: Position
