from datetime import datetime
import sqlite3
from data.db import get_connection
from models.order_review import OrderStatus


class OrderService:
    """
    Service layer for Order Processing
    Use cases:
    - Place Order
    - View Order Status
    - Cancel Order
    - View Order History
    """

    # ================= PLACE ORDER =================
    @staticmethod
    def place_order(user_id, payment_method, notes=None):
        """
        SPEC 3.7 – Place Order
        Preconditions: Cart not empty
        """
        conn = get_connection()
        cur = conn.cursor()

        # 1. Get cart
        cur.execute("SELECT cart_id FROM cart WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise Exception("Cart not found")

        cart_id = row[0]

        # 2. Get cart items + price
        cur.execute("""
            SELECT ci.item_id, ci.quantity, mi.price
            FROM cart_items ci
            JOIN menu_items mi ON ci.item_id = mi.item_id
            WHERE ci.cart_id = ?
        """, (cart_id,))
        cart_items = cur.fetchall()

        if not cart_items:
            conn.close()
            raise Exception("Cart is empty")

        # 3. Calculate total
        total_amount = sum(qty * price for _, qty, price in cart_items)

        # 4. Insert order
        cur.execute("""
            INSERT INTO orders
            (user_id, order_date, payment_method, status, total_amount, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            datetime.now(),
            payment_method,
            OrderStatus.PENDING.value,
            total_amount,
            notes
        ))

        order_id = cur.lastrowid

        # 5. Insert order items
        for item_id, quantity, price in cart_items:
            cur.execute("""
                INSERT INTO order_items
                (order_id, item_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (
                order_id,
                item_id,
                quantity,
                price,
                quantity * price
            ))

        # 6. Clear cart
        cur.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))

        conn.commit()
        conn.close()
        return order_id

    # ================= VIEW ORDER STATUS =================
    @staticmethod
    def view_order_status(user_id):
        """
        SPEC 3.9 – View Order Status
        """
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT order_id, status, total_amount, order_date
            FROM orders
            WHERE user_id = ?
            ORDER BY order_date DESC
        """, (user_id,))

        orders = cur.fetchall()
        conn.close()
        return orders

    # ================= CANCEL ORDER =================
    @staticmethod
    def cancel_order(user_id, order_id):
        """
        SPEC 3.10 – Cancel Order
        Rule: only PENDING orders can be canceled
        """
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT status
            FROM orders
            WHERE order_id = ? AND user_id = ?
        """, (order_id, user_id))

        row = cur.fetchone()
        if not row:
            conn.close()
            raise Exception("Order not found")

        if row[0] != OrderStatus.PENDING.value:
            conn.close()
            raise Exception("Only PENDING orders can be canceled")

        cur.execute("""
            UPDATE orders
            SET status = ?
            WHERE order_id = ?
        """, (OrderStatus.CANCELLED.value, order_id))

        conn.commit()
        conn.close()
        return True

    # ================= VIEW ORDER HISTORY =================
    @staticmethod
    def view_order_history(user_id):
        """
        SPEC 3.11 – View Order History
        """
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT order_id, status, total_amount, order_date
            FROM orders
            WHERE user_id = ?
            ORDER BY order_date DESC
        """, (user_id,))

        orders = cur.fetchall()
        history = []

        for order in orders:
            cur.execute("""
                SELECT 
                        item_id,
                        quantity,
                        COALESCE(unit_price, 0) AS unit_price,
                        COALESCE(subtotal, quantity* unit_price, 0) AS subtotal
                FROM order_items
                WHERE order_id= ?
            """, (order["order_id"],))

            items = cur.fetchall()

            history.append({
                "order_id": order["order_id"],
                "status": order["status"],
                "total_amount": order["total_amount"],
                "order_date": order["order_date"],
                "items": [dict(item) for item in items]
            })

            conn.close()
            return history
        
    # ================= UPDATE ORDER STATUS =================
    @staticmethod
    def update_order_status(order_id, new_status):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE orders
            SET status = ?
            WHERE order_id = ?
        """, (new_status, order_id))

        conn.commit()
        conn.close()