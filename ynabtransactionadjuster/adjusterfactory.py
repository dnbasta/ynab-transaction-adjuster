from abc import abstractmethod

from ynabtransactionadjuster.models import TransactionModifier, OriginalTransaction
from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.repos import PayeeRepo


class AdjusterFactory:
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the run method in it according to your needs. It has attributes which allow you to
	lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	"""
	def __init__(self, categories: CategoryRepo, payees: PayeeRepo):
		self.categories: CategoryRepo = categories
		self.payees: PayeeRepo = payees

	@abstractmethod
	def run(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		"""Function which implements the actual modification of a transaction. It is initiated and called by the library
		for all transactions provided in the parse_transaction method of the main class.

		:param original: Original transaction
		:param modifier: Transaction modifier prefilled with values from original transaction. All attributes can be
		changed and will modify the transaction
		:returns: Method needs to return the transaction modifier after modification
		"""
		pass
