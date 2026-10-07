from __future__ import annotations

from .models import Account


class NotFoundError(LookupError):
    pass


class AccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}

    def find(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def save(self, account: Account) -> Account:
        self._accounts[account.account_id] = account
        return account