# shared/order_helpers.py

from utils.display import print_error, print_success, print_warning
from utils.validation import valid_qty
from datetime import datetime
from rich.prompt import Prompt
from time import sleep

def prompt_order_items(menu_manager, item_name_dict):
   
    items = {}
    while True:
        item_name = input("What would you like to order?: ").strip()
        item_id = item_name_dict.get(item_name.lower().strip())
        if not item_id:
            print_error("Invalid item name. Try again.")
            continue

        price = menu_manager.menu_items[item_id].price
        qty = valid_qty(f"How many {item_name}:")
        if item_id in items:
            items[item_id]["qty"] += qty
        else:
            items[item_id] = {
                "item_id": item_id,
                "name": item_name,
                "qty": qty,
                "price": price
                }
    
        while True:
            more = Prompt.ask("Would you like to add anything else to your order? (y/n)").lower().strip()

            if more in ["n", "no"]:
                return list(items.values())
            elif more in ["yes", "y"]:
                break
            else:
                print_error("Invalid Option, Try Again!")         

     
def place_order_flow(menu_manager, order_manager, item_name_dict, is_admin=False):
    from utils.display import display_view_menu, display_order_summary

    display_view_menu(menu_manager)
    while True:
        to_order = Prompt.ask("Place an order? (y/n)").strip().lower()
        if to_order in ["n", "no"]:
            return
        elif to_order in ["yes", "y"]:
            break
        else:
            print_error("Invalid Option, Try Again!") 
    
    customer_name = input("Enter customer name: ") if is_admin else None
    items = prompt_order_items(menu_manager, item_name_dict)
    timestamp = datetime.now().isoformat()
    order_id = order_manager.generate_order_id(timestamp)
    total = sum(item["qty"] * item["price"] for item in items)

    from orders.order import Order
    order = Order(items, total, "placed", timestamp, False, order_id, customer_name)
    success = order_manager.add_order(order)

    if success:
        
        if not is_admin:
            order_manager.mark_paid(order_id)
            print_success("💰 Payment successful!")
            print("🧑‍🍳 Preparing your order...")
            sleep(2)
            order_manager.update_status(order_id, "completed")
            print_success("✅ Your order is now completed. Enjoy your meal!")
        else:
            print_success(f"📦 Order for '{customer_name}' added.")
            print_warning("ℹ️ Admin must manually manage preparation and status updates and payment to mark as paid.")
    
        display_order_summary(order)
    else:
        print_error("❌ Failed to place order.")
