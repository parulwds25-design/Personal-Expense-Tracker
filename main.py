# Personal Expense Tracker

expenses = []

while True:
    print("\n===================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("===================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Category Summary")
    print("5. Monthly Summary")
    print("6. Generate Graph")
    print("7. Exit")
    print("===================================")

    choice = input("Enter your choice: ")

    # Add Expense
    if choice == "1":
        print("\n--- Add Expense ---")

        date = input("Enter date (DD-MM-YYYY): ")
        category = input("Enter category: ")
        description = input("Enter description: ")

        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            expense = {
                "date": date,
                "category": category,
                "amount": amount,
                "description": description
            }

            expenses.append(expense)

            print("Expense added successfully!")

        except ValueError:
            print("Please enter a valid amount.")

    # View Expenses
    elif choice == "2":
        print("\n--- All Expenses ---")

        if len(expenses) == 0:
            print("No expenses recorded yet.")
        else:
            for i, expense in enumerate(expenses, start=1):
                print(
                    f"{i}. {expense['date']} | "
                    f"{expense['category']} | "
                    f"₹{expense['amount']:.2f} | "
                    f"{expense['description']}"
                )

    # Search Expense
    elif choice == "3":
        print("\n--- Search Expense ---")

        if len(expenses) == 0:
            print("No expenses recorded yet.")
        else:
            category = input("Enter category to search: ")

            found = False

            for expense in expenses:
                if expense["category"].lower() == category.lower():
                    print(
                        f"{expense['date']} | "
                        f"{expense['category']} | "
                        f"₹{expense['amount']:.2f} | "
                        f"{expense['description']}"
                    )
                    found = True

            if not found:
                print("No expense found in this category.")

    # Category Summary
    elif choice == "4":
        print("\n--- Category Summary ---")

        if len(expenses) == 0:
            print("No expenses recorded yet.")
        else:
            category_totals = {}

            for expense in expenses:
                category = expense["category"]

                if category in category_totals:
                    category_totals[category] += expense["amount"]
                else:
                    category_totals[category] = expense["amount"]

            for category, total in category_totals.items():
                print(f"{category}: ₹{total:.2f}")

    # Monthly Summary
    elif choice == "5":
        print("\n--- Monthly Summary ---")

        if len(expenses) == 0:
            print("No expenses recorded yet.")
        else:
            month = input("Enter month (MM-YYYY): ")

            total = 0

            for expense in expenses:
                if expense["date"][3:] == month:
                    total += expense["amount"]

            print(f"Total expense for {month}: ₹{total:.2f}")

    # Generate Graph
    elif choice == "6":
        print("\nGraph generation will be added in the next development phase.")

    # Exit
    elif choice == "7":
        print("\nThank you for using Personal Expense Tracker!")
        break

    else:
        print("Invalid choice. Please select 1 to 7.")
