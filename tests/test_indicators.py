from trading_bot.indicators import atr, ema, rsi


def test_ema_tracks_last_value_directionally():
    values = [1, 2, 3, 4, 5]
    out = ema(values, 3)
    assert 3.5 < out < 5.1


def test_rsi_bounds():
    rising = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    val = rsi(rising, 14)
    assert 0 <= val <= 100


def test_atr_non_negative():
    highs = [10, 11, 12, 13]
    lows = [9, 10, 11, 12]
    closes = [9.5, 10.5, 11.5, 12.5]
    assert atr(highs, lows, closes, 3) >= 0
