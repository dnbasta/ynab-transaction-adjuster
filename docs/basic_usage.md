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
Create a [`Credentials`][models.Credentials] object and initialize Adjuster class with it. Providing `account` for the 
credentials is optional. If not set the Adjuster will work on all transactions in the budget. 
```py
from ynabtransactionadjuster import Credentials

my_credentials = Credentials(token='<token>', budget='<budget>', account='<account>')
my_adjuster = MyAdjuster(my_credentials)
```

### Apply
Apply the filter and adjust function on the fetched transactions from YNAB via the `apply()` method. It 
returns a filtered list of [`ModifiedTransaction`][models.ModifiedTransaction] which can be inspected for the changed 
properties via the `changed_attributes` attribute. Only actually changed transactions are returned. 
```py
modified_transactions = my_adjuster.apply()
```

### Update
The modified transactions can be upated in YNAB passing them to the `update()` function. The method returns an integer 
with the number of successfully updated records.
```py
count_of_updated_transactions = my_adjuster.update(modified_transactions)
```
