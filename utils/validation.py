from utils.display import console


def validate_boolean(prompt, allow_blank=True):
    while True:
        value =  input(prompt).strip().lower()

        if allow_blank and value == "":
            return None
        
        if value in ("yes", "y", "true", "1"):
            return True
        elif value in ("no", "n", "false", "0"):
            return False
        else:
            console.print("❌ [red]Please enter 'y' or 'n'.[/red]")


def validate_name(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if not value and not allow_blank:
            console.print("❌ [red]Name cannot be empty.[/red]")

        if value: return value


def validate_price(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()

        if allow_blank and raw == "":
            return None
        
        try:
            value = float(raw)
            if value > 0:
                return value
            console.print("❌ [red]Price must be greater than 0.[/red]")
        except ValueError:
            console.print("❌ [red]Please enter a valid number.[/red]")
        

def validate_category(prompt, category_list=None, allow_blank=False):
    while True:
        value = input(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if category_list:
            # Match ignoring case and spaces
            matches = [cat for cat in category_list if cat.strip().lower() == value.lower()]
            if matches:
                return matches[0]  # Return original formatted category from list
            else:
                console.print(f"❌ [red]Invalid category. Choose from: {', '.join(category_list)}[/red]")
        else:
            return value


def validate_item_id(prompt, item_dict=None, allow_blank=False):
    while True:
        value = input(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if item_dict and value not in item_dict:
            console.print(f"❌ [red]Item ID '{value}' not found.[/red]")
        else:
            return value


def get_valid_item_id(prompt, item_dict):
    item_id = input(prompt).strip()
    if item_id not in item_dict:
        console.print(f"❌ [red]Item ID '{item_id}' not found.[/red]")
        return None
    return item_id


def valid_qty(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            return None
        
        try:
            qty = int(value)
            if qty > 0:
                return qty
            console.print("❌ [red]Quantity must be greater than 0.[/red]")
        except ValueError:
            console.print("❌ [red]Please enter a valid number.[/red]")
