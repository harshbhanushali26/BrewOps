from rich.prompt import Prompt
from utils.validation import validate_category, validate_boolean, validate_name, validate_price, get_valid_item_id
from utils.filtering import filter_menu_items
from utils.display import show_item_category_main_menu, menu_views_summary_menu, manage_categories_menu, manage_items_menu, print_section_title, print_error, print_warning, display_menu_items, print_success, console
from shared.managers import menu_manager
from menu.item import MenuItem



#==================================== Menu View and Filter handlers ===================================#

def handle_menu_view_and_filter_options():
    
    actions = {
    "1": handle_view_menu,
    "2": handle_view_special_items,
    "3": handle_filter_items,
    "0": lambda: None 
    }
         
    while True:
        print(" ")
        menu_views_summary_menu()

        choice = Prompt.ask("\n👉 Select an option").strip()
        action = actions.get(choice)

        if choice == "0":
            break

        if action:
            action()
            input("\n[Press Enter to return to Menu View and Filter...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")   
            

def handle_view_menu():
    
    print_section_title("Full menu", '📋')
    items = sorted(menu_manager.get_all_item_objects(), key=lambda x: x.name.lower())
    display_menu_items(items, title="📋  Menu Items")
    console.print(f"\n[bold cyan]Total Items Found:[/bold cyan] {len(items)}\n")


def handle_view_special_items(): 
    
    print_section_title("Special Items", "🌟")
    items = menu_manager.list_special_items().values()
    display_menu_items(items, title="🌟  Special Items List")
    console.print(f"\n[bold cyan]Total Items Found:[/bold cyan] {len(items)}\n")


def handle_filter_items(filter_usage=None):
    if filter_usage is None:
        print_section_title("Filter Menu Items", icon="🔍  ", color="blue")

    if not menu_manager.menu_items:
        print_warning("No items in the menu to filter.")
        return

    # ✅ Show available filters
    console.print("[bold cyan]You can apply the following filters:[/bold cyan]")
    console.print(f"• Category: [green]{', '.join(menu_manager.categories)}[/green]")
    console.print("• Available: [green]yes / no[/green]")
    console.print("• Special: [green]yes / no[/green]\n")
    
    apply_filters = input("\nWould you like to apply filters? (y/n): ").strip().lower()
    category = available = is_special = None
    
    if apply_filters in ['y', 'yes']:
        # 📝 Prompt user (blank to skip)
        console.print("\n1️⃣ [bold yellow]Category Filter[/bold yellow]")
        category = validate_category("→ Enter category (or press Enter to skip): ", category_list=menu_manager.categories, allow_blank=True)
        
        console.print("\n2️⃣ [bold yellow]Item Available Filter[/bold yellow]")
        available = validate_boolean("→ Is Item Available? (y/n or press Enter to skip): ", allow_blank=True)
        
        console.print("\n3️⃣ [bold yellow]Special Item Filter[/bold yellow]")
        is_special = validate_boolean("→ Is Special Item (y/n or press Enter to skip): ", allow_blank=True)

    filtered_items = filter_menu_items(
        menu_manager.menu_items,
        category=category,
        available=available,
        is_special=is_special
    )

    if not filtered_items:
        print_warning("No items matched your filter criteria.")
        return
    print("\n \n")
    display_menu_items(filtered_items.values(), "🔍  Filtered Menu Items")
    console.print(f"\n[bold cyan]Total Items Found:[/bold cyan] {len(filtered_items)}\n")


#==================================== Manage Items handlers ===================================#


def handle_manage_items_options():
    
    actions = {
    "1": handle_add_item,
    "2": handle_update_item,
    "3": handle_remove_item,
    "4": handle_toggle_special,
    "0": lambda: None 
    }
         
    while True:
        print(" ")
        manage_items_menu()

        choice = Prompt.ask("\n👉 Select an option").strip()
        action = actions.get(choice)

        if choice == "0":
            break

        if action:
            action()
            input("\n[Press Enter to return to Manage Items...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")   
            

def handle_add_item():
    
    print_section_title("Add New Item", icon="➕  ")

    if not menu_manager.categories:
        print_warning("No categories found. Please add a category first.")
        return

    console.print(f"[bold cyan]Available Categories:[/bold cyan] {', '.join(menu_manager.categories)}")

    name = validate_name("Enter item name", allow_blank=False)
    category = validate_category("Enter item category",  category_list=menu_manager.categories, allow_blank=False)
    price = validate_price("Enter price (₹)", allow_blank=False)
    available = validate_boolean("Is the item available? (y/n)", allow_blank=False)
    is_special = validate_boolean("Is this a special item? (y/n)", allow_blank=False)
    order_count = 0 

    item_id = menu_manager.generate_new_item_id(category)
    item = MenuItem(category, name, price, available, is_special, order_count, item_id)
    success = menu_manager.add_item(item)
    
    if success:
        print_success("Item added successfully!!")
        display_menu_items([item], title="🆕 Item Details")
    else:
        print_error("Failed to add Item")


