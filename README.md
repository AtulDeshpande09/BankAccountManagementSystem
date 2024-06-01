# Bank Account Management System

This project is a simple bank account management system implemented in Python using Object-Oriented Programming (OOP) principles. It includes functionality for savings and checking accounts, handling deposits, withdrawals, and applying interest, with transaction history tracking.

## Features

- Deposit and withdrawal transactions with transaction history
- Interest application for savings accounts
- Overdraft limit for checking accounts
- Account validation and exception handling
- Saving and loading accounts from a JSON file
- Retrieving account details and total bank funds

## Classes and Features

1. **BankAccount (Abstract Base Class)**
   - Attributes: `account_number`, `balance`, `transaction_list`
   - Methods: `deposit`, `withdraw`, `get_balance`, `apply_interest` (abstract), `get_transaction_history`, `__str__`, `__add__`

2. **SavingsAccount (Subclass of BankAccount)**
   - Additional Attribute: `interest_rate`
   - Method Override: `apply_interest`

3. **CheckingAccount (Subclass of BankAccount)**
   - Additional Attribute: `overdraft_limit`
   - Method Override: `withdraw`

4. **Transaction**
   - Attributes: `type`, `amount`, `date`

5. **Bank**
   - Attributes: `account_list`
   - Methods: `add_account`, `remove_account`, `get_bank_account`, `get_total_funds`, `validate_account_number`, `save_accounts`, `load_accounts`
