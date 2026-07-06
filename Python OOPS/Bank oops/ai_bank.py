import json
import random
import string
from pathlib import Path

class Bank:
    def __init__(self, db_path='accountdata.json'):
        self.db_path = db_path
        self.accounts = self._load_data()

    def _load_data(self):
        """Private method to load data on initialization."""
        if Path(self.db_path).exists():
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        """Saves current state to JSON."""
        with open(self.db_path, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def _generate_account_no(self):
        digits = random.choices(string.digits, k=4)
        letters = random.choices(string.ascii_letters, k=3)
        account_no = digits + letters
        random.shuffle(account_no)
        return "".join(account_no)

    def find_account(self, pin):
        return next((acc for acc in self.accounts if acc['pin'] == pin), None)

    def create_account(self, name, age, email, pin):
        if age < 18:
            return False, "User must be 18+ years old."
        
        # Check if PIN is unique (Logic moved from UI to Engine)
        if any(acc['pin'] == pin for acc in self.accounts):
            return False, "This PIN is already registered."

        new_user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "Account_number": self._generate_account_no(),
            "Account_balance": 0
        }
        self.accounts.append(new_user)
        self.save_data()
        return True, new_user

    def update_balance(self, pin, amount):
        acc = self.find_account(pin)
        if acc:
            if acc['Account_balance'] + amount < 0:
                return False, "Insufficient funds."
            acc['Account_balance'] += amount
            self.save_data()
            return True, acc['Account_balance']
        return False, "Account not found."
    