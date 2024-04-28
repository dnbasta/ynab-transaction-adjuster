from unittest.mock import MagicMock, patch, PropertyMock

from ynabtransactionadjuster import Adjuster, ModifiedTransaction


class MockYnabTransactionAdjuster(Adjuster):

	def __init__(self, memo: str):
		super().__init__(MagicMock())
		self.memo = memo

	def filter(self, transactions):
		return transactions

	def adjust(self, transaction, modifier):
		modifier.memo = self.memo
		return modifier


@patch("ynabtransactionadjuster.Adjuster.categories", new_callable=PropertyMock)
@patch("ynabtransactionadjuster.Adjuster.transactions", new_callable=PropertyMock)
def test_apply(mock_transactions, mock_categories, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	memo = 'test'
	my_adjuster = MockYnabTransactionAdjuster(memo=memo)
	mock_transactions.return_value = [mock_original_transaction]
	mock_categories.return_value = mock_category_repo

	# Act
	r = my_adjuster.apply()

	# Assert
	assert len(r) == 1
	assert isinstance(r[0], ModifiedTransaction)
	assert r[0].modifier.memo == memo


@patch('ynabtransactionadjuster.adjuster.Client.update_transactions')
def test_update(mock_update, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='test')

	my_adjuster.update(modified_transactions=[MagicMock(spec=ModifiedTransaction)])
	mock_update.assert_called_once()


@patch('ynabtransactionadjuster.adjuster.Client.update_transactions')
def test_run_no_modified(mock_update, mock_category_repo, caplog, mock_original_transaction):
	# Arrange
	my_adjuster = MockYnabTransactionAdjuster(memo='memo')

	my_adjuster.update([])
	mock_update.assert_not_called()
