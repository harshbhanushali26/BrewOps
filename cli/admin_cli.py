from rich.prompt import Prompt
from utils.display import (
    console,              
    print_error,
    admin_menu,
    print_success
)
from analytics.analyzer import main_analytics_management
from cli.items_category_cli import main_item_category_management
from cli.order_cli import main_order_management
from auth.auth import AuthManager
auth_manager = AuthManager()

# -------------------------------------------- Admin Management -------------------------------------------- #

def handle_logout():
    auth_manager.session_manager.clear_session()
    auth_manager.logout()
    print_success("\nLogged out successfully!")
    print_success("\nThanks for using Café Management System! 👋\n")
    exit()


def admin_main():

    
    actions = {
    "1": main_item_category_management,
    "2": main_order_management,
    "3": main_analytics_management,
    "0": handle_logout 
    }
         
    while True:
        # Check session when returning to main menu
        if not auth_manager.session_manager.check_session_on_main_menu():
            print_error("\nSession expired. Returning to login...")
            return  # This will take them back to login
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
