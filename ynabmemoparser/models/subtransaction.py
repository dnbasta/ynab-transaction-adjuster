from dataclasses import dataclass

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee


@dataclass(frozen=True)
class SubTransaction:
	payee: Payee
	category: Category
	memo: str
	amount: int
