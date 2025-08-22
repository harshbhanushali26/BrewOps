from rich.prompt import Prompt
from utils.filtering import get_name_to_id_map, filter_orders_by_criteria, filter_by_month
from utils.display import print_section_title, print_success, print_warning, print_error, display_order_summary, display_multiple_orders_table, print_order_menu, console, datetime
from shared.order_helpers import place_order_flow as shared_place_order
from utils.validation import validate_date, validate_order_status, validate_boolean
from shared.managers import menu_manager, order_manager

item_name_dict = get_name_to_id_map(menu_manager.menu_items)

        
def handle_add_order():
    print_section_title("Add Order", "📝")
    shared_place_order(menu_manager, order_manager, item_name_dict, is_admin=True)


def handle_update_status():
    print_section_title("Update Status")
    
    console.print("Apply filters to get particular order and its details for updation\n")
    # handle_view_all_orders("update")
    handle_filter_and_view_all_orders("update")
    
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
    # handle_view_all_orders("mark_paid")
    handle_filter_and_view_all_orders("mark_paid")
    
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
    # handle_view_all_orders("view_order")
    handle_filter_and_view_all_orders("view_order")
    order_id = input("Enter Order Id: ").strip()

    if order_id not in order_manager.orders:
        print_error("Invalid order ID. Please try again.")
        return
    
    display_order_summary(order_manager.orders[order_id])


# def handle_view_all_orders(filter_usage=None):
#     if filter_usage is None:
#         print_section_title("View All Orders", icon="📦 ")
    
#     console.print("You can apply the following filters: \n")
#     console.print(f"• Status Filter: [green]placed, in progress, completed, cancelled[/green]")
#     console.print("• Payment Filter: [green]yes / no[/green]")
#     console.print("• Date Filter: YYYY-MM-DD or [Enter] to skip\n")
#     console.print("\n[bold yellow]🔍  Apply Filters to Order Search[/bold yellow]")
#     apply_filters = input("\nWould you like to apply filters? (y/n): ").strip().lower()
#     status = paid = date = None

#     if apply_filters in ["y", "yes"]:
#         console.print("\n1️⃣ [bold yellow]Status Filter[/bold yellow]")
#         console.print("\n[bold green]Available : placed, in progress, completed, cancelled[/bold green]")
#         status = input("→ Enter status (or press Enter to skip): ").strip()
#         if status == "":
#             status = None

#         # filter_paid = input("Would you like to apply Filter by payment status? (y/n): ").strip().lower()
#         # if filter_paid in ["y", "yes"]:
#         console.print("\n2️⃣ [bold yellow]Payment Filter[/bold yellow]")
#         paid_input = input("→ Is the order paid? (y/n or press Enter to skip): ").strip().lower()
#         paid = True if paid_input in ["y", "yes"] else False
#         if paid_input == "":
#             paid = None

#         console.print("\n3️⃣ [bold yellow]Date Filter[/bold yellow]")
#         date = input("→ Enter order date (YYYY-MM-DD) (or press Enter to skip): ").strip()
#         if date == "":
#             date = None

#     filtered_orders = filter_orders_by_criteria(
#         order_manager.orders,
#         status=status,
#         paid=paid,
#         date=date
#     )

#     if not filtered_orders:
#         print_warning("No orders match the selected filters.")
#     else:
#         print("\n \n")
#         display_multiple_orders_table(filtered_orders)


def handle_remove_orders():
    print_section_title("Remove Order", "  🗑️")
    
    console.print("Apply filters to get particular order and its details for deletion\n")
    # handle_view_all_orders("remove_order")
    handle_filter_and_view_all_orders("remove_order")
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

     
def sort_orders(transactions, sort_by="date", order="asc"):
    """
    Sort transactions by date or total_amount
    
    Args:
        transactions: Dict of {transaction_id: transaction_object}
        sort_by: "date" or "total_amount"
        order: "asc" or "desc"
    
    Returns:
        List of sorted transaction objects (values only)
    """
    try:
        # Convert dict values to list for sorting
        txn_list = list(transactions.values())
        
        if sort_by == "date":
            sorted_txns = sorted(
                txn_list, 
                key=lambda txn: datetime.strptime(txn.timestamp, "%Y-%m-%d").date(),
                reverse=(order == "desc")
            )
        elif sort_by == "total amount":
            sorted_txns = sorted(
                txn_list,
                key=lambda txn: float(txn.total_amount),
                reverse=(order == "desc")
            )
        else:
            print_warning(f"Invalid sort option: {sort_by}")
            return txn_list
        
        return sorted_txns
        
    except Exception as e:
        print_warning(f"Error sorting transactions: {e}")
        return list(transactions.values())


