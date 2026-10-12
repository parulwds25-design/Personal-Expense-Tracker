"""Personal Expense Tracker - Assessment III utility.

Run with: python main.py
Charts are saved to the charts/ folder and displayed when a GUI is available.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

DATA_FILE = Path(__file__).with_name("expenses.csv")
CHART_DIR = Path(__file__).with_name("charts")
FIELDS = ("Date", "Category", "Amount", "Description")
DATE_FORMAT = "%Y-%m-%d"


def load_expenses() -> list[dict]:
    """Load saved expense records; return an empty list for a new project."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        expenses = []
        for row in rows:
            date_text = row.get("Date", row.get("date", "")).strip()
            category = row.get("Category", row.get("category", "")).strip()
            amount_text = row.get("Amount", row.get("amount", ""))
            description = row.get("Description", row.get("description", "")).strip()
            date = datetime.strptime(date_text, DATE_FORMAT)
            amount = float(amount_text)
            if amount > 0:
                expenses.append({"date": date.strftime(DATE_FORMAT), "category": category,
                                 "description": description, "amount": amount})
        return expenses
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print(f"Could not read {DATA_FILE.name}: {error}")
        return []


def save_expenses(expenses: list[dict]) -> None:
    """Write all expenses to a portable CSV file."""
    with DATA_FILE.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({"Date": item["date"], "Category": item["category"],
                          "Amount": item["amount"], "Description": item["description"]}
                         for item in expenses)


def add_expense(expenses: list[dict]) -> None:
    print("\n--- Add expense ---")
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()
        try:
            date_text = datetime.strptime(date_text, DATE_FORMAT).strftime(DATE_FORMAT)
            break
        except ValueError:
            print("Enter a valid date such as 2026-10-12.")
    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount (₹): "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter a number greater than zero.")
        return
    expenses.append({"date": date_text, "category": category,
                     "description": description, "amount": amount})
    save_expenses(expenses)
    print("Expense saved.")


def view_expenses(expenses: list[dict]) -> None:
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("\nDate        | Category       | Amount     | Description")
    print("-" * 72)
    for item in sorted(expenses, key=lambda entry: datetime.strptime(entry["date"], DATE_FORMAT)):
        print(f"{item['date']} | {item['category'][:14]:14} | ₹{item['amount']:9.2f} | {item['description']}")


def category_totals(expenses: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for item in expenses:
        totals[item["category"]] += item["amount"]
    return dict(sorted(totals.items(), key=lambda pair: pair[1], reverse=True))


def show_category_summary(expenses: list[dict]) -> None:
    totals = category_totals(expenses)
    if not totals:
        print("No expenses to summarize.")
        return
    print("\n--- Category totals ---")
    for category, amount in totals.items():
        print(f"{category}: ₹{amount:.2f}")
    print(f"Overall total: ₹{sum(totals.values()):.2f}")


def show_monthly_summary(expenses: list[dict]) -> None:
    month = input("Month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Enter a valid month such as 2026-10.")
        return
    matching = [item for item in expenses if item["date"][:7] == month]
    print(f"Total for {month}: ₹{sum(item['amount'] for item in matching):.2f} ({len(matching)} transactions)")


def generate_graph(expenses: list[dict]) -> None:
    """Save category and monthly spending charts as PNG files."""
    if not expenses:
        print("Add at least one expense before generating a graph.")
        return
    if plt is None:
        print("Charts need Matplotlib. Install it with: python -m pip install matplotlib")
        return
    CHART_DIR.mkdir(exist_ok=True)
    totals = category_totals(expenses)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(totals.keys(), totals.values(), color="#4285F4")
    ax.set(title="Expenses by Category", xlabel="Category", ylabel="Amount (₹)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    category_path = CHART_DIR / "category_spending.png"
    fig.savefig(category_path, dpi=150)
    plt.close(fig)

    months: dict[str, float] = defaultdict(float)
    for item in expenses:
        parsed = datetime.strptime(item["date"], DATE_FORMAT)
        months[parsed.strftime("%Y-%m")] += item["amount"]
    ordered_months = sorted(months)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ordered_months, [months[key] for key in ordered_months], marker="o", color="#0F9D58")
    ax.set(title="Monthly Spending Trend", xlabel="Month", ylabel="Amount (₹)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    monthly_path = CHART_DIR / "monthly_spending.png"
    fig.savefig(monthly_path, dpi=150)
    plt.close(fig)
    print(f"Charts saved to:\n  {category_path}\n  {monthly_path}")
    try:
        import os
        if os.environ.get("DISPLAY") or os.name == "nt":
            for image_path in (category_path, monthly_path):
                image = plt.imread(image_path)
                plt.figure(figsize=(8, 5))
                plt.imshow(image)
                plt.axis("off")
                plt.show()
    except Exception:
        print("Image files were saved; this environment cannot open chart windows.")


def search_by_category(expenses: list[dict]) -> None:
    query = input("Category to search: ").strip().casefold()
    matches = [item for item in expenses if item["category"].casefold() == query]
    if not matches:
        print("No matching expenses.")
        return
    for item in matches:
        print(f"{item['date']} | {item['category']} | ₹{item['amount']:.2f} | {item['description']}")


def delete_expense(expenses: list[dict]) -> None:
    if not expenses:
        print("No expenses to delete.")
        return
    view_expenses(expenses)
    try:
        index = int(input("Enter row number to delete (0 to cancel): "))
        if index == 0:
            return
        if not 1 <= index <= len(expenses):
            print("Row number is out of range.")
            return
        del expenses[index - 1]
        save_expenses(expenses)
        print("Expense deleted.")
    except ValueError:
        print("Enter a whole-number row number.")


def main() -> None:
    expenses = load_expenses()
    actions = {"1": lambda: add_expense(expenses),
               "2": lambda: view_expenses(expenses),
               "3": lambda: search_by_category(expenses),
               "4": lambda: show_category_summary(expenses),
               "5": lambda: show_monthly_summary(expenses),
               "6": lambda: generate_graph(expenses),
               "7": lambda: print(f"Total expenses: ₹{sum(item['amount'] for item in expenses):.2f}"),
               "8": lambda: delete_expense(expenses)}
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1 Add expense | 2 View expenses | 3 Search category")
        print("4 Category summary | 5 Monthly summary | 6 Generate graphs")
        print("7 Total expenses | 8 Delete expense | 9 Exit")
        choice = input("Select (1-9): ").strip()
        if choice == "9":
            print("Good luck with your assessment!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Choose a number from 1 to 9.")


if __name__ == "__main__":
    main()
