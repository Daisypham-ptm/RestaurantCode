from db import get_connection


class Category:
    def __init__(self, category_id, category_name, description, display_order=0):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description
        self.display_order = display_order

    def get_menu_item(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM menu_items WHERE category_id = %s",
            (self.category_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [MenuItem(*row) for row in rows]
    

class MenuItem:
    def __init__(
            self,
            item_id,
            item_name,
            description,
            price,
            status,
            avg_rating=0
    ):
        self.item_id = item_id
        self.item_name = item_name
        self.description = description
        self.price = price
        self.status = status
        self.avg_rating = avg_rating

    def get_details(self):
        return self
    
    def update_order_count(self, quantity):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu_items SET order_count = order_count + %s WHERE item_id = %s",
            (quantity, self.item_id)
        )

        conn.commit()
        conn.close()

    def calculate_avg_rating(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT AVG(rating) FROM reviews WHERE item_id = %s",
            (self.item_id,)
        )
        avg = cur.fetchone()[0]
        conn.close()
        self.avg_rating = avg if avg is not None else 0
        return self.avg_rating
    

class Cart:
    def __init__(self, cart_id, created_at):
        self.cart_id = cart_id
        self.created_at = created_at

    def add_item(self, cart_item):
        pass

    def remove_item(self, cart_item):
        pass

    def clear(self):
        pass

    def get_total_price(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT SUM(subtotal) FROM cart_items WHERE user_id = %s",
            (self.cart_id,)
        )

        total = cur.fetchone()[0] or 0
        conn.close()
        return total
    

class CartItem:
    def __init__(self, cart_item_id, quantity, subtotal):
        self.cart_item_id = cart_item_id
        self.quantity = quantity
        self.subtotal = subtotal

    def calculate_subtotal(self, price):
        self.subtotal = self.quantity * price
        return self.subtotal
        