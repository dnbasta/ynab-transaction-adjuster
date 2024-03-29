from typing import List

import requests
from requests import HTTPError

from ynabtransactionadjuster.models import CategoryGroup, ModifiedTransaction
from ynabtransactionadjuster.models import OriginalTransaction
from ynabtransactionadjuster.models import Payee


YNAB_BASE_URL = 'https://api.ynab.com/v1'


class Client:
	"""Client for reading from and writing to YNAB

	:param token: YNAB API token
	:param budget: YNAB budget ID
	:param account: YNAB account ID
	"""

	def __init__(self, token: str, budget: str, account: str):
		self._header = {'Authorization': f'Bearer {token}'}
		self._budget = budget
		self._account = account

	def fetch_categories(self) -> List[CategoryGroup]:
		"""Fetches categories from YNAB"""
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/categories', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['category_groups']
		categories = [CategoryGroup.from_dict(cg) for cg in data if cg['deleted'] is False]
		return categories

	def fetch_payees(self) -> List[Payee]:
		"""Fetches payees from YNAB"""
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/payees', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['payees']
		payees = [Payee.from_dict(p) for p in data if p['deleted'] is False]
		return payees

	def fetch_transactions(self) -> List[OriginalTransaction]:
		"""Fetches transactions from YNAB"""
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/accounts/{self._account}/transactions', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['transactions']
		transaction_dicts = [t for t in data if t['deleted'] is False]
		transactions = [OriginalTransaction.from_dict(t) for t in transaction_dicts]
		return transactions

	def update_transactions(self, transactions: List[ModifiedTransaction]) -> int:
		"""Updates transactions in YNAB. The updates are done in bulk.

		:param transactions: list of modified transactions to be updated
		:raises HTTPError: if bulk update call is not successful. Error can be related to any item in the passed list
		of transactions
		"""
		update_dict = {'transactions': [r.as_dict() for r in transactions]}
		r = requests.patch(f'{YNAB_BASE_URL}/budgets/{self._budget}/transactions',
						   json=update_dict,
						   headers=self._header)
		try:
			r.raise_for_status()
		except HTTPError as e:
			raise HTTPError(r.text, update_dict)
		r_dict = r.json()['data']['transaction_ids']
		return len(r_dict)
