import pytest

from ynabtransactionadjuster.exceptions import NoMatchingAccountError
from ynabtransactionadjuster.models.account import Account
from ynabtransactionadjuster.repos.accountrepo import AccountRepo


@pytest.fixture
def mock_account_repo():
	return AccountRepo(accounts=[Account(id='aid1', name='aname1'), Account(id='aid2', name='aname2')])


def test_fetch_account_by_name_success(mock_account_repo):
	# Act
	a = mock_account_repo.fetch_by_name(account_name='aname2')

	# Assert
	assert isinstance(a, Account)
	assert a.name == 'aname2'


def test_fetch_account_by_name_fail(mock_account_repo):
	# Act
	with pytest.raises(NoMatchingAccountError):
		mock_account_repo.fetch_by_name(account_name='xxx')

