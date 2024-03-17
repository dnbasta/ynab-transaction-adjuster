# Basic Usage
### Fetch transactions
Fetch current transactions from YNAB backend with all available information and check for useful values. All records 
come with two attributes (`import_payee_name` and `import_payee_name_original`) which are not shown in the user 
interface.

```py
from ynabtransactionadjuster import YnabTransactionAdjuster

ynab_transaction_adjuster = YnabTransactionAdjuster(token='<token>',
													budget='<budget>',
													account='<account>')
orig_transactions = ynab_transaction_adjuster.fetch()
```

### Create a [`AdjusterFactory`][adjusterfactory.AdjusterFactory] child class
This class is for implementing your actual logic. It needs to implement a `run()` method which receives on runtime 
the [`OriginalTransaction`][models.OriginalTransaction] and a [`TransactionModifier`][models.TransactionModifier]. The 
latter is prefilled with values from the original transaction. Its attributes can be modified, and it needs to be 
returned at the end of the function. Please refer to the [detailed usage](detailed_usage.md) section for explanations 
how to change different attributes.

```py
from ynabtransactionadjuster import AdjusterFactory
from ynabtransactionadjuster.models import OriginalTransaction, TransactionModifier


class MyAdjusterFactory(AdjusterFactory):

	def run(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		# your implementation

		# return the altered modifier
		return modifier
```

### Test your factory
Test the factory on records fetched via the `fetch()`method. If only a subset of these transactions should
get adjusted, filter them before handing the list over to the `adjust()` method. The method returns a list 
of [`ModifiedTransaction`][models.ModifiedTransaction] objects which can be inspected for the changed properties.

```py
transations = ynab_transaction_adjuster.fetch()
# optionally filter transactions before passing them to method below
mod_transactions = ynab_transaction_adjuster.adjust(transactions=transactions,
													factory_class=MyAdjusterFactory)
```

### Update records in YNAB
If you are satisfied with your parsing results you can pass the list of the 
[`ModifedTransaction`][models.ModifiedTransaction] objects to the `update()` method. It will update the 
changed transactions in YNAB and return an integer with the number of successfully updated records.

```py
count = ynab_transaction_adjuster.update(transactions=mod_transactions)
```
