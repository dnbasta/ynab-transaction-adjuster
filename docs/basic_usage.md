# Basic Usage

### Create an Adjuster
Create a child class of [`YnabTransactionAdjuster`][ynabtransactionadjuster.YnabTransactionAdjuster].
This class needs to implement a `filter()` and an `adjust()` method which contain the intended logic. The `filter()`
method receives a list of [`OriginalTransaction`][models.OriginalTransaction] objects which can be filtered before 
adjustement. The `adjust()` method receives a singular [`OriginalTransaction`][models.OriginalTransaction] and a 
[`TransactionModifier`][models.TransactionModifier]. The latter is prefilled with values from the original transaction. 
Its attributes can be modified, and it needs to be returned at the end of the function. 
Please refer to the [detailed usage](detailed_usage.md) section for explanations how to change different attributes.
```py
from ynabtransactionadjuster import YnabTransactionAdjuster
from ynabtransactionadjuster.models import OriginalTransaction, TransactionModifier


class MyAdjuster(YnabTransactionAdjuster):
    
    def filter(self, transactions: List[OriginalTransaction]) -> List[OriginalTransaction]:
        # your implementation
        
        # return the filtered list of transactions
        return transactions
        
    def adjust(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
        # your implementation

		# return the altered modifier
		return modifier
```

### Initialize
Initalize the adjuster with `token`, `budget` and `account` from YNAB
```py
my_adjuster = MyAdjuster(token='<token>', budget='<budget>', account='<account>')
```

### Test
Test the adjuster on records fetched via the `test()`method. The method fetches and executes the 
adjustments but doesn't write the results back to YNAB. Instead it returns a list of 
the changed transactions which can be inspected for the changed properties.

```py
mod_transactions = my_adjuster.test()
```

### Run
If you are satisfied with the functionality you can execute the adjuster with the `run()` method. This will run the 
adjustments and will update the changed transactions in YNAB. The method returns an integer with the number of 
successfully updated records.
```py
count_of_updated_transactions = my_adjuster.run()
```
