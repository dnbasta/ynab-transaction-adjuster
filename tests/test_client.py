from unittest.mock import MagicMock, patch

from requests import Response, Session

from ynabtransactionadjuster import Transaction
from ynabtransactionadjuster.client import Client
from ynabtransactionadjuster.models.account import Account
from ynabtransactionadjuster.models.payee import Payee

def create_mock_session(res: dict) -> MagicMock:
	mock_session = MagicMock(spec=Session)
	mock_session.headers = MagicMock()
	mock_response = MagicMock(spec=Response)
	mock_response.json.return_value = res
	mock_session.get.return_value = mock_response
	return mock_session


def test_fetch_categories():
	# Arrange
	resp = {'data': {'category_groups': [
		{'id': 'cg_id', 'name': 'cg_name', 'deleted': False,
		 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False},
						{'id': 'c_id', 'name': 'c_name', 'deleted': True}]},
		{'id': 'cg_id2', 'name': 'cg_name2', 'deleted': True,
		 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False}]}
	]}}
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock(), session=create_mock_session(resp))
	# Act

	cats = c.fetch_categories()

	# Assert
	assert len(cats) == 1
	assert cats[0].name == 'cg_name'
	assert list(cats[0].categories)[0].name == 'c_name'
	assert list(cats[0].categories)[0].id == 'c_id'


def test_fetch_payees():
	# Arrange
	resp = {'data': {'payees': [{
		'id': 'p_id', 'name': 'p_name', 'deleted': False, 'transfer_account_id': 't_id'}]}}
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock(), session=create_mock_session(resp))

	# Act

	p_list = c.fetch_payees()

	# Assert
	assert len(p_list) == 1
	assert isinstance(p_list[0], Payee)
	assert p_list[0].name == 'p_name'
	assert p_list[0].id == 'p_id'
	assert p_list[0].transfer_account_id == 't_id'


def test_fetch_transaction(mock_transaction_dict):
	# Arrange
	resp = {'data': {'transaction': mock_transaction_dict}}
	client = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock(), session=create_mock_session(resp))

	# Act
	t = client.fetch_transaction('transaction_id')
	assert isinstance(t, Transaction)


def test_fetch_accounts():
	# Arrange
	resp = {'data': {'accounts': [dict(name='account_name', id='account_id', deleted=False),
											dict(name='account_name2', id='account_id2', deleted=True)]}}
	client = Client.from_credentials(credentials=MagicMock(), session=create_mock_session(resp))

	# Act
	a = client.fetch_accounts()

	# Assert
	assert len(a) == 1
	assert isinstance(a[0], Account)
	assert a[0].name == 'account_name'
	assert a[0].id == 'account_id'
