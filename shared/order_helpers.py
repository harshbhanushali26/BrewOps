# shared/order_helpers.py

from utils.display import print_error, print_success, print_warning,console, Table, box
from utils.validation import valid_qty
from datetime import datetime
from rich.prompt import Prompt
from time import sleep

"""Display order summary and calculate total"""
def display_order_confirmation(items):
    
    table = Table(title="\n🛒 Order Summary\n", show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    table.add_column("Item", style="cyan", no_wrap=True)
    table.add_column("Quantity", justify="center", style="green")
    table.add_column("Price Each", justify="right", style="yellow")
    table.add_column("Subtotal", justify="right", style="bold yellow")
    
    total = 0
    for item in items:
        subtotal = item["qty"] * item["price"]
        total += subtotal
        table.add_row(
            item["name"],
            str(item["qty"]),
            f"₹{item['price']:.2f}",
            f"₹{subtotal:.2f}"
        )
    
    # Add total row
    table.add_section()
    table.add_row("", "", "TOTAL:", f"₹{total:.2f}", style="bold green")
    
    console.print(table)
    return total


"""Ask for order confirmation"""
def confirm_order():
   
    while True:
        confirm = Prompt.ask(f"\nConfirm your order? (y/n)").lower().strip()
        if confirm in ["y", "yes"]:
            return True
        elif confirm in ["n", "no"]:
            return False
        else:
            print_error("Invalid Option, Try Again!")


"""Ask User for items and qty"""
def prompt_order_items(menu_manager, item_name_dict):
   
    items = {}
    while True:
        item_name = Prompt.ask("What would you like to order?").strip()
        item_id = item_name_dict.get(item_name.lower().strip())
        if not item_id:
            print_error("Invalid item name. Try again.")
            continue

        price = menu_manager.menu_items[item_id].price
        qty = valid_qty(f"How many {item_name}")
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
    
    customer_name = Prompt.ask("Enter customer name") if is_admin else None
    items = prompt_order_items(menu_manager, item_name_dict)
    
    # Display order summary and get confirmation
    total = display_order_confirmation(items)
    if not confirm_order():
        items = modify_order(items, menu_manager, item_name_dict)
        if not items:  # Cancelled
            return
        total = display_order_confirmation(items)

    
    timestamp = datetime.now().isoformat()
    order_id = order_manager.generate_order_id(timestamp)

    from orders.order import Order
    order = Order(items, total, "placed", timestamp, False, order_id, customer_name)
    success = order_manager.add_order(order)

    if success:
        
        if not is_admin:
            order_manager.mark_paid(order_id)
            print_success("💰 Payment successful!")
            console.print("🧑‍🍳 Preparing your order...")
            sleep(2)
            order_manager.update_status(order_id, "completed")
            print_success("✅ Your order is now completed. Enjoy your meal!")
        else:
            print_success(f"📦 Order for '{customer_name}' added.")
            print_warning("ℹ️ Admin must manually manage preparation and status updates and payment to mark as paid.")
    
        display_order_summary(order)
    else:
        print_error("❌ Failed to place order.")


def modify_order(items, menu_manager, item_name_dict):
    while True:
        console.print("\n⚙️ What would you like to do?", style="bold magenta")
        console.print("1. ➕ Add item")
        console.print("2. ➖ Remove item")
        console.print("3. ✏️ Change quantity")
        console.print("4. ❌ Cancel order completely")

        choice = Prompt.ask("Enter choice (1-4)").strip()

        if choice == "1":  # Add item
            new_items = prompt_order_items(menu_manager, item_name_dict)
            items.extend(new_items)

        elif choice == "2":  # Remove item
            item_name = Prompt.ask("Enter item name to remove").strip().lower()
            items = [i for i in items if i["name"].lower() != item_name]

        elif choice == "3":  # Change quantity
            item_name = Prompt.ask("Enter item name to update qty").strip().lower()
            for i in items:
                if i["name"].lower() == item_name:
                    new_qty = valid_qty(f"Enter new qty for {item_name}")
                    i["qty"] = new_qty
                    break
            else:
                print_error("Item not found in order.")

        elif choice == "4":  # Cancel order
            print_warning("❌ Order cancelled.")
            return None  # completely exit

        else:
            print_error("Invalid choice, try again!")
            continue

        # After modification, re-show summary
        total = display_order_confirmation(items)
        if confirm_order():
            return items  # confirmed
