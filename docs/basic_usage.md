# Basic Usage

### Create an Adjuster
Create a child class of [`Adjuster`][ynabtransactionadjuster.Adjuster].
This class needs to implement a `filter()` and an `adjust()` method which contain the intended logic. The `filter()`
method receives a list of [`Transaction`][models.Transaction] objects which can be filtered before 
adjustement. The `adjust()` method receives a single [`Transaction`][models.Transaction] and a 
[`Modifier`][models.Modifier]. The latter is prefilled with values from the original transaction and can be altered. 
The modifier needs to be returned at the end of the function. 
Please check the [detailed usage](detailed_usage.md) section for explanations how to change different attributes.

```py
from ynabtransactionadjuster import Adjuster, Transaction, Modifier


class MyAdjuster(Adjuster):

	def filter(self, transactions: List[Transaction]) -> List[Transaction]:
		# your implementation

		# return the filtered list of transactions
		return transactions

	def adjust(self, transaction: Transaction, modifier: Modifier) -> Modifier:
		# your implementation

		# return the altered modifier
		return modifier
```

### Initialize
Create a [`Credentials`][models.Credentials] object and initialize Adjuster class with it
```py
from ynabtransactionadjuster import Credentials

my_credentials = Credentials(token='<token>', budget='<budget>', account='<account>')
my_adjuster = MyAdjuster.from_credentials(credentials=my_credentials)
```

### Test
Test the adjuster on records fetched via the `dry_run()` method. It executes the adjustments but doesn't write the 
results back to YNAB. Instead it returns a list of the changed transactions which can be inspected for the changed 
properties.

```py
mod_transactions = my_adjuster.dry_run()
```

### Run
If you are satisfied with the functionality you can execute the adjuster with the `run()` method. This will run the 
adjustments and will update the changed transactions in YNAB. The method returns an integer with the number of 
successfully updated records.
```py
count_of_updated_transactions = my_adjuster.run()
```
