from services.auth import main_menu
import sqlite3
import os
from datetime import datetime

# Import modules
from menu import MenuManager, display_view_menu, display_search_menu, display_food_detail
from cart import Cart
from order import place_order, view_orders, cancel_order, view_order_history
from admin import admin_menu

DB_PATH = "database/restaurant_menu.db"

# ================== DATABASE SETUP ==================
def init_database():
    """Initialize database and create tables if not exist"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Categories table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            description TEXT,
            display_order INTEGER DEFAULT 0
        )
    """)
    
    # Menu items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            item_name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            status TEXT DEFAULT 'available',
            order_count INTEGER DEFAULT 0,
            avg_rating REAL DEFAULT 0.0,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cart items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            subtotal REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
        )
    """)
    
    # Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            receiver_name TEXT,
            receiver_phone TEXT,
            receiver_address TEXT,
            payment_method TEXT,
            total_amount REAL,
            order_date TIMESTAMP,
            status TEXT DEFAULT 'new',
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Order items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
        )
    """)
    
    conn.commit()
    
    # Insert sample data if tables are empty
    cur.execute("SELECT COUNT(*) FROM categories")
    if cur.fetchone()[0] == 0:
        insert_sample_data(conn, cur)
    
    conn.close()


def insert_sample_data(conn, cur):
    """Insert sample data for testing"""
    
    # Sample categories
    categories = [
        ("Appetizers", "Start your meal right", 1),
        ("Main Course", "Delicious main dishes", 2),
        ("Desserts", "Sweet endings", 3),
        ("Beverages", "Refreshing drinks", 4)
    ]
    
    cur.executemany("""
        INSERT INTO categories (category_name, description, display_order)
        VALUES (?, ?, ?)
    """, categories)
    
    # Sample menu items
    menu_items = [
        (1, "Spring Rolls", "Fresh Vietnamese spring rolls", 45000, "available"),
        (1, "Fried Wontons", "Crispy wontons with sweet chili sauce", 55000, "available"),
        (2, "Pho Bo", "Traditional beef noodle soup", 75000, "available"),
        (2, "Com Tam", "Broken rice with grilled pork", 65000, "available"),
        (2, "Bun Cha", "Grilled pork with vermicelli", 70000, "available"),
        (3, "Che Ba Mau", "Three-color dessert", 35000, "available"),
        (3, "Banh Flan", "Vietnamese caramel flan", 30000, "available"),
        (4, "Ca Phe Sua Da", "Vietnamese iced coffee", 25000, "available"),
        (4, "Tra Chanh", "Lemon tea", 20000, "available")
    ]
    
    cur.executemany("""
        INSERT INTO menu_items (category_id, item_name, description, price, status)
        VALUES (?, ?, ?, ?, ?)
    """, menu_items)
    
    # Sample admin user
    cur.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES ('admin', 'admin@restaurant.com', 'admin123', 'admin')
    """)
    
    # Sample customer user
    cur.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES ('customer', 'customer@email.com', 'customer123', 'customer')
    """)
    
    conn.commit()


# ================== AUTHENTICATION ==================
def login():
    """User login"""
    print("\nLOGIN")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT user_id, username, role, email
        FROM users
        WHERE email = ? AND password = ?
    """, (email, password))
    
    user = cur.fetchone()
    conn.close()
    
    if user:
        print("\nLogin successful!")
        return {"user_id": user[0], "username": user[1], "role": user[2], "email": user[3]}
    else:
        print("\nInvalid email or password. Please try again!")
        return None


def register():
    """User registration"""
    print("\nREGISTER NEW ACCOUNT")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Confirm Password: ").strip()
    
    if password != confirm_password:
        print("\nPasswords do not match!")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, 'customer')
        """, (username, email, password))
        conn.commit()
        print("\nRegistration successful! Please login.")
        return True
    except sqlite3.IntegrityError:
        print("\nUsername or email already exists!")
        return False
    finally:
        conn.close()


