from datetime import datetime

import pytest

from ynabtransactionadjuster.models import Transaction, Category, Payee


def test_from_dict(mock_transaction_dict):
	o = Transaction.from_dict(mock_transaction_dict)
	assert o.id == mock_transaction_dict['id']
	assert o.amount == mock_transaction_dict['amount']
	assert o.transaction_date == datetime.strptime(mock_transaction_dict['date'], '%Y-%m-%d').date()
	assert o.category == Category(id=mock_transaction_dict['category_id'], name=mock_transaction_dict['category_name'])
	assert o.payee == Payee(id=mock_transaction_dict['payee_id'], name=mock_transaction_dict['payee_name'],
							transfer_account_id=mock_transaction_dict['transfer_account_id'])
	assert o.flag_color == mock_transaction_dict['flag_color']
	assert o.memo == mock_transaction_dict['memo']
	assert o.import_payee_name_original == mock_transaction_dict['import_payee_name_original']
	assert o.import_payee_name == mock_transaction_dict['import_payee_name']
	assert o.approved == mock_transaction_dict['approved']
	assert o.cleared == mock_transaction_dict['cleared']
	assert o.transfer_transaction_id == mock_transaction_dict['transfer_transaction_id']
	assert not o.subtransactions


@pytest.mark.parametrize('name, cid, expected', [
	('Uncategorized', None, None),
	('Split', 'id', None),
	('category', 'id', Category(id='id', name='category'))])
def test_from_dict_category(mock_transaction_dict, name, cid, expected):
	# Arrange
	mock_transaction_dict['category_name'] = name
	mock_transaction_dict['category_id'] = cid

	o = Transaction.from_dict(mock_transaction_dict)

	assert o.category == expected


def test_from_dict_subtransactions(mock_transaction_dict):
	# Arrange
	st = dict(amount=500, memo='memo', category_name='category', category_id='categoryid', payee_name='payee',
			   payee_id='payeeid', transfer_account_id='transferid')
	mock_transaction_dict['subtransactions'] = [st, st]

	# Act
	o = Transaction.from_dict(mock_transaction_dict)

	# Assert
	assert len(o.subtransactions) == 2
	assert o.subtransactions[0].amount == st['amount']
	assert o.subtransactions[0].payee == Payee(id=st['payee_id'], name=st['payee_name'], transfer_account_id=st['transfer_account_id'])
	assert o.subtransactions[0].memo == st['memo']
	assert o.subtransactions[0].category == Category(id=st['category_id'], name=st['category_name'])
