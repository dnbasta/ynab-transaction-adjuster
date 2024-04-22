import pytest

from ynabtransactionadjuster.exceptions import SignatureError
from ynabtransactionadjuster.signaturechecker import SignatureChecker


def mock_parent(self, x: int, y: str):
	pass


def test_check_parameter_count_success():
	# Arrange
	def mock_func(x, y):
		pass

	# Act
	SignatureChecker(func=mock_func, parent_func=mock_parent).check_parameter_count()


def test_check_parameter_count_fail():
	# Arrange
	def mock_func(x):
		pass

	# Act
	with pytest.raises(SignatureError):
		SignatureChecker(func=mock_func, parent_func=mock_parent).check_parameter_count()


def test_check_annotations_fail_on_type():
	# Arrange
	def mock_func(x: dict):
		pass

	# Act
	with pytest.raises(SignatureError):
		SignatureChecker(func=mock_func, parent_func=mock_parent).check_parameter_annotations()


def test_check_annotations_fail_on_type_count():
	# Arrange
	def mock_func(x: int, y: int):
		pass

	# Act
	with pytest.raises(SignatureError):
		SignatureChecker(func=mock_func, parent_func=mock_parent).check_parameter_annotations()


def test_check_annotation_type_success():

	# Arrange
	def mock_func(x: int):
		pass

	# Act
	SignatureChecker(func=mock_func, parent_func=mock_parent).check_parameter_annotations()
