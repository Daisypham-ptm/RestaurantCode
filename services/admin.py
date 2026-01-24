import sqlite3

DB_PATH = "database/restaurant_menu.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

def input_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Invalid number, please enter again.")


def input_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Invalid number, please enter again.")


def input_yes_no(msg):
    while True:
        c = input(msg + " (y/n): ").strip().lower()
        if c == "y":
            return True
        if c == "n":
            return False
        print("Invalid choice, please enter y or n.")


def input_status():
    while True:
        s = input("Status (a = available, o = out_of_stock): ").strip().lower()
        if s == "a":
            return "available"
        if s == "o":
            return "out_of_stock"
        print("Invalid status, please enter a or o.")


def continue_or_back():
    while True:
        print("\n1. Continue")
        print("0. Back")
        c = input("Choose: ").strip()
        if c == "1":
            return True
        if c == "0":
            return False
        print("Invalid choice.")

def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Manage Menu Items")
        print("2. Manage Categories")
        print("3. Manage Orders")
        print("4. Manage Users")
        print("5. View Reports")
        print("0. Exit")

        c = input("Select option: ").strip()
        if c == "1":
            manage_menu_items()
        elif c == "2":
            manage_categories()
        elif c == "3":
            manage_orders()
        elif c == "4":
            manage_users()
        elif c == "5":
            view_reports()
        elif c == "0":
            break
        else:
            print("Invalid choice.")

def manage_menu_items():
    while True:
        print("\n===== MANAGE MENU ITEMS =====")
        print("1. View Menu Items")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("0. Back")

        c = input("Choose: ").strip()
        if c == "1":
            view_menu_items()
        elif c == "2":
            add_menu_item()
        elif c == "3":
            update_menu_item()
        elif c == "4":
            delete_menu_item()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


def view_menu_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_id, item_name, price, status FROM menu_items")
    rows = cur.fetchall()
    conn.close()

    print("\n--- MENU ITEMS ---")
    for r in rows:
        print(f"ID:{r[0]} | Name:{r[1]} | Price:{r[2]} | Status:{r[3]}")
    input("\nPress Enter to continue...")


def add_menu_item():
    while True:
        category_id = input_int("Category ID: ")
        name = input("Item name: ").strip()
        desc = input("Description: ").strip()
        price = input_float("Price: ")
        status = input_status()

        if not input_yes_no("Confirm add item"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO menu_items
            (category_id, item_name, description, price, status, avg_rating)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (category_id, name, desc, price, status))
        conn.commit()
        conn.close()

        print("Menu item added successfully.")

        if not continue_or_back():
            break


