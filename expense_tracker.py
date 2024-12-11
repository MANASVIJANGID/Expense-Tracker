from expense import Expense
import calendar
import datetime

def main():
    print(f"Running Expense Tracker! 🗂️")
    expense_file_path = "expenses.csv"
    budget = 5000

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    print("Getting User Expense 📝")
    expense_name = input("Enter expense name: ")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid amount: {e}. Please enter a valid number.")
    
    expense_categories = [
        "Food 🍔",
        "Home 🏠",
        "Work 💼",
        "Fun 🎉",
        "Misc 🎁",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if selected_index not in range(len(expense_categories)):
                raise IndexError("Invalid category number.")
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        except (ValueError, IndexError) as e:
            print(f"Invalid selection: {e}. Please try again!")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense 💾: {expense} to {expense_file_path}")
    try:
        with open(expense_file_path, "a", encoding="utf-8", newline="") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    except IOError as e:
        print(f"Error writing to file: {e}")

def summarize_expenses(expense_file_path, budget):
    print("Summarizing User Expenses 📊")
    expenses: list[Expense] = []
    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                )
                expenses.append(line_expense)
    except IOError as e:
        print(f"Error reading from file: {e}")
        return
    except ValueError as e:
        print(f"Error processing file data: {e}")
        return

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum(x.amount for x in expenses)
    print(f"Total Spent 💸: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining 💰: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
    else:
        daily_budget = remaining_budget  # If no days left, show the remaining budget as daily budget

    print(f"Budget Per Day 📅: ${daily_budget:.2f}")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()


