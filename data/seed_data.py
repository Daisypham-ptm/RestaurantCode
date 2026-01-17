import sqlite3
import random

conn = sqlite3.connect("database/restaurant_menu.db")
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
    ("admin@email.com", "123456", "admin"),
    ("customer1@email.com", "123456", "customer"),
    ("customer2@email.com", "123456", "customer")
]

cur.executemany("""
INSERT INTO users (username, password, role)
VALUES (?, ?, ?)
""", users)

# ===== CATEGORIES (5) =====
categories = [
    ("Main Dish", "The core course of a meal, providing the main source of energy, typically made with meat, fish, or seafood."),
    ("Fast Food", "Quick and convenient meals that are easy to prepare and serve, typically including burgers, fries, fried chicken, and sandwiches."),
    ("Drink", "A selection of beverages served hot or cold, including soft drinks, juices, coffee, tea, and smoothies. Designed to refresh and complement meals."),
    ("Dessert", "Sweet dishes served after the main meal, such as cakes, ice cream, pastries, and puddings. Perfect for ending the meal on a delightful note."),
    ("Vegetarian", "Dishes made without meat or seafood, focusing on vegetables, grains, legumes, and plant-based ingredients. Suitable for vegetarians and customers seeking lighter or healthier options.")
]

cur.executemany("""
INSERT INTO categories (category_name, description)
VALUES (?, ?)
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

conn.commit()
conn.close()

print("Seed data completed: users, categories, menu items.")