def update_menu_item():
    while True:
        view_menu_items()
        item_id = input_int("Item ID: ")
        name = input("New name: ").strip()
        desc = input("New description: ").strip()
        price = input_float("New price: ")
        status = input_status()

        if not input_yes_no("Confirm update item"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE menu_items
            SET item_name=?, description=?, price=?, status=?
            WHERE item_id=?
        """, (name, desc, price, status, item_id))
        conn.commit()
        conn.close()

        print("Menu item updated.")

        if not continue_or_back():
            break


def delete_menu_item():
    while True:
        view_menu_items()
        item_id = input_int("Item ID to delete: ")

        if not input_yes_no("Confirm delete item"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM menu_items WHERE item_id=?", (item_id,))
        conn.commit()
        conn.close()

        print("Menu item deleted.")

        if not continue_or_back():
            break

def manage_categories():
    while True:
        print("\n===== MANAGE CATEGORIES =====")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Update Category")
        print("4. Delete Category")
        print("0. Back")

        c = input("Choose: ").strip()
        if c == "1":
            view_categories()
        elif c == "2":
            add_category()
        elif c == "3":
            update_category()
        elif c == "4":
            delete_category()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


def view_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name, description FROM categories")
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        print(f"ID:{r[0]} | Name:{r[1]} | Desc:{r[2]}")
    input("\nPress Enter to continue...")


def add_category():
    while True:
        name = input("Category name: ").strip()
        desc = input("Description: ").strip()

        if not input_yes_no("Confirm add category"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO categories (category_name, description) VALUES (?, ?)",
            (name, desc),
        )
        conn.commit()
        conn.close()

        print("Category added.")

        if not continue_or_back():
            break


def update_category():
    while True:
        view_categories()
        cid = input_int("Category ID: ")
        name = input("New name: ").strip()
        desc = input("New description: ").strip()

        if not input_yes_no("Confirm update category"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE categories SET category_name=?, description=? WHERE category_id=?",
            (name, desc, cid),
        )
        conn.commit()
        conn.close()

        print("Category updated.")

        if not continue_or_back():
            break


def delete_category():
    while True:
        view_categories()
        cid = input_int("Category ID: ")

        if not input_yes_no("Confirm delete category"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM categories WHERE category_id=?", (cid,))
        conn.commit()
        conn.close()

        print("Category deleted.")

        if not continue_or_back():
            break

def manage_orders():
    while True:
        print("\n===== MANAGE ORDERS =====")
        print("1. View Orders")
        print("2. Update Order Status")
        print("0. Back")

        c = input("Choose: ").strip()
        if c == "1":
            view_orders()
        elif c == "2":
            update_order_status()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


def view_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id, user_id, total_amount, status FROM orders")
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        print(f"ID:{r[0]} | User:{r[1]} | Total:{r[2]} | Status:{r[3]}")
    input("\nPress Enter to continue...")


def update_order_status():
    while True:
        view_orders()
        oid = input_int("Order ID: ")
        status = input("New status: ").strip().upper()

        if not input_yes_no("Confirm update order status"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status=? WHERE order_id=?", (status, oid))
        conn.commit()
        conn.close()

        print("Order status updated.")

        if not continue_or_back():
            break


def manage_users():
    while True:
        print("\n===== MANAGE USERS =====")
        print("1. View Users")
        print("2. Update User")
        print("3. Delete User")
        print("0. Back")

        c = input("Choose: ").strip()
        if c == "1":
            view_users()
        elif c == "2":
            update_user()
        elif c == "3":
            delete_user()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


def view_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, email, full_name, phone_number, role FROM users")
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        print(f"ID:{r[0]} | Email:{r[1]} | Name:{r[2]} | Phone:{r[3]} | Role:{r[4]}")
    input("\nPress Enter to continue...")


def update_user():
    while True:
        view_users()
        uid = input_int("User ID: ")
        email = input("New email: ").strip()
        name = input("New full name: ").strip()
        phone = input("New phone: ").strip()
        role = input("New role (admin/customer): ").strip()

        if not input_yes_no("Confirm update user"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users
            SET email=?, full_name=?, phone_number=?, role=?
            WHERE user_id=?
        """, (email, name, phone, role, uid))
        conn.commit()
        conn.close()

        print("User updated.")

        if not continue_or_back():
            break


def delete_user():
    while True:
        view_users()
        uid = input_int("User ID: ")

        if not input_yes_no("Confirm delete user"):
            print("Cancelled.")
            if not continue_or_back():
                break
            continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id=?", (uid,))
        conn.commit()
        conn.close()

        print("User deleted.")

        if not continue_or_back():
            break

def view_reports():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(total_amount) FROM orders WHERE status='COMPLETED'")
    revenue = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT mi.item_name, SUM(oi.quantity)
        FROM order_items oi
        JOIN menu_items mi ON oi.item_id = mi.item_id
        GROUP BY mi.item_name
        ORDER BY SUM(oi.quantity) DESC
        LIMIT 1
    """)
    best = cur.fetchone()

    conn.close()

    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: {revenue}")
    if best:
        print(f"Best Selling Item: {best[0]} ({best[1]} sold)")
    else:
        print("Best Selling Item: None")

    input("\nPress Enter to continue...")


if __name__ == "__main__":
    admin_menu()
