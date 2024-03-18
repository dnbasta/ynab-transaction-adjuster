from abc import abstractmethod
from typing import List

from ynabtransactionadjuster.adjuster import Adjuster
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models import OriginalTransaction, ModifiedTransaction
from ynabtransactionadjuster.models import TransactionModifier
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo


class YnabTransactionAdjuster:
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the run method in it according to your needs. It has attributes which allow you to
	lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	"""
	def __init__(self, budget: str, account: str, token: str) -> None:
		self._budget = budget
		self._account = account
		self._client = Client(token=token, budget=budget, account=account)
		self.categories: CategoryRepo = CategoryRepo(self._client.fetch_categories())
		self.payees: PayeeRepo = PayeeRepo(self._client.fetch_payees())

	def run(self) -> int:
		transactions = self._client.fetch_transactions()
		filtered_transactions = self.filter(transactions)
		sa = Adjuster(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = sa.run()
		updated = self._client.update_transactions(modified_transactions)
		return updated

	def test(self) -> List[ModifiedTransaction]:
		transactions = self._client.fetch_transactions()
		filtered_transactions = self.filter(transactions)
		sa = Adjuster(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = sa.run()
		return modified_transactions

	@abstractmethod
	def filter(self, transactions: List[OriginalTransaction]) -> List[OriginalTransaction]:
		pass

	@abstractmethod
	def adjust(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		"""Function which implements the actual modification of a transaction. It is initiated and called by the library
		for all transactions provided in the parse_transaction method of the main class.

		:param original: Original transaction
		:param modifier: Transaction modifier prefilled with values from original transaction. All attributes can be
		changed and will modify the transaction
		:returns: Method needs to return the transaction modifier after modification
		"""
		pass
