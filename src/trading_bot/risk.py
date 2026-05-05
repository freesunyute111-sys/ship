from __future__ import annotations

from .config import RiskConfig
from .models import AccountState


class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config

    def drawdown_breached(self, account: AccountState) -> bool:
        if account.peak_equity <= 0:
            return False
        drawdown = 1 - (account.equity / account.peak_equity)
        return drawdown >= self.config.max_drawdown

    def stop_or_take_profit(self, account: AccountState, price: float) -> bool:
        if account.position.units == 0 or account.position.avg_price == 0:
            return False
        pnl_pct = (price - account.position.avg_price) / account.position.avg_price
        if account.position.units < 0:
            pnl_pct *= -1
        return pnl_pct <= -self.config.stop_loss_pct or pnl_pct >= self.config.take_profit_pct

    def target_fraction(self, signal: float, realized_vol: float) -> float:
        if realized_vol <= 1e-9:
            scaled = signal
        else:
            scaled = signal * min(self.config.vol_target / realized_vol, 2.0)
        return max(min(scaled, self.config.max_gross_exposure), -self.config.max_gross_exposure)
