from dataclasses import dataclass


@dataclass
class Credentials:
	"""Credentials to use for YNAB

	:ivar token: The YNAB token to use
	:ivar budget: The YNAB budget id to use
	:ivar account: The YNAB account id to use
	"""
	token: str
	budget: str
	account: str
