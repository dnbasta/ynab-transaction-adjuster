from datetime import date, datetime

import pytest
from pydantic import ValidationError

from ynabtransactionadjuster.models import Category, Payee, Modifier, ModifiedTransaction


@pytest.mark.parametrize('test_attribute, test_input', [
	('memo', 'memox'),
	('transaction_date', date(2024, 1, 2)),
	('category', Category(id='c_id1', name='c_name1')),
	('payee', Payee(id='p_id1', name='p_name1', transfer_account_id='t_id1')),
	('flag_color', 'blue'),
	('approved', True),
	('cleared', 'cleared')])
def test_is_changed_true(test_attribute, test_input, mock_original_transaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	mock_modifier.__setattr__(test_attribute, test_input)
	modified = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act

	r = modified.is_changed()
	assert r is True


@pytest.mark.parametrize('mock_original_transaction', ['optional_none'], indirect=True)
@pytest.mark.parametrize('test_attribute, test_input', [
	('memo', 'memox'),
	('category', Category(id='c_id1', name='c_name1')),
])
def test_is_changed_true_none_values_in_original(test_attribute, test_input, mock_original_transaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	mock_modifier.__setattr__(test_attribute, test_input)
	modified = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act
	r = modified.is_changed()
	assert r is True


@pytest.mark.parametrize('mock_original_transaction', [None, 'optional_none'], indirect=True)
def test_changed_false(mock_original_transaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	modified = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act
	r = modified.is_changed()
	assert r is False


@pytest.mark.parametrize('mock_original_transaction', ['subtransactions'], indirect=True)
def test_invalid_subtransactions(mock_original_transaction, mock_subtransaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	mock_modifier.subtransactions = [mock_subtransaction, mock_subtransaction]
	with pytest.raises(ValidationError):
		ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)


def test_as_dict(mock_original_transaction, mock_subtransaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	mock_modifier.payee = Payee(id='pid2', name='pname2')
	mock_modifier.category = Category(id='cid2', name='cname2')
	mock_modifier.flag_color = 'blue'
	mock_modifier.subtransactions = [mock_subtransaction, mock_subtransaction]
	mt = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act
	d = mt.as_dict()

	# Assert
	assert d['id'] == mock_original_transaction.id
	assert d['payee_name'] == mt.transaction_modifier.payee.name
	assert d['payee_id'] == mt.transaction_modifier.payee.id
	assert d['category_id'] == mt.transaction_modifier.category.id
	assert d['flag_color'] == mt.transaction_modifier.flag_color
	assert len(d['subtransactions']) == 2
	assert isinstance(d['subtransactions'][0], dict)
	assert d['date'] == datetime.strftime(mock_modifier.transaction_date, '%Y-%m-%d')
	assert d['approved'] == mock_modifier.approved
	assert d['cleared'] == mock_modifier.cleared


def test_as_dict_none_values(mock_original_transaction):
	# Arrange
	mock_modifier = Modifier.from_transaction(mock_original_transaction)
	mock_modifier.category = None
	mock_modifier.flag_color = None
	mt = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act
	d = mt.as_dict()

	# Assert
	assert 'category_id' not in d.keys()
	assert 'flag_color' not in d.keys()
	assert 'subtransactions' not in d.keys()
