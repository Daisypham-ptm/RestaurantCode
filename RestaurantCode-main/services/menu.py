from models.menu_cart import Category, MenuItem
from data.db import get_connection


class MenuItem:
    
    def __init__(self, item_id, item_name, description, price, status, category_id=None, avg_rating=0, order_count=0):
        self.item_id = item_id
        self.item_name = item_name
        self.description = description
        self.price = price
        self.status = status
        self.category_id = category_id
        self.avg_rating = avg_rating
        self.order_count = order_count

    def get_details(self):
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'avg_rating': self.avg_rating
        }

    def update_order_count(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu_items SET order_count = order_count + 1 WHERE item_id = ?",
            (self.item_id,)
        )
        conn.commit()
        conn.close()

    def calculate_avg_rating(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT AVG(rating) FROM reviews WHERE item_id = ?",
            (self.item_id,)
        )
        avg = cur.fetchone()[0]
        avg_rating = avg if avg else 0
        
        # Update avg_rating in database
        cur.execute(
            "UPDATE menu_items SET avg_rating = ? WHERE item_id = ?",
            (avg_rating, self.item_id)
        )
        conn.commit()
        conn.close()
        
        self.avg_rating = avg_rating
        return self.avg_rating


class Category:
    """Class đại diện cho danh mục món ăn"""
    
    def __init__(self, category_id, category_name, description, display_order=0):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description
        self.display_order = display_order

    def get_menu_items(self):
        """Lấy danh sách tất cả món ăn trong danh mục"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT item_id, item_name, description, price, status, category_id, avg_rating, order_count
            FROM menu_items
            WHERE category_id = ?
            ORDER BY item_name
            """,
            (self.category_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [MenuItem(*row) for row in rows]


# =========
# FUNCTIONS 
# ==========

def view_menu():
    """
    Function 1: View Menu
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, item_name, price, status
        FROM menu_items
        ORDER BY item_id
        """
    )
    items = cur.fetchall()
    conn.close()
    
    if items:
        print("\n" + "="*80)
        print(f"{'Food ID':<10} {'Name':<30} {'Price (VND)':<15} {'Status':<15}")
        print("="*80)
        for item in items:
            print(f"{item[0]:<10} {item[1]:<30} {item[2]:<15,.0f} {item[3]:<15}")
        print("="*80)
    else:
        print("\nThere are no dishes on the menu!")
    
    return items


def search_menu(keyword):
    """
    Function 2: Search Menu
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, item_name, description, price, status
        FROM menu_items
        WHERE item_name LIKE ? OR description LIKE ?
        ORDER BY item_name
        """,
        (f'%{keyword}%', f'%{keyword}%')
    )
    items = cur.fetchall()
    conn.close()
    
    if items:
        print(f"\nSearch results for '{keyword}':")
        print("="*80)
        print(f"{'Food ID':<10} {'Name':<25} {'Price (VND)':<15} {'Status':<15}")
        print("="*80)
        for item in items:
            print(f"{item[0]:<10} {item[1]:<25} {item[3]:<15,.0f} {item[4]:<15}")
        print("="*80)
    else:
        print(f"\nNo dishes found with the keyword '{keyword}'")
    
    return items


def view_food_detail(item_id):
    """
    Function 3: View Food Detail
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_name, price, description, status
        FROM menu_items
        WHERE item_id = ?
        """,
        (item_id,)
    )
    item = cur.fetchone()
    conn.close()
    
    if item:
        print("\n" + "="*60)
        print("FOOD DETAILS")
        print("="*60)
        print(f"Name           : {item[0]}")
        print(f"Price          : {item[1]:,.0f} VND")
        print(f"Description    : {item[2]}")
        print(f"Satus          : {item[3]}")
        print("="*60)
        return item
    else:
        print(f"\nNo dishes found with ID: {item_id}")
        return None


# =========================
# HELPER FUNCTIONS
# =========================

def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT category_id, category_name, description, display_order
        FROM categories
        ORDER BY display_order, category_name
        """
    )
    rows = cur.fetchall()
    conn.close()
    return [Category(*row) for row in rows]


def get_category_by_id(category_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT category_id, category_name, description, display_order
        FROM categories
        WHERE category_id = ?
        """,
        (category_id,)
    )
    row = cur.fetchone()
    conn.close()
    
    if row:
        return Category(*row)
    return None


def get_menu_item_by_id(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, item_name, description, price, status, category_id, avg_rating, order_count
        FROM menu_items
        WHERE item_id = ?
        """,
        (item_id,)
    )
    row = cur.fetchone()
    conn.close()
    
    if row:
        return MenuItem(*row)
    return None


def get_all_menu_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, item_name, description, price, status, category_id, avg_rating, order_count
        FROM menu_items
        ORDER BY item_name
        """
    )
    rows = cur.fetchall()
    conn.close()
    return [MenuItem(*row) for row in rows]


def get_available_menu_items():
    """(status = 'available')"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT item_id, item_name, description, price, status, category_id, avg_rating, order_count
        FROM menu_items
        WHERE status = 'available'
        ORDER BY item_name
        """
    )
    rows = cur.fetchall()
    conn.close()
    return [MenuItem(*row) for row in rows]


def main():
    print("=== MENU TEST ===\n")

    
    category = Category(
        category_id=1,
        category_name="Food",
        description="Food Menu"
    )

    items = category.get_menu_items()

    if not items:
        print("There are no items in this category")
        return

    print(f"List of items in categoryy '{category.category_name}':\n")

    for item in items:
        print(f"- ID: {item.item_id}")
        print(f"  Name: {item.item_name}")
        print(f"  Description: {item.description}")
        print(f"  Price: {item.price}")
        print(f"  Status: {item.status}")
        print(f"  averating rate: {item.avg_rating}")
        print("-" * 30)


if __name__ == "__main__":
    main()

