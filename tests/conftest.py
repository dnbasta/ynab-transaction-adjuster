from datetime import date

import pytest

from ynabtransactionadjuster.models import Transaction, Category, Payee, SubTransaction, ModifierSubTransaction, CategoryGroup
from ynabtransactionadjuster.repos import CategoryRepo


@pytest.fixture
def mock_subtransaction(request):
	return ModifierSubTransaction(memo='memo', amount=500,
								  category=Category(name='cname', id='cid'),
								  payee=Payee(name='pname'))


@pytest.fixture
def mock_original_transaction(request):
	subs = tuple()
	memo = 'memo'
	category = Category(id='cid1', name='cname')
	flag_color = 'red'
	if hasattr(request, 'param'):
		if request.param == 'subtransactions':
			st = SubTransaction(memo='memo1', amount=500,
								category=Category(name='cname', id='cid'),
								payee=Payee(name='pname'))
			subs = (st, st)
		if request.param == 'optional_none':
			memo = None
			category = None
			flag_color = None
	return Transaction(id='id',
					   memo=memo,
					   category=category,
					   payee=Payee(id='pid', name='pname'),
					   subtransactions=subs,
					   flag_color=flag_color,
					   amount=1000,
					   import_payee_name='ipn',
					   import_payee_name_original='ipno',
					   transaction_date=date(2024, 1, 1),
					   approved=False,
					   cleared='uncleared',
					   transfer_transaction_id=None)


@pytest.fixture
def mock_category_repo():
	return CategoryRepo(categories=[
		CategoryGroup(name='group1', categories=frozenset([Category(id='cid1', name='c_name')])),
		CategoryGroup(name='group2', categories=frozenset([Category(id='cid2', name='c_name')]))])


@pytest.fixture
def mock_transaction_dict():
	return dict(id='id', amount=1000, date='2024-01-01', category_name='category', category_id='categoryid',
				payee_name='payee', payee_id='payeeid', flag_color=None, memo=None, subtransactions=[],
				import_payee_name_original=None, import_payee_name=None, transfer_account_id='transfer_account_id',
				approved=False, cleared='uncleared', transfer_transaction_id='transfer_transaction_id')
