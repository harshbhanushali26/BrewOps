from utils.display import console
from rich.prompt import Prompt
from utils.display import print_error, datetime


def validate_boolean(prompt, allow_blank=True):
    while True:
        value =  Prompt.ask(prompt).strip().lower()

        if allow_blank and value == "":
            return None
        
        if value in ("yes", "y", "true", "1"):
            return True
        elif value in ("no", "n", "false", "0"):
            return False
        else:
            print_error("Please enter 'y' or 'n'.")


def validate_name(prompt, allow_blank=False):
    while True:
        value = Prompt.ask(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if not value and not allow_blank:
            print_error("Name cannot be empty. ")

        if value: return value


def validate_price(prompt, allow_blank=False):
    while True:
        raw = Prompt.ask(prompt).strip()

        if allow_blank and raw == "":
            return None
        
        try:
            value = float(raw)
            if value > 0:
                return value
            print_error("Price must be greater than 0. ")
        except ValueError:
            print_error("Please enter a valid number. ")
        

def validate_category(prompt, category_list=None, allow_blank=False):
    while True:
        value = Prompt.ask(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if category_list:
            # Match ignoring case and spaces
            matches = [cat for cat in category_list if cat.strip().lower() == value.lower()]
            if matches:
                return matches[0]  # Return original formatted category from list
            else:
                print_error(f"Invalid category. Choose from: {', '.join(category_list)} ")
        else:
            return value


def validate_item_id(prompt, item_dict=None, allow_blank=False):
    while True:
        value = Prompt.ask(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if item_dict and value not in item_dict:
            print_error(f"Item ID '{value}' not found. ")
        else:
            return value


def get_valid_item_id(prompt, item_dict):
    item_id = Prompt.ask(prompt).strip()
    if item_id not in item_dict:
        print_error(f"Item ID '{item_id}' not found. ")
        return None
    return item_id


def valid_qty(prompt):
    while True:
        value = Prompt.ask(prompt).strip()

        if value == "":
            return None
        
        try:
            qty = int(value)
            if qty > 0:
                return qty
            print_error("Quantity must be greater than 0.")
        except ValueError:
            print_error("Please enter a valid number.")


def validate_date(prompt, allow_blank=True):
    while True:
        value = Prompt.ask(prompt).strip()
        if allow_blank and value == "":
            return None  # user skipped

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print_error("Date must be in YYYY-MM-DD format.")
            
            
def validate_order_status(prompt, allow_blank=True):
    while True:
        value = Prompt.ask(prompt).strip()

        if allow_blank and value == "":
            return None
        
        if value in ["placed", "in progress", "completed", "cancelled"]:
            return value
        else:
            print_error(f"Invalid category. Choose from: ('placed', 'in progress', 'completed', 'cancelled')")
