from __future__ import annotations

from .models import AccountState


class PaperBroker:
    def __init__(self, fee_bps: float):
        self.fee_rate = fee_bps / 10_000.0

    def rebalance_to_fraction(self, account: AccountState, price: float, target_fraction: float) -> None:
        if price <= 0:
            return

        account.equity = account.cash + account.position.units * price
        target_notional = account.equity * target_fraction
        current_notional = account.position.units * price
        delta_notional = target_notional - current_notional
        delta_units = delta_notional / price

        fees = abs(delta_notional) * self.fee_rate
        account.cash -= delta_notional
        account.cash -= fees

        new_units = account.position.units + delta_units
        if new_units == 0:
            account.position.units = 0.0
            account.position.avg_price = 0.0
        elif account.position.units == 0 or (account.position.units > 0) == (delta_units > 0):
            prev_notional = account.position.units * account.position.avg_price
            add_notional = delta_units * price
            account.position.units = new_units
            account.position.avg_price = (prev_notional + add_notional) / new_units
        else:
            account.position.units = new_units
            if (account.position.units > 0) != (new_units > 0):
                account.position.avg_price = price

        account.equity = account.cash + account.position.units * price
        account.peak_equity = max(account.peak_equity, account.equity)

    def flatten(self, account: AccountState, price: float) -> None:
        self.rebalance_to_fraction(account, price, 0.0)
