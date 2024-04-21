import inspect
from typing import List, Callable, Optional, OrderedDict

from ynabtransactionadjuster.exceptions import AdjustError, NoMatchingCategoryError
from ynabtransactionadjuster.models import Transaction, ModifiedTransaction, Modifier, Category
from ynabtransactionadjuster.repos import CategoryRepo


class Serializer:

	def __init__(self, transactions: List[Transaction], adjust_func: Callable, categories: CategoryRepo):
		self._transactions = transactions
		self._adjust_func = adjust_func
		self._categories = categories

	def run(self) -> List[ModifiedTransaction]:
		modified_transactions = [self.adjust_single(transaction=t, adjust_func=self._adjust_func)
								 for t in self._transactions]
		filtered_transactions = [t for t in modified_transactions if t.is_changed()]
		return filtered_transactions

	def adjust_single(self, transaction: Transaction, adjust_func: Callable) -> ModifiedTransaction:
		modifier = Modifier.from_transaction(transaction=transaction)
		try:
			transaction_field, modifier_field = self.find_field_names(adjust_func)
			modifier_return = adjust_func(**{transaction_field: transaction, modifier_field: modifier})
			self.validate_instance(modifier_return)
			self.validate_attributes(modifier_return)
			self.validate_category(modifier_return.category)
			modified_transaction = ModifiedTransaction(original_transaction=transaction,
													   transaction_modifier=modifier_return)
			return modified_transaction
		except Exception as e:
			raise AdjustError(f"Error while adjusting {transaction.as_dict()}") from e

	def validate_category(self, category: Category):
		if category:
			self._categories.fetch_by_id(category.id)

	@staticmethod
	def validate_attributes(modifier: Modifier):
		Modifier.model_validate(modifier.__dict__)

	@staticmethod
	def validate_instance(modifier: Optional[Modifier]):
		if not isinstance(modifier, Modifier):
			raise AdjustError(f"Adjust function doesn't return TransactionModifier object")

	@staticmethod
	def find_field_names(adjust_func: Callable) -> (str, str):
		args_dict = inspect.signature(adjust_func).parameters
		transaction_field = next(k for k, v in args_dict.items() if v.annotation == Transaction)
		modifier_field = next(k for k, v in args_dict.items() if v.annotation == Modifier)
		return transaction_field, modifier_field
