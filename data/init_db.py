import sqlite3

conn = sqlite3.connect("data/restaurant_menu.db")
cur = conn.cursor()

#USERS
cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
    );
    """)

#CATEGORIES
cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT,
    description TEXT
);
""")

#MENU_ITEMS
cur.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    item_name TEXT,
    description TEXT,
    price REAL,
    status TEXT,
    avg_rating REAL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

#CART_ITEMS
cur.execute("""
CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""")

#ORDERS
cur.execute(""")
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

#ORDER_ITEMS
cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    price REAL,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")
