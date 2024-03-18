# Detailed Usage
## Change the category
The `adjust()` method allows changing the category of the transaction. For that purpose the adjuster class comes with a 
[`CategoryRepo`][repos.CategoryRepo] instance attached which can be used in the method via `self.categories`. The repo 
can be called with either `fetch_by_name()` or `fetch_by_id()` method to fetch a valid category. Using the repo is 
recommended to ensure you only assign valid categories to the modifier. The library doesn't allow creating new 
categories and specifying a non-existing category will raise an error.

```py
from ynabtransactionadjuster import YnabTransactionAdjuster


class MyAdjusterFactory(YnabTransactionAdjuster):
    
    def filter(self, transactions):
        return transactions
        
    def adjust(self, original, modifier):
        my_category = self.categories.fetch_by_name('my_category')
        # or alternatively
        my_category = self.categories.fetch_by_id('category_id')
        modifier.category = my_category

        return modifier
```
The [`CategoryRepo`][repos.CategoryRepo] instance gets build when the adjuster gets initialized and can also be accessed 
from the main instance (e.g. for finding category ids to be used in the parser later). The `fetch_all()` method fetches 
all categories and returns a dict with group name as key and list of categories as values.
```py
my_adjuster = MyAdjuster(token='<token>', budget='<budget>', account='<account>')
categories = my_adjuster.categories.fetch_all()
```

## Change the payee
The payee of the transaction can be changed either by creating a new [`Payee`][models.Payee] object or fetching an
existing payee from the [`PayeeRepo`][repos.PayeeRepo] which can be used in the adjust function via `self.payees`. The 
repo can be called with either `fetch_by_name()` or `fetch_by_id()` method to fetch an existing payee. It can also be 
called with `fetch_by_transfer_account_id()` to fetch a transfer payee. You can find the account id for the transfer 
account following the method mentioned in the [preparations](#preparations) section.

```py
from ynabtransactionadjuster import YnabTransactionAdjuster
from ynabtransactionadjuster.models import Payee


class MyAdjuster(YnabTransactionAdjuster):
    
    def filter(self, transactions):
        return transactions
        
    def adjust(self, original, modifier):
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
The [`PayeeRepo`][repos.PayeeRepo] instance gets build when the adjuster gets initialized and can also be accessed 
from the main instance. The `fetch_all()` method fetches all payees in the budget.  

```py
my_adjuster = MyAdjuster(token='<token>', budget='<budget>', account='<account>')
payees = my_adjuster.payees.fetch_all()
```

## Split the transaction
The transaction can be splitted if the original transaction is not already a split (YNAB doesn't allow updating splits 
of an existing split transaction). Splits can be created by using [`SubTransaction`][models.SubTransaction] instances.
There must be at least two subtransactions and the sum of their amounts must be equal to the amount of the original 
transaction.

```py
from ynabtransactionadjuster import YnabTransactionAdjuster
from ynabtransactionadjuster.models import SubTransaction


class MyAdjuster(YnabTransactionAdjuster):
    
    def filter(self, transactions):
        return transactions
        
    def adjust(self, original, modifier):
        # example for splitting a transaction in two equal amount subtransactions with different categories 
        subtransaction_1 = SubTransaction(amount=original.amount / 2, 
                                          category=original.category)
        subtransaction_2 = SubTransaction(amount=original.amount / 2,
										  category=self.categories.fetch_by_name('My 2nd Category'))
        modifier.subtransactions = [subtransaction_1, subtransaction_2]

        return modifier
```


