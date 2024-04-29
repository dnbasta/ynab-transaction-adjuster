
from abc import abstractmethod, ABCMeta
from typing import List
from deprecated import deprecated

from ynabtransactionadjuster.models import ModifiedTransaction
from ynabtransactionadjuster.models.credentials import Credentials
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models import Transaction
from ynabtransactionadjuster.models import Modifier
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo
from ynabtransactionadjuster.serializer import Serializer
from ynabtransactionadjuster.signaturechecker import SignatureChecker


class Adjuster(metaclass=ABCMeta):
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the `filter()`and `adjust()` method in it according to your needs. It has attributes
	which allow you to lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	:ivar transactions: All current non deleted transactions from YNAB Account
	:ivar credentials: Credentials for YNAB API
	"""
	def __init__(self, credentials: Credentials):
		self.credentials = credentials
		self._client = Client.from_credentials(self.credentials)
		self._categories = None
		self._payees = None

	@property
	def categories(self) -> CategoryRepo:
		if not self._categories:
			self._categories = CategoryRepo(self._client.fetch_categories())
		return self._categories

	@property
	def payees(self) -> PayeeRepo:
		if not self._payees:
			self._payees = PayeeRepo(self._client.fetch_payees())
		return self._payees

	@property
	def transactions(self) -> List[Transaction]:
		if self.credentials.account:
			return self._client.fetch_transactions(account_id=self.credentials.account)
		return self._client.fetch_transactions()

	@abstractmethod
	def filter(self, transactions: List[Transaction]) -> List[Transaction]:
		"""Function which implements filtering for the list of transactions from YNAB account. It receives a list of
		the original transactions which can be filtered. Must return the filtered list or just the list if no filtering
		is intended.

		:param transactions: List of original transactions from YNAB
		:return: Method needs to return a list of filtered transactions"""
		pass

	@abstractmethod
	def adjust(self, transaction: Transaction, modifier: Modifier) -> Modifier:
		"""Function which implements the actual modification of a transaction. It receives the original transaction from
		YNAB and a prefilled modifier. The modifier can be altered and must be returned.

		:param transaction: Original transaction
		:param modifier: Transaction modifier prefilled with values from original transaction. All attributes can be
		changed and will modify the transaction
		:returns: Method needs to return the transaction modifier after modification
		"""
		pass

	def apply(self) -> List[ModifiedTransaction]:
		"""Function which applies filter & adjust function on transactions as per implementation of the two methods.

		:return: Filtered list of modified transactions (only transactions with actual changes are returned)
		:raises SignatureError: if signature of implemented adjuster functions is not compatible
		:raises AdjustError: if there is any error during the adjust process
		"""
		self._check_signatures()
		filtered_transactions = self.filter(self.transactions)
		s = Serializer(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = s.run()
		return modified_transactions

	def update(self, modified_transactions: List[ModifiedTransaction]) -> int:
		"""Updates the modified transactions in YNAB

		:param modified_transactions: List of modified transactions to be updated in YNAB
		:return: count of adjusted transactions which have been updated in YNAB
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		if modified_transactions:
			updated = self._client.update_transactions(modified_transactions)
			return updated
		return 0

	def _check_signatures(self):
		SignatureChecker(func=self.filter, parent_func=Adjuster.filter).check()
		SignatureChecker(func=self.adjust, parent_func=Adjuster.adjust).check()

	def fetch_transaction(self, transaction_id: str) -> Transaction:
		"""Fetches an individual transaction from the YNAB account

		:param transaction_id: Transaction ID of the transaction to be fetched
		"""
		return self._client.fetch_transaction(transaction_id=transaction_id)

	@classmethod
	@deprecated(version='1.2.0', reason='Use the standard constructor method MyAdjuster(credentials) instead.')
	def from_credentials(cls, credentials: Credentials):
		"""**Deprecated** Use the standard constructor method `MyAdjuster(credentials)` instead.

		Classmethod which creates a new Adjuster instance from credentials

		:param credentials: Credentials for YNAB APIx
		"""
		return cls(credentials)

	@deprecated(version='1.2.0', reason='Use apply() function instead.')
	def dry_run(self, pretty_print: bool = False) -> List[ModifiedTransaction]:
		"""	**Deprecated** Use `apply()` function instead

		Tests the filter & adjust methods of the adjuster.This function doesn't update records in YNAB.

		:param pretty_print: if set to True will print modified transactions as strings in console

		:return: List of modified transactions
		:raises SignatureError: if signature of implemented adjuster functions is not compatible
		:raises AdjustError: if there is any error during the adjust process
		"""
		modified_transactions = self.apply()
		if pretty_print:
			print('\n'.join(map(str, modified_transactions)))
		return modified_transactions

	@deprecated(version='1.2.0', reason='Use apply() and updated() function instead.')
	def run(self) -> int:
		"""**Deprecated** Use `apply()` and `update()` functions instead.

		Run the adjuster. It will apply the filter & adjust methods and update the modified transactions in YNAB

		:return: count of adjusted transactions which have been updated in YNAB
		:raises SignatureError: if signature of implemented adjuster functions is not compatible
		:raises AdjustError: if there is any error during the adjust process
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		modified_transactions = self.apply()
		return self.update(modified_transactions)
