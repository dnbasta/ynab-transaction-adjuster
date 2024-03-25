from datetime import datetime

from pydantic import BaseModel, model_validator

from ynabtransactionadjuster.models.originaltransaction import OriginalTransaction
from ynabtransactionadjuster.models.transactionmodifier import TransactionModifier


class ModifiedTransaction(BaseModel):
	original_transaction: OriginalTransaction
	transaction_modifier: TransactionModifier

	def is_changed(self) -> bool:
		"""Helper function to determine if transaction has been altered as compared to original one

		:returns: True if values from original transaction have been altered, False otherwise
		"""
		if self.changed_attributes():
			return True
		return False

	def as_dict(self) -> dict:
		"""Returns a dictionary representation of the transaction which is used for the update call to YNAB"""
		t_dict = dict(id=self.original_transaction.id,
					payee_name=self.transaction_modifier.payee.name,
					payee_id=self.transaction_modifier.payee.id,
					date=datetime.strftime(self.transaction_modifier.transaction_date, '%Y-%m-%d'))
		if len(self.transaction_modifier.subtransactions) > 0:
			t_dict['subtransactions'] = [s.as_dict() for s in self.transaction_modifier.subtransactions]
		if self.transaction_modifier.category:
			t_dict['category_id'] = self.transaction_modifier.category.id
		if self.transaction_modifier.flag_color:
			t_dict['flag_color'] = self.transaction_modifier.flag_color
		if self.transaction_modifier.memo:
			t_dict['memo'] = self.transaction_modifier.memo

		return t_dict

	def changed_attributes(self) -> dict:
		"""Returns a dictionary representation of the modified values and the original transaction"""
		changed_attributes = {}
		if self.transaction_modifier.payee != self.original_transaction.payee:
			changed_attributes['payee'] = dict(original=self.original_transaction.payee,
											   changed=self.transaction_modifier.payee)
		if (self.transaction_modifier.transaction_date.isocalendar() !=
				self.original_transaction.transaction_date.isocalendar()):
			changed_attributes['transaction_date'] = dict(original=self.original_transaction.transaction_date,
														  changed=self.transaction_modifier.transaction_date)
		if (self.transaction_modifier.category and
				self.transaction_modifier.category.id != self.original_transaction.category.id):
			changed_attributes['category'] = dict(original=self.original_transaction.category,
												  changed=self.transaction_modifier.category)
		if self.transaction_modifier.memo != self.original_transaction.memo:
			changed_attributes['memo'] = dict(original=self.original_transaction.memo,
											  changed=self.transaction_modifier.memo)
		if self.transaction_modifier.flag_color != self.original_transaction.flag_color:
			changed_attributes['flag_color'] = dict(original=self.original_transaction.flag_color,
													changed=self.transaction_modifier.flag_color)
		if len(self.transaction_modifier.subtransactions) > 0:
			changed_attributes['subtransactions'] = dict(original=[],
														changed=self.transaction_modifier.subtransactions)
		return changed_attributes

	@model_validator(mode='after')
	def check_values(self):
		if len(self.transaction_modifier.subtransactions) > 1:
			if len(self.original_transaction.subtransactions) > 1:
				raise ValueError(f"Existing Subtransactions can not be updated")
			if sum(a.amount for a in self.transaction_modifier.subtransactions) != self.original_transaction.amount:
				raise ValueError('Amount of subtransactions needs to be equal to amount of original transaction')
		return self
