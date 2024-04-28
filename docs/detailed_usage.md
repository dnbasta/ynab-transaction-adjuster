# Detailed Usage
## Change the category
The `adjust()` method allows changing the category of the transaction. For that purpose the adjuster class comes with a 
[`CategoryRepo`][repos.CategoryRepo] instance attached which can be used in the method via `self.categories`. The repo 
can be called with either `fetch_by_name()` or `fetch_by_id()` method to fetch a valid category. `fetch_all()` will 
return a `dict` with group names as key and a list of categories as values. It can be used for custom search patterns 
if needed. Using the category lookup is recommended to ensure only assign valid categories are assigned. The library 
doesn't allow creating new categories and specifying a non-existing category will raise an error.

```py
from ynabtransactionadjuster import Adjuster


class MyAdjuster(Adjuster):

	def filter(self, transactions):
		return transactions

	def adjust(self, transaction, modifier):
		my_category = self.categories.fetch_by_name('my_category')
		# or alternatively
		my_category = self.categories.fetch_by_id('category_id')
		modifier.category = my_category

		return modifier
```

## Change the payee
The payee of the transaction can be changed either by creating a new [`Payee`][models.Payee] object or fetching an
existing payee from the [`PayeeRepo`][repos.PayeeRepo] which can be used in the adjust function via `self.payees`. The 
repo can be called with either `fetch_by_name()` or `fetch_by_id()` method to fetch an existing payee. It can also be 
called with `fetch_by_transfer_account_id()` to fetch a transfer payee or with `fetch_all()`to get all payees. 
You can find the account id for the transfer account following the method mentioned in the [preparations](#preparations) section.

```py
from ynabtransactionadjuster import Adjuster, Payee

class MyAdjuster(Adjuster):

	def filter(self, transactions):
		return transactions

	def adjust(self, transaction, modifier):
		my_payee = Payee(name='My Payee')
		# or 
		my_payee = self.payees.fetch_by_name('My Payee')
		# or 
		my_payee = self.payees.fetch_by_id('payee_id')
		# or for transfers
		my_payee = self.payees.fetch_by_transfer_account_id('transfer_account_id')
		modifier.payee = my_payee

		return modifier
```

## Split the transaction
The transaction can be split if the original transaction is not already a split (YNAB doesn't allow updating splits 
of an existing split transaction). Splits can be created by using [`ModifierSubTransaction`][models.ModifierSubTransaction] 
instances. There must be at least two subtransactions and the sum of their amounts must be equal to the amount of the 
original transaction.

```py
from ynabtransactionadjuster import Adjuster, ModifierSubTransaction


class MyAdjuster(Adjuster):

	def filter(self, transactions):
		return transactions

	def adjust(self, transaction, modifier):
		# example for splitting a transaction in two equal amount subtransactions with different categories 
		subtransaction_1 = ModifierSubTransaction(amount=transaction.amount / 2,
												  category=transaction.category)
		subtransaction_2 = ModifierSubTransaction(amount=transaction.amount / 2,
												  category=self.categories.fetch_by_name('My 2nd Category'))
		modifier.subtransactions = [subtransaction_1, subtransaction_2]

		return modifier
```
## Fetch originating transactions from transfers
Transfer [`Transactions`][models.Transaction] have the original transaction linked via its id in the 
`transfer_transaction_id` attribute. That attribute can be used to fetch the corresponding transaction with the 
`fetch_transactions()` method in the adjuster
```py
from ynabtransactionadjuster import Adjuster, ModifierSubTransaction


class MyAdjuster(Adjuster):

    def filter(self, transactions):
        return transactions
    
    def adjust(self, transaction, modifier):
        originating_transaction = self.fetch_transaction(transaction.transfer_transaction_id)

        # Do something
        return modifier
```

## Use additional attributes in Adjuster child class
The `__init__()` constructor in the child class can be used to set additional attributes in the class. 
```py
from ynabtransactionadjuster import Adjuster, Credentials
from typing import Any

class MyAdjuster(Adjuster):
    
    def __init__(self, credentials: Credentials, my_attribute: Any):
        # initialize base adjuster class
        super().__init__(credentials=credentials)
        
        # set additional attributes
        self.myattribute = my_attribute
```

