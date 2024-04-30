from unittest.mock import MagicMock, patch

from requests import Response

from ynabtransactionadjuster import Transaction
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models.account import Account
from ynabtransactionadjuster.models.payee import Payee


@patch('ynabtransactionadjuster.client.requests.get')
def test_fetch_categories(get_patch):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'category_groups': [
		{'id': 'cg_id', 'name': 'cg_name', 'deleted': False, 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False},
																			{'id': 'c_id', 'name': 'c_name', 'deleted': True}]},
		{'id': 'cg_id2', 'name': 'cg_name2', 'deleted': True, 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False}]}
	]}}
	get_patch.return_value = resp

	# Act
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())
	cats = c.fetch_categories()

	# Assert
	assert len(cats) == 1
	assert cats[0].name == 'cg_name'
	assert list(cats[0].categories)[0].name == 'c_name'
	assert list(cats[0].categories)[0].id == 'c_id'


@patch('ynabtransactionadjuster.client.requests.get')
def test_fetch_payees(mock_get):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'payees': [{
		'id': 'p_id', 'name': 'p_name', 'deleted': False, 'transfer_account_id': 't_id'}]}}
	mock_get.return_value = resp

	# Act
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())
	p_list = c.fetch_payees()

	# Assert
	assert len(p_list) == 1
	assert isinstance(p_list[0], Payee)
	assert p_list[0].name == 'p_name'
	assert p_list[0].id == 'p_id'
	assert p_list[0].transfer_account_id == 't_id'


@patch('ynabtransactionadjuster.client.requests.get')
def test_fetch_transaction(mock_get, mock_transaction_dict):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'transaction': mock_transaction_dict}}
	mock_get.return_value = resp
	client = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())

	# Act
	t = client.fetch_transaction('transaction_id')
	assert isinstance(t, Transaction)


@patch('ynabtransactionadjuster.client.requests.get')
def test_fetch_accounts(mock_get):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'accounts': [dict(name='account_name', id='account_id', deleted=False),
											dict(name='account_name2', id='account_id2', deleted=True)]}}
	mock_get.return_value = resp
	client = Client.from_credentials(MagicMock())

	# Act
	a = client.fetch_accounts()

	# Assert
	assert len(a) == 1
	assert isinstance(a[0], Account)
	assert a[0].name == 'account_name'
	assert a[0].id == 'account_id'
