import sqlite3
import random

conn = sqlite3.connect("data/restaurant_menu.db")
cur = conn.cursor()

# RESET DATA
cur.execute("DELETE FROM order_items")
cur.execute("DELETE FROM orders")
cur.execute("DELETE FROM cart_items")
cur.execute("DELETE FROM menu_items")
cur.execute("DELETE FROM categories")
cur.execute("DELETE FROM users")

#USERS
users = [
    ("admin@email.com", "123456", "admin"),
    ("customer1@email.com", "678910", "customer"),
    ("customer2@email.com", "987654", "customer")
]

cur.executemany("""
INSERT INTO users (username, password, role)
VALUES (?, ?, ?)
""", users)

#CATEGORIES
categories = [
    ("Main Dish", "Main course dishes"),
    ("Fast Food", "Quick and easy meals"),
    ("Drink", "Beverages and drinks"),
    ("Dessert", "Sweet treats"),
    ("Vegetarian", "Vegetarian options")
]

cur.executemany("""
INSERT INTO categories (category_name, description)
VALUES (?, ?)
""", categories)

#MENU_ITEMS
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
item_id = 1

for category_id, names in food_names.items():
    for name in names:
        menu_items.append((
            category_id,
            name,
            f"{name} description",
            random.randint(15000, 100000),
            "available",
            round(random.uniform(3.5, 5.0), 1)
        ))
        item_id += 1

cur.executemany("""
INSERT INTO menu_items
(category_id, item_name, description, price, status, avg_rating)
VALUES (?, ?, ?, ?, ?, ?)
""", menu_items)

conn.commit()
conn.close()

print("Seed data completed: 3 users, 5 categories, 50 menu items.")