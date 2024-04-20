from unittest.mock import MagicMock, patch

import pytest

from ynabtransactionadjuster import AdjusterBase, dry_run_adjuster, run_adjuster


class MockYnabTransactionAdjuster(AdjusterBase):

	def __init__(self, memo: str):
		self.categories = None
		self.payees = None
		self.memo = memo

	def filter(self, transactions):
		return transactions

	def adjust(self, original, modifier):
		modifier.memo = self.memo
		return modifier


@patch('ynabtransactionadjuster.functions.Client.fetch_transactions')
def test_test_adjuster(mock_client, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	mock_client.return_value = [mock_original_transaction]
	memo = 'test'
	my_adjuster = MockYnabTransactionAdjuster(memo=memo)
	my_adjuster.categories = mock_category_repo

	# Act
	r = dry_run_adjuster(adjuster=my_adjuster, credentials=MagicMock())

	# Assert
	assert len(r) == 1
	assert r[0]['changes']['memo']['changed'] == memo

@patch('ynabtransactionadjuster.functions.Client.fetch_transactions')
@patch('ynabtransactionadjuster.functions.Client.update_transactions')
def test_run(mock_update, mock_fetch, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='test')
	my_adjuster.categories = mock_category_repo
	mock_fetch.return_value = [mock_original_transaction]

	c = run_adjuster(my_adjuster, credentials=MagicMock())
	mock_update.assert_called_once()


@pytest.mark.parametrize('test_input', ['a', 'b'])
@patch('ynabtransactionadjuster.functions.Client.fetch_transactions')
@patch('ynabtransactionadjuster.functions.Client.update_transactions')
def test_run_no_modified(mock_update, mock_fetch, mock_category_repo, caplog, test_input, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='memo')
	my_adjuster.categories = mock_category_repo
	mock_fetch.return_value = [mock_original_transaction] if test_input == 'a' else []

	c = run_adjuster(my_adjuster, credentials=MagicMock())
	mock_update.assert_not_called()
