from typing import List

from ynabtransactionadjuster.adjusterbase import AdjusterBase
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models.credentials import Credentials
from ynabtransactionadjuster.repos import CategoryRepo, PayeeRepo
from ynabtransactionadjuster.serializer import Serializer


def fetch_categories(credentials: Credentials) -> CategoryRepo:
	"""Fetches categories from YNAB budget.

	:param credentials: Credentials to use for YNAB API

	:return: Collection of categories from YNAB budget
	"""
	client = Client.from_credentials(credentials=credentials)
	return CategoryRepo(client.fetch_categories())


def fetch_payees(credentials: Credentials) -> PayeeRepo:
	"""Fetches payees from YNAB budget.

	:param credentials: Credentials to use for YNAB API

	:return: Collection of payees from YNAB budget
	"""
	client = Client.from_credentials(credentials=credentials)
	return PayeeRepo(client.fetch_payees())


def dry_run_adjuster(adjuster: AdjusterBase, credentials: Credentials) -> List[dict]:

	"""Tests the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
	implementation of the two methods. This function doesn't update records in YNAB but returns the modified
	transactions so that they can be inspected.

	:param adjuster: Adjuster to use
	:param credentials: Credentials to use for YNAB API

	:return: List of modified transactions in the format
	:raises AdjustError: if there is any error during the adjust process
	:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
	"""
	client = Client.from_credentials(credentials=credentials)
	transactions = client.fetch_transactions()
	filtered_transactions = adjuster.filter(transactions)
	s = Serializer(transactions=filtered_transactions, adjust_func=adjuster.adjust, categories=adjuster.categories)
	modified_transactions = [{'original': mt.original_transaction, 'changes': mt.changed_attributes()} for mt in s.run()]
	return modified_transactions


def run_adjuster(adjuster: AdjusterBase, credentials: Credentials) -> int:
	"""Run the adjuster. It will fetch transactions from the YNAB account, filter & adjust them as per
	implementation of the two methods and push the updated transactions back to YNAB

	:param adjuster: Adjuster to use
	:param credentials: Credentials to use for YNAB API

	:return: count of adjusted transactions which have been updated in YNAB
	:raises AdjustError: if there is any error during the adjust process
	:raises HTTPError: if there is any error with the YNAB API (e.g. wrong credentials)
	"""
	client = Client.from_credentials(credentials=credentials)
	transactions = client.fetch_transactions()
	filtered_transactions = adjuster.filter(transactions)
	adjuster = Serializer(transactions=filtered_transactions, adjust_func=adjuster.adjust, categories=adjuster.categories)
	modified_transactions = adjuster.run()
	if modified_transactions:
		updated = client.update_transactions(modified_transactions)
		return updated
	return 0
