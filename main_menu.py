
from cli.customer_cli import handle_customer_menu
from utils.display import print_header, console, print_error
from cli.admin_auth_cli import main_auth_management

from rich.prompt import Prompt



    
def main_menu():
    print_header()

    while True:
        console.print("[bold cyan]1.[/bold cyan] 💻⚙️  Admin")
        console.print("[bold cyan]2.[/bold cyan] 👤  Customer")
        console.print("[bold cyan]0.[/bold cyan] 🚪  Exit")

        role = Prompt.ask("Select an option")

        if role == "1":
            main_auth_management()
        elif role == "2":
            handle_customer_menu()
        elif role == "0":
            break
        else: 
            print_error("Invalid Option, Try again!")
