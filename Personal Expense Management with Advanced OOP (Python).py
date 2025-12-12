import json
import csv
from typing import List, Dict


class Transaction:
    """
    Represents a financial transaction (income or expense).
    """

    def __init__(self, transaction_type: str, category: str, amount: float):
        if transaction_type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        self.transaction_type = transaction_type
        self.category = category
        self.amount = amount

    def to_dict(self) -> Dict:
        """Converts the transaction to a dictionary (for JSON or CSV)."""
        return {"type": self.transaction_type, "category": self.category, "amount": self.amount}


class ExpenseTracker:
    """
    System for recording personal income and expenses.
    """

    def __init__(self):
        self.transactions: List[Transaction] = []

    # ---------- Main operations ----------
    def add_transaction(self, transaction_type: str, category: str, amount: float) -> None:
        """Adds a new transaction (income or expense)."""
        transaction = Transaction(transaction_type, category, amount)
        self.transactions.append(transaction)

    def calculate_balance(self) -> float:
        """Returns the total balance (income - expenses)."""
        income = sum(t.amount for t in self.transactions if t.transaction_type == "income")
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == "expense")
        return income - expenses

    def summary_by_category(self) -> Dict[str, float]:
        """Generates an expense summary by category."""
        summary: Dict[str, float] = {}
        for t in self.transactions:
            if t.transaction_type == "expense":
                summary[t.category] = summary.get(t.category, 0) + t.amount
        return summary

    # ---------- JSON persistence ----------
    def save_json(self, filename: str) -> None:
        """Saves transactions to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=4)

    def load_json(self, filename: str) -> None:
        """Loads transactions from a JSON file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.transactions = [Transaction(**item) for item in data]
        except FileNotFoundError:
            self.transactions = []

    # ---------- CSV persistence ----------
    def save_csv(self, filename: str) -> None:
        """Saves transactions to a CSV file."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["type", "category", "amount"])
            writer.writeheader()
            for t in self.transactions:
                writer.writerow(t.to_dict())

    def load_csv(self, filename: str) -> None:
        """Loads transactions from a CSV file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.transactions = [Transaction(row["type"], row["category"], float(row["amount"])) for row in reader]
        except FileNotFoundError:
            self.transactions = []


# =======================
# Real usage example
# =======================
if __name__ == "__main__":
    system = ExpenseTracker()

    # Register transactions
    system.add_transaction("income", "salary", 2500)
    system.add_transaction("expense", "food", 300)
    system.add_transaction("expense", "transportation", 150)
    system.add_transaction("expense", "entertainment", 200)

    # Calculate balance
    print(f" Current balance: ${system.calculate_balance()}")

    # Summary by category
    print("\n Expense summary by category:")
    for category, total in system.summary_by_category().items():
        print(f" - {category}: ${total}")

    # Save to files
    system.save_json("transactions.json")
    system.save_csv("transactions.csv")

    # Load from files
    new_system = ExpenseTracker()
    new_system.load_json("transactions.json")
    print(f"\n Loaded from JSON, balance: ${new_system.calculate_balance()}")
