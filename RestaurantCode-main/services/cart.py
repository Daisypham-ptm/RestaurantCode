from data.db import get_connection

class Cart:
    """Cart Management Class"""
    
    def __init__(self, user_id):
        self.user_id = user_id

    def get_or_create_cart_id(self, cur):
        
        cur.execute("SELECT cart_id FROM cart WHERE user_id = ?", (self.user_id,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            cur.execute("INSERT INTO cart (user_id) VALUES (?)", (self.user_id,))
            return cur.lastrowid

    # ================== ADD ITEM TO CART ==================
    def add_to_cart(self, food_id, quantity):
        """Add item to cart"""
        conn = get_connection()
        cur = conn.cursor()

        # Check if food exists
        cur.execute("SELECT item_name, price, status FROM menu_items WHERE item_id = ?", (food_id,))
        food = cur.fetchone()

        if not food:
            print("\nFood not found!")
            conn.close()
            return False

        food_name, price, status = food
        if status != 'available':
            print(f"\n{food_name} is currently unavailable!")
            conn.close()
            return False

        # LẤY CART_ID CỦA USER
        cart_id = self.get_or_create_cart_id(cur)
        subtotal = price * quantity

        # Check if item already exists in cart_items using cart_id
        cur.execute("""
            SELECT cart_item_id, quantity 
            FROM cart_items 
            WHERE cart_id = ? AND item_id = ?
        """, (cart_id, food_id))

        existing = cur.fetchone()

        if existing:
            cart_item_id, old_qty = existing
            new_qty = old_qty + quantity
            new_subtotal = new_qty * price
            cur.execute("""
                UPDATE cart_items 
                SET quantity = ?, subtotal = ? 
                WHERE cart_item_id = ?
            """, (new_qty, new_subtotal, cart_item_id))
            print(f"\n✓ Updated {food_name} quantity to {new_qty}")
        else:
            cur.execute("""
                INSERT INTO cart_items (cart_id, item_id, quantity, subtotal)
                VALUES (?, ?, ?, ?)
            """, (cart_id, food_id, quantity, subtotal))
            print(f"\n✓ Added {food_name} to cart (Qty: {quantity})")

        conn.commit()
        conn.close()
        return True

    # ================== UPDATE ITEM QUANTITY ==================
    def update_cart(self, food_id, new_quantity):
        """Update item quantity in cart"""
        conn = get_connection()
        cur = conn.cursor()

        if new_quantity <= 0:
            print("\n✗ Quantity must be greater than 0!")
            conn.close()
            return False

        # JOIN để kiểm tra món có trong giỏ của user không
        cur.execute("""
            SELECT ci.cart_item_id, m.item_name, m.price
            FROM cart_items ci
            JOIN menu_items m ON ci.item_id = m.item_id
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.user_id = ? AND ci.item_id = ?
        """, (self.user_id, food_id))
        
        result = cur.fetchone()
        if not result:
            print("\n✗ Item not found in cart!")
            conn.close()
            return False

        cart_item_id, item_name, price = result
        new_subtotal = price * new_quantity

        cur.execute("""
            UPDATE cart_items SET quantity = ?, subtotal = ? WHERE cart_item_id = ?
        """, (new_quantity, new_subtotal, cart_item_id))

        conn.commit()
        conn.close()
        print(f"\n✓ Updated {item_name} quantity to {new_quantity}")
        return True

    # ================== REMOVE ITEM FROM CART ==================
    def remove_from_cart(self, food_id):
        """Remove item from cart"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.item_name, ci.cart_id
            FROM cart_items ci
            JOIN menu_items m ON ci.item_id = m.item_id
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.user_id = ? AND ci.item_id = ?
        """, (self.user_id, food_id))
        
        result = cur.fetchone()
        if not result:
            print("\n✗ Item not found in cart!")
            conn.close()
            return False

        item_name, cart_id = result

        cur.execute("DELETE FROM cart_items WHERE cart_id = ? AND item_id = ?", (cart_id, food_id))

        conn.commit()
        conn.close()
        print(f"\n✓ Removed {item_name} from cart")
        return True

    # ================== VIEW CART ==================
    def view_cart(self):
        """View cart contents"""
        conn = get_connection()
        cur = conn.cursor()

        # JOIN 3 bảng để lấy đủ thông tin của user_id
        cur.execute("""
            SELECT m.item_id, m.item_name, m.price, ci.quantity, ci.subtotal
            FROM cart_items ci
            JOIN menu_items m ON ci.item_id = m.item_id
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.user_id = ?
            ORDER BY m.item_name
        """, (self.user_id,))

        items = cur.fetchall()
        conn.close()

        if not items:
            print("\n" + "="*70 + "\nYOUR CART\n" + "="*70 + "\nYour cart is empty.\n" + "="*70)
            return

        print("\n" + "="*70 + "\nYOUR CART\n" + "="*70)
        print(f"{'ID':<6} {'Name':<28} {'Qty':<6} {'Price':<14} {'Subtotal':<14}")
        print("-" * 70)

        total = 0
        for item in items:
            item_id, name, price, qty, subtotal = item
            print(f"{item_id:<6} {name:<28} {qty:<6} {price:>11,.0f} {subtotal:>11,.0f}")
            total += subtotal

        print("-" * 70 + f"\n{'Total:':<46} {total:>11,.0f}\n" + "="*70)

    # ================== CALCULATE TOTAL ==================
    def calculate_total(self):
        """Calculate total amount in cart"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(ci.subtotal)
            FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.user_id = ?
        """, (self.user_id,))

        total = cur.fetchone()[0]
        conn.close()
        return total if total else 0

    # ================== CLEAR CART ==================
    def clear_cart(self):
        """Clear all items from cart"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM cart_items 
            WHERE cart_id = (SELECT cart_id FROM cart WHERE user_id = ?)
        """, (self.user_id,))

        conn.commit()
        conn.close()
        print("\n✓ Cart cleared successfully")

    # ================== GET CART ITEM COUNT ==================
    def get_item_count(self):
        """Get number of items in cart"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(ci.cart_item_id)
            FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.user_id = ?
        """, (self.user_id,))

        count = cur.fetchone()[0]
        conn.close()
        return count
   