from dataclasses import dataclass

from .models import Account
from .repository import AccountRepository


@dataclass(frozen=True)
class CreateAccountAction:
    repository: AccountRepository

    def execute(self, account_id: str, *, name: str) -> Account:
        account = Account(account_id=account_id, name=name.strip())
        return self.repository.save(account)