# ================== CUSTOMER MENU ==================
def customer_menu(user):
    """Customer menu interface"""
    menu_manager = MenuManager(DB_PATH)
    cart = Cart(user["user_id"])
    
    while True:
        print("\n" + "="*50)
        print("CUSTOMER MENU")
        print("="*50)
        print("1. View Menu")
        print("2. Search Menu")
        print("3. View Food Detail")
        print("4. Manage Cart")
        print("5. Place Order")
        print("6. Make Payment")
        print("7. View Order Status")
        print("8. View Order History")
        print("9. Update Profile")
        print("10. Recover Password")
        print("0. Logout")
        
        choice = input("\nPlease choose one option: ").strip()
        
        if choice == "1":
            view_menu_interface(menu_manager)
            
        elif choice == "2":
            search_menu_interface(menu_manager)
            
        elif choice == "3":
            view_food_detail_interface(menu_manager)
                
        elif choice == "4":
            manage_cart_interface(cart, user["user_id"])
            
        elif choice == "5":
            place_order(user["user_id"])
            
        elif choice == "6":
            place_order(user["user_id"])
            
        elif choice == "7":
            view_order_status_interface(user["user_id"])
            
        elif choice == "8":
            view_order_history(user["user_id"])
            
        elif choice == "9":
            update_profile(user)
            
        elif choice == "10":
            recover_password()
            
        elif choice == "0":
            print("\nLogged out successfully!")
            menu_manager.close()
            break
            
        else:
            print("\nInvalid selection!")
    
    menu_manager.close()


def view_menu_interface(menu_manager):
    """View menu by category"""
    categories = menu_manager.get_categories()
    print("\n--- CATEGORIES ---")
    print("0. All categories")
    for cat in categories:
        print(f"{cat['category_id']}. {cat['category_name']}")
    
    cat_choice = input("\nSelect category (0 for all): ").strip()
    cat_id = int(cat_choice) if cat_choice.isdigit() and cat_choice != "0" else None
    
    items = menu_manager.view_menu(cat_id)
    
    # Display menu
    print("\n" + "="*70)
    print("VIEW MENU")
    print("="*70)
    if not items:
        print("No food items found.")
    else:
        print(f"{'ID':<8} {'Name':<25} {'Price':<15} {'Status':<12}")
        print("-" * 70)
        for item in items:
            print(f"{item.item_id:<8} {item.item_name:<25} {item.price:>12,.0f} {item.status:<12}")
    
    input("\nPress Enter to continue...")


def search_menu_interface(menu_manager):
    """Search menu"""
    keyword = input("\nEnter search food by keyword: ").strip()
    items = menu_manager.search_menu(keyword)
    
    if not items:
        print("\nNo matching items found.")
    else:
        print(f"\n{'ID':<8} {'Name':<25} {'Price':<15} {'Orders':<12}")
        print("-" * 70)
        for item in items:
            print(f"{item.item_id:<8} {item.item_name:<25} {item.price:>12,.0f} Orders:{item.order_count}")
    
    input("\nPress Enter to continue...")


def view_food_detail_interface(menu_manager):
    """View food detail"""
    item_id = input("\nEnter Food ID: ").strip()
    if item_id.isdigit():
        detail = menu_manager.view_food_detail(int(item_id))
        if detail:
            print("\n" + "="*50)
            print("FOOD DETAIL")
            print("="*50)
            print(f"Name: {detail['item_name']}")
            print(f"Price: {detail['price']:,.0f}")
            print(f"Description: {detail['description']}")
            print(f"Status: {detail['status']}")
        else:
            print("\nFood item not found!")
    else:
        print("\nInvalid Food ID!")
    
    input("\nPress Enter to continue...")


