from unittest.mock import MagicMock, patch

import pytest

from ynabtransactionadjuster import Adjuster


class MockYnabTransactionAdjuster(Adjuster):

	def __init__(self, memo: str):
		self.categories = None
		self.payees = None
		self.transactions = None
		self.credentials = MagicMock()
		self.memo = memo

	def filter(self, transactions):
		return transactions

	def adjust(self, original, modifier):
		modifier.memo = self.memo
		return modifier


def test_dry_run(mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	memo = 'test'
	my_adjuster = MockYnabTransactionAdjuster(memo=memo)
	my_adjuster.transactions = [mock_original_transaction]
	my_adjuster.categories = mock_category_repo

	# Act
	r = my_adjuster.dry_run()

	# Assert
	assert len(r) == 1
	assert r[0]['changes']['memo']['changed'] == memo


@patch('ynabtransactionadjuster.adjuster.Client.update_transactions')
def test_run(mock_update, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='test')
	my_adjuster.categories = mock_category_repo
	my_adjuster.transactions = [mock_original_transaction]

	c = my_adjuster.run()
	mock_update.assert_called_once()


@pytest.mark.parametrize('test_input', ['a', 'b'])
@patch('ynabtransactionadjuster.adjuster.Client.update_transactions')
def test_run_no_modified(mock_update, mock_category_repo, caplog, test_input, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='memo')
	my_adjuster.categories = mock_category_repo
	my_adjuster.transactions = [mock_original_transaction] if test_input == 'a' else []

	c = my_adjuster.run()
	mock_update.assert_not_called()
