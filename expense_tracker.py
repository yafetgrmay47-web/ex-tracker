import json
from datetime import datetime

FILE_NAME = "expenses.json"


# ---------- FILE HANDLING ----------

def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- ADD EXPENSE ----------

def add_expense(expenses):
    description = input("Description: ")

    while True:
        try:
            amount = float(input("Amount: €"))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    category = input("Category: ")

    while True:
        date = input("Date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

    expense = {
        "id": len(expenses) + 1,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("\nExpense added successfully!")


# ---------- VIEW EXPENSES ----------

def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<5}{'Description':<20}{'Amount':<12}{'Category':<18}{'Date'}")
    print("-" * 70)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['description']:<20}"
            f"€{expense['amount']:<11.2f}"
            f"{expense['category']:<18}"
            f"{expense['date']}"
        )

    print("=" * 70)


# ---------- SEARCH ----------

def search_expenses(expenses):
    category = input("Enter category to search: ").lower()

    results = []

    for expense in expenses:
        if expense["category"].lower() == category:
            results.append(expense)

    if not results:
        print("\nNo expenses found for that category.")
        return

    print(f"\nExpenses in category: {category}")

    for expense in results:
        print(
            f"{expense['description']} - "
            f"€{expense['amount']:.2f} - "
            f"{expense['date']}"
        )


# ---------- STATISTICS ----------

def show_statistics(expenses):
    if not expenses:
        print("\nNo expenses available.")
        return

    total = sum(expense["amount"] for expense in expenses)
    average = total / len(expenses)

    categories = {}

    for expense in expenses:
        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    print("\n===== STATISTICS =====")

    print(f"\nTotal spent: €{total:.2f}")
    print(f"Average expense: €{average:.2f}")

    print("\nSpending by category:")

    for category, amount in categories.items():
        print(f"{category}: €{amount:.2f}")


# ---------- DELETE ----------

def delete_expense(expenses):
    if not expenses:
        print("\nNo expenses to delete.")
        return

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)

            print("\nExpense deleted!")
            return

    print("\nExpense ID not found.")


# ---------- MENU ----------

def main():
    expenses = load_expenses()

    while True:
        print("\n")
        print("=" * 30)
        print("     EXPENSE TRACKER")
        print("=" * 30)

        print("1. Add expense")
        print("2. View expenses")
        print("3. Search expenses")
        print("4. Show statistics")
        print("5. Delete expense")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            search_expenses(expenses)

        elif choice == "4":
            show_statistics(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please choose 1-6.")


# ---------- START PROGRAM ----------

if __name__ == "__main__":
    main()