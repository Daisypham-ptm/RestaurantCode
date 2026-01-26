from enum import Enum
from datetime import datetime
from db import get_connection



class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Recipient:
    def __init__(self, recipient_id, full_name, address, phone_number):
        self.recipient_id = recipient_id
        self.full_name = full_name
        self.address = address
        self.phone_number = phone_number

class Order:
    def __init_(
            self,
            order_id,
            order_date,
            payment_method,
            status,
            total_amount,
            notes=""
    ):
        self.order_id = order_id
        self.order_date = order_date
        self.payment_method = payment_method
        self.status = status
        self.total_amount = 0
        self.notes = notes
        self.items = []


    def create_order(self):
        self.status = OrderStatus.PENDING
        return True
    
    def update_status(self, new_status):
        self.status = new_status
        return True
    
    def cancel_order(self):
        if self.status == OrderStatus.PENDING:
            self.status = OrderStatus.CANCELLED
            return True
        return False
    
    def calculate_total(self):
        self.total_amount = sum(item.subtotal for item in self.items)
        return self.total_amount
    

class OrderItem:
    def __init__(
            self, 
            order_item_id,
            quantity,
            unit_price,
            subtotal,
            special_request
    ):
        self.order_item_id = order_item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.special_request = special_request
        self.subtotal = subtotal

    def calculate_subtotal(self):
        return self.unit_price * self.quantity
    
class Review:
    def __init__(
            self,
            review_id,
            rating,
            review_date=datetime.now()
    ):
        self.review_id = review_id
        self.rating = rating
        self.review_date = review_date

    def submit_review(self):
        return True
    
    def update_review(self, new_rating):
        self.rating = new_rating
        return True