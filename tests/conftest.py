from datetime import date

import pytest

from ynabtransactionadjuster.models import OriginalTransaction, Category, Payee, OriginalSubTransaction, SubTransaction, CategoryGroup
from ynabtransactionadjuster.repos import CategoryRepo


@pytest.fixture
def mock_subtransaction(request):
	return SubTransaction(memo='memo', amount=500,
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
			st = OriginalSubTransaction(memo='memo1', amount=500,
								   category=Category(name='cname', id='cid'),
								   payee=Payee(name='pname'))
			subs = (st, st)
		if request.param == 'optional_none':
			memo = None
			category = None
			flag_color = None
	return OriginalTransaction(id='id',
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
							   cleared='uncleared')


@pytest.fixture
def mock_category_repo():
	return CategoryRepo(categories=[
		CategoryGroup(name='group1', categories=frozenset([Category(id='cid1', name='c_name')])),
		CategoryGroup(name='group2', categories=frozenset([Category(id='cid2', name='c_name')]))])
