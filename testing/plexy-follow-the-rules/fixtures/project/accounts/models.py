from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    account_id: str
    name: str