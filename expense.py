import mysql.connector
import csv
from datetime import datetime

# ---------------- Database Connection ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # change if needed
        password="pass@word1",    # change if needed
        database="expense"  ,
        use_pure=True
        # make sure this DB exists
    )

# ---------------- CRUD Functions ----------------
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food, Travel, Bills, etc): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (date, category, amount, description))
    conn.commit()
    conn.close()
    print("Expense added successfully!")


def view_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM expenses"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Expense List ---")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Description: {row[4]}")
    else:
        print("No expenses found.")


def update_expense():
    exp_id = int(input("Enter expense ID to update: "))
    new_amount = float(input("Enter new amount: "))

    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE expenses SET amount = %s WHERE id = %s"
    cursor.execute(query, (new_amount, exp_id))
    conn.commit()
    conn.close()
    print("Expense updated successfully!")


def delete_expense():
    exp_id = int(input("Enter expense ID to delete: "))

    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM expenses WHERE id = %s"
    cursor.execute(query, (exp_id,))
    conn.commit()
    conn.close()
    print("Expense deleted successfully!")


def search_expense():
    keyword = input("Enter category or description to search: ")

    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM expenses WHERE category LIKE %s OR description LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Search Results ---")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Description: {row[4]}")
    else:
        print("No matching expenses found.")


def export_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    with open("C:\\Users\\Administrator\\Desktop\\ExpenseProj\\expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        writer.writerows(rows)
        print("Data exported to expenses.csv")


# ---------------- Monthly Summary ----------------
def monthly_summary():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) 
        FROM expenses 
        GROUP BY month 
        ORDER BY month;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Monthly Expense Summary ---")
    if rows:
        for row in rows:
            print(f"Month: {row[0]}, Total Spent: {row[1]}")
    else:
        print("No expenses found.")


# ----------- Main Menu ----------- #
def main_menu():
    while True:
        print("\n===== Expense Management System =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Search Expense")
        print("6. Export Expenses to CSV")
        print("7. Monthly Summary")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            update_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            search_expense()
        elif choice == "6":
            export_expenses()
        elif choice == "7":
            monthly_summary()
        elif choice == "8":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main_menu()
