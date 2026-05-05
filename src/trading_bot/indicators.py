from __future__ import annotations

from math import fabs


def sma(values: list[float], period: int) -> float:
    if len(values) < period or period <= 0:
        return values[-1]
    window = values[-period:]
    return sum(window) / period


def ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    if period <= 1:
        return values[-1]
    alpha = 2 / (period + 1)
    out = values[0]
    for v in values[1:]:
        out = alpha * v + (1 - alpha) * out
    return out


def rsi(values: list[float], period: int) -> float:
    if len(values) <= period:
        return 50.0
    gains: list[float] = []
    losses: list[float] = []
    for i in range(-period, 0):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(highs: list[float], lows: list[float], closes: list[float], period: int) -> float:
    if not highs or not lows or not closes:
        return 0.0
    trs: list[float] = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            fabs(highs[i] - closes[i - 1]),
            fabs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if not trs:
        return highs[-1] - lows[-1]
    if len(trs) < period:
        return sum(trs) / len(trs)
    return sum(trs[-period:]) / period
