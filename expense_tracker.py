from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

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


# ---------- HOME PAGE ----------

@app.route("/")
def index():
    expenses = load_expenses()

    total = sum(expense["amount"] for expense in expenses)

    if expenses:
        average = total / len(expenses)
    else:
        average = 0

    categories = {}

    for expense in expenses:
        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        average=average,
        categories=categories
    )


# ---------- ADD EXPENSE ----------

@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form["description"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    # Check date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date. Please use YYYY-MM-DD."

    expenses = load_expenses()

    expense = {
        "id": len(expenses) + 1,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    return redirect(url_for("index"))


# ---------- DELETE EXPENSE ----------

@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    expenses = load_expenses()

    expenses = [
        expense for expense in expenses
        if expense["id"] != expense_id
    ]

    save_expenses(expenses)

    return redirect(url_for("index"))


# ---------- SEARCH ----------

@app.route("/search")
def search():
    category = request.args.get("category", "").lower()

    expenses = load_expenses()

    results = [
        expense for expense in expenses
        if expense["category"].lower() == category
    ]

    return render_template(
        "index.html",
        expenses=results,
        total=sum(e["amount"] for e in results),
        average=(
            sum(e["amount"] for e in results) / len(results)
            if results else 0
        ),
        categories={}
    )


# ---------- START FLASK ----------

if __name__ == "__main__":
    app.run(debug=True)
