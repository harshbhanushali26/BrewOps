from rich.prompt import Prompt
from utils.filtering import get_name_to_id_map, filter_orders_by_criteria
from utils.display import print_section_title, print_success, print_warning, print_error, display_order_summary, display_multiple_orders_table, print_order_menu, console
from shared.order_helpers import place_order_flow as shared_place_order
from shared.managers import menu_manager, order_manager

item_name_dict = get_name_to_id_map(menu_manager.menu_items)

        
def handle_add_order():
    print_section_title("Add Order", "📝")
    shared_place_order(menu_manager, order_manager, item_name_dict, is_admin=True)


def handle_update_status():
    print_section_title("Update Status")
    
    console.print("Apply filters to get particular order and its details for updation\n")
    handle_view_all_orders("update")
    
    order_id = input("Enter Order Id: ").strip()

    if order_id not in order_manager.orders:
        print_error("Please Enter valid order Id. No such order found")
        return
    
    current_status = order_manager.orders[order_id].status
    console.print(f"Current status for this order is {current_status}")

    ask = input("Do you want to change status ? (y/n): ").strip().lower()
    if ask not in ["yes", "y"]:
        return
    
    valid_statuses = ["placed", "in progress", "completed", "cancelled"]
    console.print(f"Available status options: {', '.join(valid_statuses)}")
    
    new_status = input("Enter the status: ").strip().lower()

    if new_status not in valid_statuses:
        print_error("❌ Invalid status. Must be one of: placed, in progress, completed, cancelled.")
        return
    
    success = order_manager.update_status(order_id, new_status)

    if success:
        print_success("Order status changed successfully!")
        display_order_summary(order_manager.orders[order_id])
        
    else:
        print_error("Failed to update order status.")


def handle_mark_paid():
    print_section_title("Update Payment Status", "💳")
    
    console.print("Apply filters to get particular order and its details\n")
    handle_view_all_orders("mark_paid")
    order_id = input("Enter Order Id: ").strip()

    if order_id not in order_manager.orders:
        print_error("Invalid order ID. Please try again.")
        return
    
    order = order_manager.orders[order_id]
    payment_status = "Paid" if order.paid else "Unpaid"
    console.print(f"🔎 Current payment status: [bold yellow]{payment_status}[/bold yellow]")

    if order.paid:
        print_warning("ℹ️ This order is already marked as paid.")
        return

    ask = input("Do you want to change it ? (y/n): ").strip().lower()
    if ask not in ["yes", "y"]:
        return
    
    success = order_manager.mark_paid(order_id)

    if success:
        print_success("Payment Done!")
        display_order_summary(order_manager.orders[order_id])
        
    else:
        print_error("Failed to update payment status.")


def handle_view_order():
    print_section_title("Order Details", "📝")
    
    console.print("Apply filters to get particular order and its details.\n")
    handle_view_all_orders("view_order")
    order_id = input("Enter Order Id: ").strip()

    if order_id not in order_manager.orders:
        print_error("Invalid order ID. Please try again.")
        return
    
    display_order_summary(order_manager.orders[order_id])


def handle_view_all_orders(filter_usage=None):
    if filter_usage is None:
        print_section_title("View All Orders", icon="📦 ")
    
    console.print("You can apply the following filters: \n")
    console.print(f"• Status Filter: [green]placed, in progress, completed, cancelled[/green]")
    console.print("• Payment Filter: [green]yes / no[/green]")
    console.print("• Date Filter: YYYY-MM-DD or [Enter] to skip\n")
    console.print("\n[bold yellow]🔍  Apply Filters to Order Search[/bold yellow]")
    apply_filters = input("\nWould you like to apply filters? (y/n): ").strip().lower()
    status = paid = date = None

    if apply_filters in ["y", "yes"]:
        console.print("\n1️⃣ [bold yellow]Status Filter[/bold yellow]")
        console.print("\n[bold green]Available : placed, in progress, completed, cancelled[/bold green]")
        status = input("→ Enter status (or press Enter to skip): ").strip()
        if status == "":
            status = None

        # filter_paid = input("Would you like to apply Filter by payment status? (y/n): ").strip().lower()
        # if filter_paid in ["y", "yes"]:
        console.print("\n2️⃣ [bold yellow]Payment Filter[/bold yellow]")
        paid_input = input("→ Is the order paid? (y/n or press Enter to skip): ").strip().lower()
        paid = True if paid_input in ["y", "yes"] else False
        if paid_input == "":
            paid = None

        console.print("\n3️⃣ [bold yellow]Date Filter[/bold yellow]")
        date = input("→ Enter order date (YYYY-MM-DD) (or press Enter to skip): ").strip()
        if date == "":
            date = None

    filtered_orders = filter_orders_by_criteria(
        order_manager.orders,
        status=status,
        paid=paid,
        date=date
    )

    if not filtered_orders:
        print_warning("No orders match the selected filters.")
    else:
        print("\n \n")
        display_multiple_orders_table(filtered_orders)


def handle_remove_orders():
    print_section_title("Remove Order", "  🗑️")
    
    console.print("Apply filters to get particular order and its details for deletion\n")
    handle_view_all_orders("remove_order")
    order_id = input("Enter Order Id: ").strip()

    if order_id not in order_manager.orders:
        print_error("Invalid order ID. Please try again.")
        return

    confirm = input("Are you sure you want to delete this order? (y/n): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print("🛑 Deletion cancelled.")
        return

    success = order_manager.remove_order(order_id)

    if success:
        print_success("Order removed successfully.")
    else:
        print_error("Failed to remove order.")


def main_order_management():
    
    actions = {
    "1": handle_add_order,
    "2": handle_update_status,
    "3": handle_mark_paid,
    "4": handle_view_order,
    "5": handle_view_all_orders,
    "6": handle_remove_orders,
    "0": lambda: None 
    }

    while True:
        print(" ")
        print_order_menu()
        choice = Prompt.ask("\n👉 Select an option")
        action = actions.get(choice)

        if choice == "0":
            break

        if action:
            action()
            input("\n[Press Enter to return to  Order Management...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")