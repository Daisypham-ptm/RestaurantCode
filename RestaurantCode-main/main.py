from services.auth import main_menu
from services.cart import Cart
from services.order import OrderService
from services.admin import admin_menu
from models.user import Admin, Customer
from UI.customer_menu import customer_menu
     

# ================= MAIN =================
def main():
    while True:
        user = main_menu()

        if user is None:
            break

        if user.role == "admin":
            admin_menu()
        else:
            customer_menu(user)


if __name__ == "__main__":
    main()


