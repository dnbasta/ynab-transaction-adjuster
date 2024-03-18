# from typing import List
# from unittest.mock import patch, MagicMock
#
# import pytest
#
# from ynabtransactionadjuster import YnabTransactionAdjuster
# from ynabtransactionadjuster.exceptions import AdjustError
# from ynabtransactionadjuster.models import ModifiedTransaction, OriginalTransaction
#
#
# class MockYnabTransactionAdjuster(YnabTransactionAdjuster):
#
# 	def __init__(self):
# 		self._client = None
# 		self.categories = None
# 		self.payees = None
#
#k
# @pytest.fixture
# def mock_adjuster(mock_original_transaction, mock_category_repo):
# 	class MyAdjuster(MockYnabTransactionAdjuster):
#
# 		def filter(self, transactions):
# 			return transactions
#
# 		def adjust(self, original, modifier):
# 			return modifier
#
# 	my_adjuster = MyAdjuster()
# 	mock_client = MagicMock()
# 	mock_client.fetch_transactions.return_value = [mock_original_transaction]
# 	my_adjuster._client = mock_client
# 	my_adjuster.categories = mock_category_repo
# 	return my_adjuster
#
#
# def test_test(mock_category_repo, caplog, mock_original_transaction):
# 	# Arrange
# 	class MyAdjuster(MockYnabTransactionAdjuster):
#
# 		def filter(self, transactions):
# 			return transactions
#
# 		def adjust(self, original, modifier):
# 			modifier.memo = 'test'
# 			return modifier
#
# 	my_adjuster = MyAdjuster()
# 	mock_client = MagicMock()
# 	mock_client.fetch_transactions.return_value = [mock_original_transaction]
# 	my_adjuster._client = mock_client
# 	my_adjuster.categories = mock_category_repo
# 	# Act
# 	r = my_adjuster.test()
#
# 	# Assert
# 	assert len(r) == 1
# 	assert isinstance(r[0], ModifiedTransaction)
#
#
# def test_run(mock_adjuster, caplog, mock_original_transaction):
# 	# Arrange
# 	class MyAdjuster(MockYnabTransactionAdjuster):
# 		def filter(self, transactions):
# 			return transactions
#
# 		def adjust(self, original, modifier):
# 			modifier.memo = 'test'
# 			return modifier
#
# 	my_adjuster = MyAdjuster()
# 	my_adjuster.run()
# 	assert my_adjuster._client.update_transactions.called_once()
