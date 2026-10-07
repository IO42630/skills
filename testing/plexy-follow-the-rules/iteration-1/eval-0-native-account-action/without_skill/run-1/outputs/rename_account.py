from dataclasses import dataclass, replace

from .models import Account
from .repository import AccountRepository, NotFoundError


@dataclass(frozen=True)
class RenameAccountAction:
    repository: AccountRepository

    def execute(self, account_id: str, *, rename_to: str) -> Account:
        account = self.repository.find(account_id)
        if account is None:
            raise NotFoundError(account_id)
        account = replace(account, name=rename_to)
        return self.repository.save(account)