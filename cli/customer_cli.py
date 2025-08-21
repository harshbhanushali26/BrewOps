from rich.prompt import Prompt
from utils.filtering import get_name_to_id_map
from shared.managers import menu_manager, order_manager
from shared.order_helpers import place_order_flow as shared_place_order
from utils.display import (
    print_section_title, print_error,
    console, display_order_summary,
    display_view_menu, customer_menu
)

item_name_dict = get_name_to_id_map(menu_manager.menu_items)



def handle_place_order():
    print_section_title("Place Order", "📝")
    shared_place_order(menu_manager, order_manager, item_name_dict, is_admin=False)


def handle_view_menu():
    print_section_title("Cafe Menu", icon="🍽️  ", color="cyan")
    display_view_menu(menu_manager)


def handle_view_my_order():
    print_section_title("Order Details", "ℹ️")
    order_id = input("Enter order Id: ").strip()
    if order_id not in order_manager.orders:
        print_error("Please Enter valid order Id. No such order found")
        return
    
    order = order_manager.orders[order_id]
    display_order_summary(order)


def handle_exit():
    console.print("\n[bold green]Thanks for using Café Management System! 👋[/bold green]\n")
    exit()


#main
def handle_customer_menu():
    
    actions = {
        "1": handle_view_menu,
        "2": handle_place_order,
        "3": handle_view_my_order,
        "0": handle_exit,
    }
    
    while True:
        customer_menu()
        choice = Prompt.ask("\n👉 Select an option")
        action = actions.get(choice)
        if action:
            action()
            input("\n[Press Enter to return to main menu...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid option. Please enter a valid number")


if __name__ == "__main__":
    handle_customer_menu()
