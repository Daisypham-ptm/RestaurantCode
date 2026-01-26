from abc import ABC, abstractmethod
from data.db import get_connection



class User(ABC):
    def __init__(self, user_id, email, password, phone_number, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role = role
        
    @abstractmethod
    def login(self):
        pass

    def logout(self):
        return True
    
    def update_password(self, new_password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET password = %s WHERE user_id = %s",
            (new_password, self.user_id)
        )

        conn.commit()
        conn.close()
        return True
    

class Admin(User):
    def __init__(
            self,
            user_id, 
            email, 
            password, 
            phone_number,
            user_name,
    ):
        super().__init__(user_id, email, password, phone_number, role="admin")
        self.user_name = user_name


    def login(self):
        return True
    
    def manage_menu_item(self):
        pass

    def manage_categories(self):
        pass

    def manage_orders(self):
        pass

    def manage_users(self):
        pass

    def view_statistics(self):
        pass


class Customer(User):
    def __init__(
            self, 
            user_id,
            email,
            password,
            phone_number,
            full_name,
            gender,
            address
    ):
        super().__init__(user_id, email, password, phone_number, role="customer")
        self.full_name = full_name
        self.gender = gender
        self.address = address

    def login(self):
        return True
    
    def register(self):
        pass
    
    def update_profile(self):
        pass

    def reset_password(self):
        pass
    
    def view_order_history(self):
        pass

    def cancel_order(self):
        pass
    
    def rate_menu_item(self):
        pass

    def update_password(self, new_password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET password = ? WHERE user_id = ?",
            (new_password, self.user_id)
        )

        conn.commit()
        conn.close()

        self.password = new_password
        return True



