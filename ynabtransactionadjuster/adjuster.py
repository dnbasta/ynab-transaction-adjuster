from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List

from ynabtransactionadjuster.models import ModifiedTransaction
from ynabtransactionadjuster.models.credentials import Credentials
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models import Transaction
from ynabtransactionadjuster.models import Modifier
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo
from ynabtransactionadjuster.serializer import Serializer
from ynabtransactionadjuster.signaturechecker import SignatureChecker


@dataclass
class Adjuster(metaclass=ABCMeta):
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the `filter()`and `adjust()` method in it according to your needs. It has attributes
	which allow you to lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	:ivar transactions: Transactions from YNAB Account
	:ivar credentials: Credentials for YNAB API
	"""
	credentials: Credentials
	categories: CategoryRepo
	payees: PayeeRepo
	transactions: List[Transaction]

	@classmethod
	def from_credentials(cls, credentials: Credentials):
		"""Instantiate a Adjuster class from a Credentials object

		:param credentials: Credentials to use for YNAB API
		"""
		client = Client.from_credentials(credentials=credentials)
		categories = CategoryRepo(client.fetch_categories())
		payees = PayeeRepo(client.fetch_payees())
		transactions = client.fetch_transactions()
		return cls(categories=categories, payees=payees, transactions=transactions, credentials=credentials)

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

	def dry_run(self, pretty_print: bool = False) -> List[ModifiedTransaction]:
		"""Tests the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
		implementation of the two methods. This function doesn't update records in YNAB but returns the modified
		transactions so that they can be inspected.

		:param pretty_print: if set to True will print modified transactions as strings in console

		:return: List of modified transactions
		:raises SignatureError: if signature of implemented adjuster functions is not compatible
		:raises AdjustError: if there is any error during the adjust process
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		self.check_signatures()
		filtered_transactions = self.filter(self.transactions)
		s = Serializer(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = s.run()
		if pretty_print:
			print('\n'.join(map(str, modified_transactions)))
		return modified_transactions

	def run(self) -> int:
		"""Run the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
		implementation of the two methods and push the updated transactions back to YNAB

		:return: count of adjusted transactions which have been updated in YNAB
		:raises SignatureError: if signature of implemented adjuster functions is not compatible
		:raises AdjustError: if there is any error during the adjust process
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		self.check_signatures()
		filtered_transactions = self.filter(self.transactions)
		s = Serializer(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = s.run()
		if modified_transactions:
			client = Client.from_credentials(credentials=self.credentials)
			updated = client.update_transactions(modified_transactions)
			return updated
		return 0

	def check_signatures(self):
		SignatureChecker(func=self.filter, parent_func=Adjuster.filter).check()
		SignatureChecker(func=self.adjust, parent_func=Adjuster.adjust).check()
