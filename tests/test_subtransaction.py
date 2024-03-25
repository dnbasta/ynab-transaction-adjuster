import pytest
from pydantic import ValidationError

from ynabtransactionadjuster.models import SubTransaction, Category, Payee


@pytest.fixture
def mock_category():
	return Category(name='cname', id='id')


@pytest.fixture
def mock_payee():
	return Payee(name='pname')


def test_subtransaction_success(mock_category, mock_payee):
	SubTransaction(memo='memo', amount=1000, category=mock_category, payee=mock_payee)
	SubTransaction(memo=None, amount=1000, category=mock_category, payee=mock_payee)


def test_subtransaction_error(mock_category, mock_payee):
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=2.3, payee=mock_payee, category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee=mock_payee, category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee='xxx', category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee=mock_payee, category='xxx')


@pytest.mark.parametrize('test_input, expected', [
(SubTransaction(amount=1000), dict(amount=1000)),
	(SubTransaction(amount=1000, memo='memo'), dict(amount=1000, memo='memo')),
	(SubTransaction(amount=1000, payee=Payee(name='payee')), dict(amount=1000, payee_name='payee')),
	(SubTransaction(amount=1000, payee=Payee(name='payee', id='payeeid')), dict(amount=1000, payee_name='payee', payee_id='payeeid')),
	(SubTransaction(amount=1000, category=Category(name='category', id='categoryid')), dict(amount=1000, category_id='categoryid'))])
def test_as_dict(test_input, expected):
	# Act
	d = test_input.as_dict()

	# Assert
	assert d == expected
