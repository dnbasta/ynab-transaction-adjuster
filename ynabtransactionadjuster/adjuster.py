from abc import abstractmethod
from typing import List

from ynabtransactionadjuster.models.credentials import Credentials
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models import OriginalTransaction
from ynabtransactionadjuster.models import TransactionModifier
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo
from ynabtransactionadjuster.serializer import Serializer


class Adjuster:
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the `filter()`and `adjust()` method in it according to your needs. It has attributes
	which allow you to lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	:ivar transactions: Transactions from YNAB Account
	:ivar credentials: Credentials for YNAB API
	"""
	def __init__(self, categories: CategoryRepo, payees: PayeeRepo, transactions: List[OriginalTransaction],
				 credentials: Credentials) -> None:
		self.categories = categories
		self.payees = payees
		self.transactions = transactions
		self.credentials = credentials

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

	def dry_run(self) -> List[dict]:
		"""Tests the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
		implementation of the two methods. This function doesn't update records in YNAB but returns the modified
		transactions so that they can be inspected.

		:return: List of modified transactions in the format
		:raises AdjustError: if there is any error during the adjust process
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		filtered_transactions = self.filter(self.transactions)
		s = Serializer(transactions=self.transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = [{'original': mt.original_transaction, 'changes': mt.changed_attributes()} for mt in s.run()]
		return modified_transactions

	def run(self) -> int:
		"""Run the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
		implementation of the two methods and push the updated transactions back to YNAB

		:return: count of adjusted transactions which have been updated in YNAB
		:raises AdjustError: if there is any error during the adjust process
		:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
		"""
		filtered_transactions = self.filter(self.transactions)
		s = Serializer(transactions=filtered_transactions, adjust_func=self.adjust, categories=self.categories)
		modified_transactions = s.run()
		if modified_transactions:
			client = Client.from_credentials(credentials=self.credentials)
			updated = client.update_transactions(modified_transactions)
			return updated
		return 0
