from unittest.mock import PropertyMock, MagicMock

import pytest

from ynabtransactionadjuster import Modifier, Transaction
from ynabtransactionadjuster.exceptions import SignatureError
from ynabtransactionadjuster.serializer import Serializer


def test_find_field_names_position():
	def mock_func(x, y):
		pass
	s = Serializer(transactions=[MagicMock()], categories=MagicMock(), adjust_func=mock_func)
	tf, mf = s.find_field_names()
	assert tf == 'x'
	assert mf == 'y'


def test_find_field_names_partial_annotation():
	def mock_func(x: Modifier, y):
		pass
	s = Serializer(transactions=[MagicMock()], adjust_func=mock_func, categories=MagicMock())
	tf, mf = s.find_field_names()
	assert tf == 'y'
	assert mf == 'x'


def test_find_field_names_annotation():
	def mock_func(x: Modifier, y: Transaction):
		pass
	s = Serializer(transactions=[MagicMock()], adjust_func=mock_func, categories=MagicMock())
	tf, mf = s.find_field_names()
	assert tf == 'y'
	assert mf == 'x'