def manage_cart_interface(cart, user_id):
    """Manage cart interface"""
    while True:
        print("\n" + "="*50)
        print("MANAGE CART")
        print("="*50)
        print("1. Add Item")
        print("2. Update Quantity")
        print("3. Remove Item")
        print("4. View Cart")
        print("0. Back")
        
        choice = input("\nPlease choose one option: ").strip()
        
        if choice == "1":
            try:
                food_id = int(input("Enter Food ID: "))
                quantity = int(input("Enter quantity: "))
                cart.add_to_cart(food_id, quantity)
            except ValueError:
                print("Invalid input!")
                
        elif choice == "2":
            try:
                food_id = int(input("Enter Food ID: "))
                new_qty = int(input("Enter new quantity: "))
                cart.update_cart(food_id, new_qty)
            except ValueError:
                print("Invalid input!")
                
        elif choice == "3":
            try:
                food_id = int(input("Enter Food ID to remove: "))
                cart.remove_from_cart(food_id)
            except ValueError:
                print("Invalid input!")
                
        elif choice == "4":
            view_cart_detailed(user_id)
            
        elif choice == "0":
            break
            
        else:
            print("Invalid selection!")


def view_cart_detailed(user_id):
    """View cart with detailed format"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT m.item_id, m.item_name, m.price, c.quantity, c.subtotal
        FROM cart_items c
        JOIN menu_items m ON c.item_id = m.item_id
        WHERE c.user_id = ?
    """, (user_id,))
    
    items = cur.fetchall()
    conn.close()
    
    if not items:
        print("\nYour cart is empty.")
        return
    
    print("\n" + "="*70)
    print("YOUR CART")
    print("="*70)
    print(f"{'ID':<8} {'Name':<25} {'Qty':<8} {'Price':<15} {'Subtotal':<15}")
    print("-" * 70)
    
    total = 0
    for item in items:
        print(f"{item[0]:<8} {item[1]:<25} {item[3]:<8} {item[2]:>12,.0f} {item[4]:>12,.0f}")
        total += item[4]
    
    print("-" * 70)
    print(f"Total: {total:,.0f}")
    
    input("\nPress Enter to continue...")


def view_order_status_interface(user_id):
    """View current order status"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT order_id, order_date, total_amount, status
        FROM orders 
        WHERE user_id = ? AND status IN ('new', 'preparing', 'confirmed')
        ORDER BY order_date DESC
    """, (user_id,))
    
    orders = cur.fetchall()
    conn.close()
    
    if not orders:
        print("\nNo current orders found.")
        return
    
    print("\n" + "="*70)
    print("VIEW ORDER STATUS")
    print("="*70)
    print(f"{'Order ID':<12} {'Date':<20} {'Total':<15} {'Status':<15}")
    print("-" * 70)
    
    for order in orders:
        print(f"{order[0]:<12} {order[1]:<20} {order[2]:>12,.0f} {order[3]:<15}")
    
    input("\nPress Enter to continue...")


def update_profile(user):
    """Update user profile"""
    print("\n" + "="*50)
    print("UPDATE PROFILE")
    print("="*50)
    print("Feature coming soon...")
    input("\nPress Enter to continue...")


def recover_password():
    """Recover password"""
    print("\n" + "="*50)
    print("RECOVER PASSWORD")
    print("="*50)
    print("Feature coming soon...")
    input("\nPress Enter to continue...")


# ================== MAIN PROGRAM ==================
def main():
    """Main program entry point"""
    
    # Initialize database
    init_database()
    
    while True:
        print("\n" + "="*50)
        print("RESTAURANT ORDER MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Customer")
        print("2. Administrator")
        print("0. Exit")
        
        choice = input("\nPlease choose one option: ").strip()
        
        if choice == "1":
            # Customer login
            user = login()
            if user:
                if user["role"] == "customer":
                    customer_menu(user)
                else:
                    print("\nPlease use Administrator option for admin accounts.")
                    
        elif choice == "2":
            # Admin login
            user = login()
            if user:
                if user["role"] == "admin":
                    admin_menu()
                else:
                    print("\nYou don't have administrator privileges.")
            
        elif choice == "0":
            print("\nThank you for using our system!")
            print("See you again!")
            break
            
        else:
            print("\nInvalid selection!")


if __name__ == "__main__":
    main()

main_menu()
