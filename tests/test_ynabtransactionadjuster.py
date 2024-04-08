from unittest.mock import MagicMock

import pytest

from ynabtransactionadjuster import YnabTransactionAdjuster


class MockYnabTransactionAdjuster(YnabTransactionAdjuster):

	def __init__(self, memo: str):
		self._client = None
		self.categories = None
		self.payees = None
		self.memo = memo

	def filter(self, transactions):
		return transactions

	def adjust(self, original, modifier):
		modifier.memo = self.memo
		return modifier


def test_test(mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	memo = 'test'
	my_adjuster = MockYnabTransactionAdjuster(memo=memo)
	mock_client = MagicMock()
	mock_client.fetch_transactions.return_value = [mock_original_transaction]
	my_adjuster._client = mock_client
	my_adjuster.categories = mock_category_repo
	# Act
	r = my_adjuster.test()

	# Assert
	assert len(r) == 1
	assert r[0]['changes']['memo']['changed'] == memo


def test_run(mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='test')
	mock_client = MagicMock()
	mock_client.fetch_transactions.return_value = [mock_original_transaction]
	my_adjuster._client = mock_client
	my_adjuster.categories = mock_category_repo

	my_adjuster.run()
	my_adjuster._client.update_transactions.assert_called_once()


@pytest.mark.parametrize('test_input', ['a', 'b'])
def test_run_no_modified(mock_category_repo, caplog, test_input, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='memo')
	mock_client = MagicMock()
	mock_client.fetch_transactions.return_value = [mock_original_transaction] if test_input == 'a' else []
	my_adjuster._client = mock_client
	my_adjuster.categories = mock_category_repo

	my_adjuster.run()
	my_adjuster._client.update_transactions.assert_not_called()
