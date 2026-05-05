from __future__ import annotations

import csv
from pathlib import Path

from .models import Candle


def load_candles(path: str | Path) -> list[Candle]:
    rows: list[Candle] = []
    with Path(path).open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                Candle(
                    timestamp=row["timestamp"],
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0.0)),
                )
            )
    return rows
