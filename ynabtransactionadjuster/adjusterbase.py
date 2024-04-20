from abc import abstractmethod
from typing import List

from ynabtransactionadjuster.models.credentials import Credentials
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models import OriginalTransaction
from ynabtransactionadjuster.models import TransactionModifier
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo


class AdjusterBase:
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the `filter()`and `adjust()` method in it according to your needs. It has attributes
	which allow you to lookup categories and payees from your budget.

	:param budget: The YNAB budget id to use
	:param account: The YNAB account id to use
	:param token: The YNAB token to use

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	"""
	def __init__(self, categories: CategoryRepo, payees: PayeeRepo) -> None:
		self.categories = categories
		self.payees = payees

	@classmethod
	def from_credentials(cls, credentials: Credentials):
		"""Instantiate a Adjuster class from a Credentials object

		:param credentials: Credentials to use for YNAB API
		"""
		client = Client.from_credentials(credentials=credentials)
		categories = CategoryRepo(client.fetch_categories())
		payees = PayeeRepo(client.fetch_payees())
		return cls(categories=categories, payees=payees)

	@abstractmethod
	def filter(self, transactions: List[OriginalTransaction]) -> List[OriginalTransaction]:
		"""Function which implements filtering for the list of transactions from YNAB account. It receives a list of
		the original transactions which can be filtered. Must return the filtered list or just the list if no filtering
		is intended.

		:param transactions: List of original transactions from YNAB
		:return: Method needs to return a list of filtered transactions"""
		pass

	@abstractmethod
	def adjust(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		"""Function which implements the actual modification of a transaction. It receives the original transaction from
		YNAB and a prefilled modifier. The modifier can be altered and must be returned.

		:param original: Original transaction
		:param modifier: Transaction modifier prefilled with values from original transaction. All attributes can be
		changed and will modify the transaction
		:returns: Method needs to return the transaction modifier after modification
		"""
		pass
