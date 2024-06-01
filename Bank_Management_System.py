from abc import ABC, abstractmethod
from datetime import date
import json

class InvalidAccountException(Exception):
    pass

class InsufficientFundsException(Exception):
    pass

class BankAccount(ABC):
    def __init__(self, account_number, balance):
        if not Bank.validate_account_number(account_number):
            raise InvalidAccountException(f"Invalid account number: {account_number}")
        self.account_number = account_number
        self.balance = balance
        self.transaction_list = []

    def deposit(self, d_amount):
        self.balance += d_amount
        print(f"You deposited {d_amount} money")
        print(f"Total Balance: {self.balance}")
        self.transaction_list.append(Transaction("Deposit", d_amount))

    def withdraw(self, w_amount):
        if w_amount <= self.balance:
            self.balance -= w_amount
            print(f"You withdrew {w_amount} money")
            print(f"Total Balance: {self.balance}")
            self.transaction_list.append(Transaction("Withdraw", w_amount))
        else:
            raise InsufficientFundsException("INSUFFICIENT FUND BALANCE")

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"Account Number: {self.account_number}, Balance: {self.balance}"

    @abstractmethod
    def apply_interest(self):
        pass

    def get_transaction_history(self):
        for transaction in self.transaction_list:
            print(transaction)

    def __add__(self, other):
        return self.balance + other.balance

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance, interest_rate):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance *= (1 + self.interest_rate / 100)

class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance, overdraft_limit):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, w_amount):
        if w_amount <= self.balance:
            self.balance -= w_amount
            print(f"You withdrew {w_amount} money")
            print(f"Total Balance: {self.balance}")
            self.transaction_list.append(Transaction("Withdraw", w_amount))
        elif w_amount <= self.balance + self.overdraft_limit:
            overdraft_used = w_amount - self.balance
            self.balance = 0
            self.overdraft_limit -= overdraft_used
            print(f"You withdrew {w_amount} money using overdraft")
            print(f"Total Balance: {self.balance}, Remaining Overdraft Limit: {self.overdraft_limit}")
            self.transaction_list.append(Transaction("Withdraw", w_amount))
        else:
            raise InsufficientFundsException("INSUFFICIENT FUND BALANCE")

    def apply_interest(self):
        pass

class Transaction:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount
        self.date = date.today()

    def __str__(self):
        return f"{self.date}: {self.type} of {self.amount}"

class Bank:
    def __init__(self):
        self.account_list = []

    def add_account(self, bank_account):
        self.account_list.append(bank_account)

    def remove_account(self, bank_account):
        self.account_list.remove(bank_account)
    
    def get_bank_account(self, account_number):
        for account in self.account_list:
            if account.account_number == account_number:
                return account
        raise InvalidAccountException("INVALID ACCOUNT")

    def get_total_funds(self):
        total_fund = 0
        for account in self.account_list:
            total_fund += account.get_balance()
        return total_fund

    @staticmethod
    def validate_account_number(account_number):
        return len(account_number) == 9 and account_number.isdigit()

    def save_accounts(self, filename):
        with open(filename, 'w') as file:
            json.dump([account.__dict__ for account in self.account_list], file, default=str)

    def load_accounts(self, filename):
        with open(filename, 'r') as file:
            account_data = json.load(file)
            for account_info in account_data:
                if "interest_rate" in account_info:
                    account = SavingsAccount(account_info["account_number"], account_info["balance"], account_info["interest_rate"])
                elif "overdraft_limit" in account_info:
                    account = CheckingAccount(account_info["account_number"], account_info["balance"], account_info["overdraft_limit"])
                else:
                    account = BankAccount(account_info["account_number"], account_info["balance"])
                self.add_account(account)

# Example usage
try:
    savings = SavingsAccount("987654321", 2000.0, 5.0)
    savings.deposit(500.0)
    savings.apply_interest()
    print(savings.get_balance())  # Output should reflect the interest added
    print(savings)  # Output the account details

    checking = CheckingAccount("123456789", 1000.0, 500.0)
    checking.deposit(300.0)
    checking.withdraw(1500.0)
    print(checking.get_balance())  # Output should consider the overdraft limit
    print(checking)  # Output the account details

    bank = Bank()
    bank.add_account(savings)
    bank.add_account(checking)
    print(bank.get_total_funds())  # Output should reflect the combined balance of all accounts
    print(Bank.validate_account_number("123456789"))  # Output: True
    print(Bank.validate_account_number("12345"))  # Output: False

    # Print transaction history for savings account
    savings.get_transaction_history()

    # Combine two accounts (balance addition)
    combined_balance = savings + checking
    print(combined_balance)  # Output should be the sum of both balances

    # Handle custom exceptions
    try:
        checking.withdraw(3000.0)  # Should raise InsufficientFundsException
    except InsufficientFundsException as e:
        print(e)

    # Serialize and save bank accounts to a file
    bank.save_accounts("accounts.json")

    # Load bank accounts from a file
    bank.load_accounts("accounts.json")

    # Retrieve an account by its number
    account = bank.get_bank_account("987654321")
    print(account)

except InvalidAccountException as e:
    print(e)
except InsufficientFundsException as e:
    print(e)
