from models.user import Admin, Customer
from data.db import get_connection


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
            register_screen()
        elif choice == "0":
            print("Exiting the system.")
            return None
        else:
            print("Invalid selection!")


# =============== LOGIN MENU ===============
def login_menu():
    print("\n========================================")
    print("               LOGIN MENU")
    print("========================================")
    print("1. Customer")
    print("2. Admin")
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
        return None


# =============== LOGIN SCREEN ===============
def login_screen(expected_role):
    while True:
        print("\n========================================")
        print("                LOGIN")
        print("========================================")

        email = input("Email    : ").strip()
        password = input("Password : ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id, email, password, phone_number,
                   full_name, gender, address, user_name, role
            FROM users
            WHERE email = ? AND password = ?
        """, (email, password))

        row = cur.fetchone()
        conn.close()

        if not row:
            print("\nInvalid email or password!")
            continue   

        (
            user_id, email, password,
            phone_number, full_name,
            gender, address, user_name, role
        ) = row

        if role != expected_role:
            print("\nAccess denied for this role!")
            continue   

        print("\nLogin successful!")

        if role == "admin":
            return Admin(
                user_id, email, password,
                phone_number, user_name
            )
        else:
            return Customer(
                user_id, email, password,
                phone_number, full_name, gender, address
            )


# =============== REGISTER ===============
def register_screen():
    print("\n========================================")
    print("               REGISTER")
    print("========================================")

    email = input("Email        : ").strip()
    password = input("Password     : ").strip()
    full_name = input("Full name    : ").strip()
    phone = input("Phone number : ").strip()
    gender = input("Gender       : ").strip()
    address = input("Address      : ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users
            (email, password, full_name, phone_number, gender, address, role)
            VALUES (?, ?, ?, ?, ?, ?, 'customer')
        """, (email, password, full_name, phone, gender, address))

        conn.commit()
        print("\nRegistration successful!")

    except Exception as e:
        print("\nRegistration failed:", e)

    finally:
        conn.close()

# ================ UPDATE PROFILE ================
class AuthService:
    @staticmethod
    def update_profile(user_id, full_name, phone_number, gender, address):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE users
            SET full_name = ?,
                phone_number = ?,
                gender = ?,
                address = ?
            WHERE user_id = ? AND role = 'customer'
        """, (
            full_name,
            phone_number,
            gender,
            address,
            user_id
        ))

        if cur.rowcount == 0:
            conn.close()
            raise Exception("Update failed or user not found")

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def recover_password(email):
        """
        SPEC – Recover Password (Notification only)
        """
        # Không xử lý DB, chỉ giả lập
        print("\n========================================")
        print("Password Recovery")
        print("========================================")
        print(f"A password recovery request has been received for: {email}")
        print("If this email exists in the system, a recovery instruction has been sent.")
        print("Please check your email.")
        print("========================================\n")

        return True