def handle_update_item():

    print_section_title("Update Item", icon="✏️", color="yellow")

    if not menu_manager.menu_items:
        print_warning("No items available to update.")
        return
    
    console.print("Apply filters to get particular item and its details for updation\n")
    handle_filter_items("Update")

    # update 
    item_id = get_valid_item_id("Enter item ID to update", menu_manager.menu_items)
    if not item_id:
        return

    print_warning("Category cannot be updated. To change category, create a new item.")

    new_name = validate_name("Enter name to update OR [Skip or leave it blank]", allow_blank=True)
    new_price = validate_price("Enter price to update OR [Skip or leave it blank]", allow_blank=True)
    change_available = validate_boolean("Enter (y/n) to update its availability OR [Skip or leave it blank]", allow_blank=True)
    change_is_special = validate_boolean("Enter (y/n) to update is_special OR[Skip or leave it blank]", allow_blank=True)

    updated_fields = {
        "name": new_name,
        "price": new_price,
        "available": change_available,
        "is_special": change_is_special
    }

    # Remove any fields that are still None (i.e., user skipped them)
    updated_fields = {k: v for k, v in updated_fields.items() if v is not None}

    # if user accidently skip all fields 
    if not updated_fields:
        print_warning("No fields were updated.")
        return
    
    # re-confirm
    confirm = validate_boolean(f"Are you sure you want to update item '{item_id}'? (y/n)", allow_blank=False)
    if not confirm:
        print_warning("Cancelled item updation.")
        return
    
    success = menu_manager.update_item(item_id, updated_fields)

    if success:
        print_success(f"Item '{item_id}' updated successfully.")
    else:
        print_error("Failed to update item.")


def handle_remove_item():
    
    print_section_title("Remove Item", icon="🗑️   ", color="red")

    # no items
    if not menu_manager.menu_items:
        print_warning("No items available to delete.")
        return
    
    # id display before removing    
    console.print("Apply filters to get particular item and its details for deletion\n")
    handle_filter_items("remove")
    
    item_id = get_valid_item_id("Enter item ID to delete", menu_manager.menu_items)
    if not item_id:
        return  # early exit if not valid
    
    # re-confirm
    confirm = validate_boolean(f"Are you sure you want to delete item '{item_id}'? (y/n)", allow_blank=False)
    if not confirm:
        print_warning("Cancelled item removal.")
        return

    success = menu_manager.remove_item(item_id)

    if success:
        print_success(f"Item '{item_id}' removed successfully.")
    else:
        print_error("Failed to remove item.")


def handle_toggle_special():
    
    print_section_title("Toggle Special", icon="🔄", color="red")
    
    # display all special items for details
    handle_view_special_items()
    item_id = get_valid_item_id("Enter item ID to change speciality", menu_manager.menu_items)
    if not item_id:
        return  # early exit if not valid
    
    # getting current special status
    item = menu_manager.get_item(item_id)
    console.print(f"Current special status of '{item.name}' is: [bold yellow]{item.is_special}[/bold yellow]")

    # re-confirm
    confirm = validate_boolean(
    f"Do you want to toggle the special status of item '{item_id}' ({'Yes' if item.is_special else 'No'})? (y/n): ", allow_blank=False)

    if not confirm:
        print_warning("Cancelled toggle of special staus.")
        return
    
    success = menu_manager.toggle_special(item_id)

    if success:
        print_success(f"Item '{item_id}' special status changed successfully.")
    else:
        print_error("Failed to toggle special status.")



#==================================== Manage Categories handlers ===================================#


def handle_manage_category_options():
    
    actions = {
    "1": handle_add_category,
    "2": handle_remove_category,
    "0": lambda: None 
    }
         
    while True:
        print(" ")
        manage_categories_menu()

        choice = Prompt.ask("\n👉 Select an option").strip()
        action = actions.get(choice)

        if choice == "0":
            break

        if action:
            action()
            input("\n[Press Enter to return to Manage Category...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")   


def handle_add_category():
    
    print_section_title("Add New Category", icon="➕")

    existing = [cat.lower() for cat in menu_manager.categories]
    if menu_manager.categories:
        console.print(f"[cyan]Available Categories:[/cyan] {', '.join(menu_manager.categories)}")

    category_name = Prompt.ask("Enter category to add").strip()

    if not category_name:
        print_warning("Category name cannot be empty.")
        return

    if category_name.lower() in existing:
        print_warning(f"Category '{category_name}' already exists (case-insensitive match).")
        return

    success = menu_manager.add_category(category_name)
    if success:
        print_success(f"Category '{category_name}' added successfully.")
    else:
        print_error("Failed to add category.")


def handle_remove_category():
    print_section_title("Remove Category", icon="🗑️", color="red")

    categories = menu_manager.categories
    if not categories:
        print_warning("No categories available to remove.")
        return
    
    console.print(f"[cyan]Available Categories:[/cyan] {', '.join(categories)}")
    category_name = Prompt.ask("Enter category to remove").strip()

    if not category_name:
        print_warning("Category name cannot be empty.")
        return

    confirm = validate_boolean(f"Are you sure you want to delete category '{category_name}'? (y/n)", allow_blank=False)
    if not confirm:
        print_warning("Cancelled category removal.")
        return
    
    success = menu_manager.remove_category(category_name)

    if success:
        print_success(f"Category '{category_name}' removed successfully.")
    else:
        print_error(f"Cannot remove category '{category_name}'. It may not exist or is still used by items.")


#==================================== main ===================================#


def main_item_category_management():
    
    actions = {
    "1": handle_menu_view_and_filter_options,
    "2": handle_manage_items_options,
    "3": handle_manage_category_options,
    "0": lambda: None 
    }
         
    while True:
        print(" ")
        show_item_category_main_menu()

        choice = Prompt.ask("\n👉 Select an option").strip()
        action = actions.get(choice)

        if choice == "0":
            break

        if action:
            action()
            input("\n[Press Enter to return to Item and Category Management...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")   
           

if __name__ == "__main__":
    main_item_category_management()

