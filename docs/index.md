# Installation

This library helps you to automatically adjust transactions in YNAB based on your logic. It allows you to implement 
your adjustments in a simple factory class which you can run against your existing transactions and update relevant 
fields like date, payee, category, memo and flags. It also allows you to split transactions.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dnbasta)

## Preparations
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)
2. Get the IDs of your budget and account which records are faulty. You can find both IDs if you go to the
[YNAB Webapp](https://app.ynab.com/) and open the target account by clicking on the name on the left hand side menu. 
The URL does now contain both IDs `https://app.ynab.com/<budget_id>/accounts/<account_id>`

## Installation 
Install library from PyPI
```bash
pip install ynab-transaction-adjuster
```