def get_sort_choice():
    """
    Get sorting preference from user
    
    Returns:
        tuple: (sort_by, order) or (None, None) if no sorting
    """
    console.print(f"\n[bold yellow]Sort Options[/bold yellow]")
    sort_by = Prompt.ask("Sort by", choices=["date", "total amount", "none"], default="none")
    
    if sort_by == "none":
        return None, None
    
    order = Prompt.ask("Order", choices=["asc", "desc"], default="asc")
    return sort_by, order


def handle_filter_and_view_all_orders(filter_usage=None):
    
    if filter_usage is None:
        print_section_title("View All Orders", icon="📦 ")
    
    status = paid = None
    date_filter = from_date = to_date = month_filter = None
    current_month = datetime.now().strftime("%Y-%m")
    
    
    # only date filters and sort by amount only if possible
    console.print("Press [bold green]Enter[/bold green] to for current month orders or apply custom filters")
    apply_filters = Prompt.ask("Apply filters?", choices=["yes", "no"], default="no").lower().strip()
    
    if apply_filters == "no":
        # Default: current month
        month_filter = current_month
        orders = filter_by_month(order_manager.orders, month_filter)
        filter_summary = f"Month: {month_filter}"
   
    else:
        
        # Step 2: Ask for date filters first
        console.print(f"\n[bold yellow]Date Filters[/bold yellow]")
        date_filter_choice = Prompt.ask(
            "Apply date filter?", 
            choices=["exact", "range", "month", "no"], 
            default="no"
        )
        
        if date_filter_choice == "exact":
            date_filter = validate_date("Enter exact date (YYYY-MM-DD)", allow_blank=False)
            
        elif date_filter_choice == "range":
            from_date = validate_date("From date (YYYY-MM-DD)", allow_blank=False)
            to_date = validate_date("To date (YYYY-MM-DD)", allow_blank=False)
        
        elif date_filter_choice == "month":
            month_filter = Prompt.ask("Enter month (YYYY-MM)", default=current_month)

        # Step 3: Ask for type and category filters
        console.print(f"\n[bold yellow]Other Filters[/bold yellow]")
        status = validate_order_status("Enter Status (or press Enter to skip) - ('placed', 'in progress', 'completed', 'cancelled')", allow_blank=True)
                    
        paid = validate_boolean("Is the order paid? (y/n or press Enter to skip)", allow_blank=True)
        
        orders = filter_orders_by_criteria(
            order_manager.orders,
            status=status,
            paid=paid,
            date=date_filter,
            from_date=from_date,
            to_date=to_date,
            month=month_filter
        )
    
        filters_applied = []
        if status: filters_applied.append(f"Order Status: {status}")
        if paid: filters_applied.append(f"Order Paid: {paid}")
        if date_filter: filters_applied.append(f"Date: {date_filter}")
        elif from_date and to_date: filters_applied.append(f"Range: {from_date} to {to_date}")
        elif month_filter: filters_applied.append(f"Month: {month_filter}")
        
        filter_summary = " | ".join(filters_applied) if filters_applied else "No filters"

    
    if not orders:
        print_warning("No Orders found with applied filters.")
        return 
    
    # Show initial results
    order_list = list(orders.values())
    console.print(f"\n[bold green]📋 Applied Filters: {filter_summary}[/bold green]")
    print_success(f"[green]Found {len(orders.values()  )} orders[/green]")

  
    # Get sorting choice
    sort_by, order = get_sort_choice()

    if sort_by:
        # Pass the dict, get back sorted list
        order_list = sort_orders(orders, sort_by, order)
        
        order_text = "ascending ↑" if order == "asc" else "descending ↓"
        console.print(f"\n[bold cyan]📈 Results sorted by {sort_by} ({order_text}):[/bold cyan]")
    else:
        order_list = list(orders.values())
        console.print(f"\n[bold cyan]📋 Results:[/bold cyan]")
        
    print("\n \n")
    display_multiple_orders_table(order_list)
        





def main_order_management():
    
    actions = {
    "1": handle_add_order,
    "2": handle_update_status,
    "3": handle_mark_paid,
    "4": handle_view_order,
    "5": handle_filter_and_view_all_orders,
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
            
