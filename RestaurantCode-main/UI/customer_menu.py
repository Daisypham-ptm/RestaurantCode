from services.order import OrderService
from services.cart import Cart
from services.auth import AuthService
from services.menu import view_menu, search_menu, view_food_detail



def search_menu_ui():
    keyword = input("Enter keyword to search: ").strip()
    if not keyword:
        print("Keyword cannot be empty!")
        return

    search_menu(keyword)

def view_food_detail_ui():
    try:
        item_id = int(input("Enter Food ID to view detail: "))
    except ValueError:
        print("Invalid Food ID!")
        return

    view_food_detail(item_id)

def manage_cart_ui(cart):
    while True:
        print("\n========== MANAGE CART ==========")
        print("1. Add Item")
        print("2. Update Quantity")
        print("3. Remove Item")
        print("4. View Cart")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            food_id = int(input("Enter food ID: "))
            quantity = int(input("Enter quantity: "))
            cart.add_to_cart(food_id, quantity)

        elif choice == "2":
            food_id = int(input("Enter food ID: "))
            quantity = int(input("Enter new quantity: "))
            cart.update_cart(food_id, quantity)

        elif choice == "3":
            food_id = int(input("Enter food ID: "))
            cart.remove_from_cart(food_id)

        elif choice == "4":
            cart.view_cart()

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")


def place_order_ui(customer):
    print("\n===== PLACE ORDER =====")

    # Step 3: Receiver info
    receiver_name = input("Receiver name: ")
    address = input("Delivery address: ")

    # Step 4: Delivery method
    print("Delivery method:")
    print("1. Home Delivery")
    print("2. Store Pickup")
    delivery_choice = input("Choose: ")

    delivery_method = "Home Delivery" if delivery_choice == "1" else "Store Pickup"

    # Step 5: Payment method
    print("Payment method:")
    print("1. Cash")
    print("2. Bank Transfer")
    payment_choice = input("Choose: ")

    payment_method = "Cash" if payment_choice == "1" else "Bank Transfer"

    notes = f"""
    Receiver: {receiver_name}
    Address: {address}
    Delivery: {delivery_method}
    """

    # Step 6: IMPORT + CALL Place Order
    try:
        order_id = OrderService.place_order(
            user_id=customer.user_id,
            notes=notes,
            payment_method=payment_method
        )
        print(f"Order successful! Your Order ID is {order_id}.")
    except Exception as e:
        print("Place order failed:", e)

def make_payment_ui():
    print("\n===== MAKE PAYMENT =====")
    print("1. Pay by Cash")
    print("2. Pay by Banking")
    print("0. Cancel")

    choice = input("Choose payment method: ").strip()

    if choice == "1":
        print("\nPayment successful!")
        print("Please pay cash upon delivery.")

    elif choice == "2":
        print("\nPayment successful!")
        print("Banking payment completed.")

    elif choice == "0":
        print("\nPayment cancelled.")

    else:
        print("\nPayment failed! Invalid payment method.")

def view_order_status_ui(customer):
    print("\n===== VIEW ORDER STATUS =====")

    orders = OrderService.view_order_status(customer.user_id)

    if not orders:
        print("You have no orders yet.")
        return

    print("{:<10} {:<12} {:<12} {:<20}".format(
        "Order ID", "Status", "Total", "Order Date"
    ))
    print("-" * 60)

    for order_id, status, total, order_date in orders:
        print("{:<10} {:<12} {:<12} {:<20}".format(
            order_id, status, total, order_date
        ))

def view_order_history_ui(customer):
    print("\n===== ORDER HISTORY =====")

    history = OrderService.view_order_history(customer.user_id)

    if not history:
        print("You have no order history.")
        return

    for order in history:
        print("\n----------------------------------")
        print(f"Order ID   : {order['order_id']}")
        print(f"Status     : {order['status']}")
        print(f"Total      : {order['total_amount']}")
        print(f"Order Date : {order['order_date']}")

        print("\nItems:")
        print("{:<10} {:<10} {:<12} {:<12}".format(
            "Item ID", "Qty", "Unit Price", "Subtotal"
        ))

        print(order["items"])
        for item in order["items"]:
            item_id= item["item_id"]
            qty= item["quantity"]


            price= item["unit_price"]
            if price is None:
                price= 0

            subtotal= item["subtotal"]
            if subtotal is None:
                subtotal= qty* price
                
            print("{:<10} {:<10} {:<12} {:<12}".format(
                item_id, qty, price, subtotal
            ))

    print("\n===== END ORDER HISTORY =====")

def update_profile_ui(user):
    print("\n===== UPDATE PROFILE =====")
    full_name = input("Full name    : ")
    phone = input("Phone number : ")
    gender = input("Gender       : ")
    address = input("Address      : ")

    try:
        AuthService.update_profile(
            user.user_id,
            full_name,
            phone,
            gender,
            address
        )
        print("Profile updated successfully!")
    except Exception as e:
        print("Error:", e)

def recover_password_ui():
    print("\n===== RECOVER PASSWORD =====")
    email = input("Enter your email: ").strip()

    AuthService.recover_password(email)


def customer_menu(customer):
    while True:
        print("\n========================================")
        print("            CUSTOMER MENU")
        print("========================================")
        print("1. View Menu")
        print("2. Search Menu")
        print("3. View Food Detail")
        print("4. Manage Cart")
        print("5. Place Order")
        print("6. Make Payment")
        print("7. View Order Status")
        print("8. View Order History")
        print("9. Update Profile")
        print("10. Recover Password")
        print("0. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_menu()

        elif choice == "2":
            search_menu_ui()

        elif choice == "3":
            view_food_detail_ui()

        elif choice == "4":
            manage_cart_ui(Cart(customer.user_id))

        elif choice == "5":
            place_order_ui(customer)

        elif choice == "6":
            make_payment_ui()

        elif choice == "7":
            view_order_status_ui(customer)

        elif choice == "8":
            view_order_history_ui(customer)

        elif choice == "9":
            update_profile_ui(customer)

        elif choice == "10":
            AuthService.recover_password_ui(customer.email)

        elif choice == "0":
            print("Logout successful!")
            break

        else:
            print("Invalid choice. Please try again.")
