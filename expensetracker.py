import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "expenses.db"
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    return conn
def add_expense(conn):
    try:
        amount = float(input("Enter amount: ₹"))
        category = input("Enter category: ").strip()

        date = input("Enter date (YYYY-MM-DD): ").strip()

        # Validate date
        datetime.strptime(date, "%Y-%m-%d")

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses(amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date),
        )

        conn.commit()
        print("Expense added successfully.\n")

    except Exception as e:
        print("Error:", e)
def view_expenses(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, category, date
        FROM expenses
        ORDER BY date DESC
    """)

    data = cursor.fetchall()

    if not data:
        print("No expenses found.\n")
        return

    print("\n--- All Expenses ---")

    for amount, category, date in data:
        print(f"₹{amount:<10} | {category:<15} | {date}")

    print()
def filter_category(conn):
    category = input("Enter category: ")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, date
        FROM expenses
        WHERE category=?
    """, (category,))

    rows = cursor.fetchall()

    if not rows:
        print("No records found.\n")
        return

    print(f"\nCategory: {category}")

    total = 0

    for amount, date in rows:
        total += amount
        print(f"₹{amount} | {date}")

    print("Total =", total, "\n")
def monthly_total(conn):
    month = input("Enter month (YYYY-MM): ")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE substr(date,1,7)=?
    """, (month,))

    total = cursor.fetchone()[0]

    print(f"\nTotal spent in {month}: ₹{total or 0}\n")
def summary_report(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)

    total = cursor.fetchone()[0] or 0

    print("\n===== SUMMARY REPORT =====")
    print(f"Total Spent: ₹{total:.2f}\n")

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()

    print("Category Breakdown")

    for cat, amt in rows:
        print(f"{cat}: ₹{amt:.2f}")

    print()
def visualize(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()

    if not data:
        print("No data available.\n")
        return

    categories = [x[0] for x in data]
    values = [x[1] for x in data]

    plt.figure(figsize=(8, 8))

    plt.pie(
        values,
        labels=categories,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")

    plt.show()
def menu():
    conn = connect_db()

    while True:

        print("""
====== EXPENSE TRACKER ======

1. Add Expense
2. View Expenses
3. Filter by Category
4. Monthly Total
5. Summary Report
6. Visualize Expenses
7. Exit

============================
""")

        choice = input("Choose: ")

        if choice == "1":
            add_expense(conn)

        elif choice == "2":
            view_expenses(conn)

        elif choice == "3":
            filter_category(conn)

        elif choice == "4":
            monthly_total(conn)

        elif choice == "5":
            summary_report(conn)

        elif choice == "6":
            visualize(conn)

        elif choice == "7":
            conn.close()
            print("Goodbye.")
            break

        else:
            print("Invalid option\n")


if __name__ == "__main__":
    menu()