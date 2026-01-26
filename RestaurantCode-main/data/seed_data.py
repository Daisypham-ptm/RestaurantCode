import sqlite3
import random
from db import get_connection

conn = get_connection()
cur = conn.cursor()

# ===== RESET =====
cur.execute("DELETE FROM order_items")
cur.execute("DELETE FROM orders")
cur.execute("DELETE FROM cart_items")
cur.execute("DELETE FROM menu_items")
cur.execute("DELETE FROM categories")
cur.execute("DELETE FROM users")

# ===== USERS =====
users = [
    ("admin@email.com", "123456", "Admin", "0900000000", "None", "None", "admin01","admin"),
    ("cus1@email.com", "678910", "Customer One", "0911111111", "Male", "123 Nguyen Trai, HCM", "None", "customer"),
    ("cus2@email.com", "123098", "Customer Two", "0922222222", "Female", "456 Le Loi, HCM", "None", "customer"),
]


cur.executemany("""
INSERT INTO users (email, password, full_name, phone_number, gender, address, user_name, role)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", users)

# ===== CATEGORIES (5) =====
categories = [
    ("Main Dish", "The core course of a meal, providing the main source of energy, typically made with meat, fish, or seafood.", 1),
    ("Fast Food", "Quick and convenient meals that are easy to prepare and serve, typically including burgers, fries, fried chicken, and sandwiches.", 2),
    ("Drink", "A selection of beverages served hot or cold, including soft drinks, juices, coffee, tea, and smoothies. Designed to refresh and complement meals.", 3),
    ("Dessert", "Sweet dishes served after the main meal, such as cakes, ice cream, pastries, and puddings. Perfect for ending the meal on a delightful note.", 4),
    ("Vegetarian", "Dishes made without meat or seafood, focusing on vegetables, grains, legumes, and plant-based ingredients. Suitable for vegetarians and customers seeking lighter or healthier options.", 5)
]

cur.executemany("""
INSERT INTO categories (category_name, description, display_order)
VALUES (?, ?, ?)
""", categories)

# ===== MENU ITEMS (50) =====
food_names = {
    1: ["Fried Rice", "Grilled Pork", "Beef Steak", "Chicken Rice", "Seafood Rice",
        "Fried Noodles", "Roasted Duck", "BBQ Ribs", "Pork Chop", "Fish Fillet"],
    2: ["Burger", "Cheese Burger", "French Fries", "Hot Dog", "Fried Chicken",
        "Chicken Nuggets", "Pizza Slice", "Sandwich", "Taco", "Wrap"],
    3: ["Coca Cola", "Pepsi", "Orange Juice", "Lemon Tea", "Milk Tea",
        "Black Coffee", "Latte", "Green Tea", "Smoothie", "Mineral Water"],
    4: ["Cheese Cake", "Chocolate Cake", "Ice Cream", "Pudding", "Brownie",
        "Cupcake", "Donut", "Waffle", "Pancake", "Fruit Tart"],
    5: ["Vegetarian Salad", "Tofu Stir Fry", "Veggie Soup", "Veggie Burger", "Mushroom Rice",
        "Grilled Vegetables", "Veggie Noodles", "Vegetarian Pizza", "Bean Salad", "Veggie Wrap"]
}

menu_items = []

for category_id, names in food_names.items():
    for name in names:
        menu_items.append((
            category_id,
            name,
            f"{name} description",
            random.randint(20000, 100000),
            "available",
            round(random.uniform(3.5, 5.0), 1)
        ))

cur.executemany("""
INSERT INTO menu_items
(category_id, item_name, description, price, status, avg_rating)
VALUES (?, ?, ?, ?, ?, ?)
""", menu_items)

# ===== Cart =====
cur.execute("""
INSERT INTO cart (user_id) VALUES (2)
""")
cur.execute("""
INSERT INTO cart (user_id) VALUES (3)
""")
# ===== Cart Items =====
cart_items = [
    (1, 1, 2, 40000),
    (1, 3, 1, 25000),
    (2, 4, 3, 36000)
]
cur.executemany("""
INSERT INTO cart_items
(cart_id, item_id, quantity, subtotal)
VALUES (?, ?, ?, ?)
""", cart_items)

# ===== Orders(order_history) =====
orders = [
    (2, "Cash", "COMPLETED", 45000, "No onion"),
    (2, "Cash", "CANCELLED", 30000, ""),
    (3, "Cash", "COMPLETED", 12000, "")
]

cur.executemany("""
INSERT INTO orders
(user_id, payment_method, status, total_amount, notes)
VALUES (?, ?, ?, ?, ?)
""", orders)

# ===== Order Items =====
order_items = [
    (1, 1, 20000, 20000, "Less spicy"),
    (1, 2, 25000, 25000, ""),
    (2, 3, 30000, 30000, "Extra cheese"),
    (3, 4, 12000, 12000, "No sugar")
]

cur.executemany("""
INSERT INTO order_items
(order_id, item_id, unit_price, subtotal, special_request)
VALUES (?, ?, ?, ?, ?)
""", order_items)

# ===== Review =====
reviews = [
    (2, 1, 5, "Delicious fried rice!"),
    (2, 2, 4, "Tasty burger but a bit greasy."),
    (3, 3, 5, "Refreshing orange juice."),
    (3, 4, 4, "Sweet and creamy ice cream.")
]
cur.executemany("""
INSERT INTO reviews
(user_id, item_id, rating, comment)
VALUES (?, ?, ?, ?)
""", reviews)


conn.commit()
conn.close()

print("Seed data completed.")
