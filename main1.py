import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class ExpenseTracker:

    def __init__(self, filename="expenses.csv"):
        self.filename = filename

        if not os.path.exists(self.filename):
            data = pd.DataFrame(
                columns=["Date", "Category", "Amount", "Description"]
            )
            data.to_csv(self.filename, index=False)

    def add_expense(self):
        date = input("Enter date (YYYY-MM-DD): ")
        category = input("Enter category: ")
        description = input("Enter description: ")

        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                return

        except ValueError:
            print("Please enter a valid amount.")
            return

        new_expense = pd.DataFrame([{
            "Date": date,
            "Category": category,
            "Amount": amount,
            "Description": description
        }])

        new_expense.to_csv(
            self.filename,
            mode="a",
            header=False,
            index=False
        )

        print("Expense added successfully!")

    def view_expenses(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            print("No expenses found.")
        else:
            print("\nYour Expenses:")
            print(data.to_string(index=False))

    def search_expense(self):
        keyword = input("Enter category or description to search: ")

        data = pd.read_csv(self.filename)

        result = data[
            data["Category"].str.contains(keyword, case=False, na=False)
            |
            data["Description"].str.contains(keyword, case=False, na=False)
        ]

        if result.empty:
            print("No matching expense found.")
        else:
            print(result.to_string(index=False))

    def category_summary(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            print("No expenses available.")
            return

        summary = data.groupby("Category")["Amount"].sum()

        print("\nCategory Summary:")
        print(summary)

    def monthly_summary(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            print("No expenses available.")
            return

        data["Date"] = pd.to_datetime(data["Date"])

        data["Month"] = data["Date"].dt.to_period("M")

        summary = data.groupby("Month")["Amount"].sum()

        print("\nMonthly Summary:")
        print(summary)

    def total_expense(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            return 0

        amounts = data["Amount"].to_numpy()

        return np.sum(amounts)

    def delete_expense(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            print("No expenses available.")
            return

        print(data.to_string())

        try:
            number = int(input("Enter row number to delete: "))

            if number < 0 or number >= len(data):
                print("Invalid row number.")
                return

            data = data.drop(number)

            data.to_csv(self.filename, index=False)

            print("Expense deleted successfully!")

        except ValueError:
            print("Please enter a valid number.")

    def generate_charts(self):
        data = pd.read_csv(self.filename)

        if data.empty:
            print("No expenses available for charts.")
            return

        category_data = data.groupby("Category")["Amount"].sum()

        category_data.plot(kind="bar")

        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")

        plt.tight_layout()
        plt.show()

        monthly_data = data.copy()

        monthly_data["Date"] = pd.to_datetime(monthly_data["Date"])
        monthly_data["Month"] = monthly_data["Date"].dt.to_period("M")

        monthly_total = monthly_data.groupby("Month")["Amount"].sum()

        monthly_total.plot(kind="line", marker="o")

        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Amount")

        plt.tight_layout()
        plt.show()


def main():

    tracker = ExpenseTracker()

    while True:

        print("\n==============================")
        print("     PERSONAL EXPENSE TRACKER")
        print("==============================")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Category Summary")
        print("5. Monthly Summary")
        print("6. Total Expense")
        print("7. Generate Graphs")
        print("8. Delete Expense")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            tracker.add_expense()

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.search_expense()

        elif choice == "4":
            tracker.category_summary()

        elif choice == "5":
            tracker.monthly_summary()

        elif choice == "6":
            total = tracker.total_expense()
            print("Total Expense: ₹", total)

        elif choice == "7":
            tracker.generate_charts()

        elif choice == "8":
            tracker.delete_expense()

        elif choice == "9":
            print("Thank you for using Personal Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
