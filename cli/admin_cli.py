from rich.prompt import Prompt
from utils.display import (
    console,              
    print_error,
    admin_menu
)
from analytics.analyzer import main_analytics_management
from cli.items_category_cli import main_item_category_management
from cli.order_cli import main_order_management

# -------------------------------------------- Admin Management -------------------------------------------- #

def handle_exit():
    console.print("\n[bold green]Thanks for using Café Management System! 👋[/bold green]\n")
    exit()


def admin_main():

    actions = {
    "1": main_item_category_management,
    "2": main_order_management,
    "3": main_analytics_management,
    "0": handle_exit 
    }
         
    while True:
        print(" ")
        admin_menu()

        choice = Prompt.ask("\n👉 Select an option").strip()
        action = actions.get(choice)
        
        if action:
            action()
            input("\n[Press Enter to return to Main menu...]")
        else:
            print_error("Invalid choice. Please try again.")   
            

if __name__ == "__main__":
    admin_main()
