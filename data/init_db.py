import sqlite3
import os

DB_PATH = "database/restaurant_menu.db"
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ===== USERS =====
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT,
    phone_number TEXT,    
    role TEXT CHECK(role IN ('admin', 'customer')) NOT NULL
);
""")

# ===== CATEGORIES =====
cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    description TEXT,
    display_order INTEGER
);
""")

# ===== MENU ITEMS =====
cur.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    item_name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    status TEXT CHECK(status IN ('available', 'out_of_stock')) NOT NULL,
    avg_rating REAL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

# ===== CART =====
cur.execute("""
CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

# ===== CART ITEMS =====
cur.execute("""
CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""") 

# ===== ORDERS =====
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method TEXT,
    status TEXT CHECK(status IN ('PENDING', 'CONFIRMED', 'PREPARING', 'SHIPPING', 'DELIVERED', 'COMPLETED', 'CANCELLED')),
    total_amount REAL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""") # order_history = SELECT * FROM orders WHERE user_id = ?

# ===== ORDER ITEMS =====
cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    subtotal REAL,
    special_request TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""")

# ===== REVIEWS =====
cur.execute("""
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""")

conn.commit()
conn.close()

print("Database initialized successfully.")

