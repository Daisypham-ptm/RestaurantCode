from models.user import Admin, Customer
from db import get_connection


# =============== MAIN MENU ===============
def main_menu():
    while True:
        print("\n========================================")
        print("   RESTAURANT ORDER MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        print("----------------------------------------")

        choice = input("Please choose one option: ").strip()

        if choice == "1":
            return login_menu()
        elif choice == "2":
            return register_menu()
        elif choice == "0":
            print("Exiting the system.")
            return None
        else:
            print("Invalid selection!")
        

# =============== LOGIN MENU ===============
def login_menu():
    print("\n========================================")
    print("   RESTAURANT ORDER MANAGEMENT SYSTEM")
    print("========================================")
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    print("----------------------------------------")

    choice = input("Please choose role: ").strip()

    if choice == "1":
        return login_screen(expected_role="customer")
    elif choice == "2":
        return login_screen(expected_role="admin")
    elif choice == "0":
        return None
    else:
            print("Invalid selection!")


# =============== LOGIN INPUT ===============
def login_screen(expected_role):
    print("\n========================================")
    print("                LOGIN")
    print("========================================")

    email = input("Email    : ").strip()
    password = input("Password : ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, username, password, role
        FROM users
        WHERE username = ? AND password = ?
    """, (email, password))

    row = cur.fetchone()
    conn.close()

    if not row:
        print("\nInvalid email or password. Please try again!")
        return None

    user_id, email, password, role = row

    if role != expected_role:
        print("\nAccess denied for this role")
        return None

    print("\nLogin successful")

    if role == "admin":
        return Admin(user_id, email, password)
    else:
        return Customer(user_id, email, password)
    

# =============== REGISTER ===============
def register_screen():
    print("\n========================================")
    print("              REGISTER")
    print("========================================")

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (email, password, role)
            VALUES (%s, %s, 'customer')
        """, (email, password))

        conn.commit()
        print("\nRegistration successful.")
    
    except:
        print("\nRegistration failed. Email may already be in use.")

    finally:
        conn.close()