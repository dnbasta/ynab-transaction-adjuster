from typing import List, Dict

from ynabtransactionadjuster.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabtransactionadjuster.models import CategoryGroup
from ynabtransactionadjuster.models import Category


class CategoryRepo:
	"""Repository which holds all categories from your YNAB budget

	:ivar _categories: List of Category Groups in YNAB budget
	"""
	def __init__(self, categories: List[CategoryGroup]):
		self._categories = categories

	def fetch_by_name(self, category_name: str, group_name: str = None) -> Category:
		"""Fetches a YNAB category by its name

		:param category_name: Name of the category to fetch
		:param group_name: Optional name of the group the category belongs to
		:return: Matched category by name
		:raises NoMatchingCategoryError: if no matching category is found
		:raises MultipleMatchingCategoriesError: if multiple matching categories are found
		"""
		if group_name:
			cat_groups = [c for c in self._categories if c.name == group_name]
		else:
			cat_groups = self._categories

		cats = [c for cg in cat_groups for c in cg.categories if category_name == c.name]

		if len(cats) == 1:
			return cats[0]
		elif len(cats) > 1:
			raise MultipleMatchingCategoriesError(category_name, cats)
		raise NoMatchingCategoryError(category_name)

	def fetch_by_id(self, category_id: str) -> Category:
		"""Fetches a YNAB category by its ID
		:param category_id: ID of the category
		:return: Returns the matched category
		:raises NoMatchingCategoryError: if no matching category is found
		"""
		try:
			return next(c for cg in self._categories for c in cg.categories if c.id == category_id)
		except StopIteration:
			raise NoMatchingCategoryError(category_id)

	def fetch_all(self) -> Dict[str, List[Category]]:
		"""Fetches all Categories from YNAB budget

		:return: Dictionary with group names as keys and list of categories as values
		"""

		return {cg.name: list(cg.categories) for cg in self._categories}
