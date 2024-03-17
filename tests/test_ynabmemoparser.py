from unittest.mock import patch

import pytest

from ynabtransactionadjuster import Modifier, YnabTransactionAdjuster
from ynabtransactionadjuster.exceptions import FactoryError
from ynabtransactionadjuster.models import ModifiedTransaction


def test_parse_transactions_fails(mock_memo_parser, caplog, mock_original_transaction):
	# Arrange
	class MyParser(Modifier):
		def parse(self, original, modifier):
			modifier.memo = 'xxx'/0
			return modifier

	# Act
	with pytest.raises(FactoryError):
		mock_memo_parser.adjust(transactions=[mock_original_transaction], factory_class=MyParser)


def test_parse_transactions_success(mock_memo_parser, caplog, mock_original_transaction):
	# Arrange
	class MyParser(Modifier):
		def parse(self, original, modifier):
			modifier.memo = 'xxx'
			return modifier

	# Act
	r = mock_memo_parser.adjust(transactions=[mock_original_transaction], factory_class=MyParser)
	assert len(r) == 1
	assert isinstance(r[0], ModifiedTransaction)
	assert r[0].transaction_modifier.memo == 'xxx'
