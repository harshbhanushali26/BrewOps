import json
import os
from utils.display import print_error, print_warning


#---------- Menu json I/O ----------#

def load_menu_data(file_path):
    if not os.path.exists(file_path):
            return {}
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print_warning("JSON file is empty or corrupted. Starting fresh.")
        return {}
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return {}


def save_menu_data(file_path, menu_data):
    if not isinstance(menu_data, dict):
        raise ValueError("Data must be a dictionary")
    try:
        with open(file_path, 'w') as file:
            json.dump(menu_data, file, indent=4)
            
    except Exception as e:
        print_error("Error to save data")


#---------- Order json I/O ----------#

def load_order_data(file_path):
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print_warning(f"Order file '{file_path}' is empty or corrupted. Starting fresh.")
        return {}
    except Exception as e:
        print_error(f"Error reading '{file_path}': {e}")
        return {}


def save_order_data(file_path, order_data):
    if not isinstance(order_data, dict):
        raise ValueError("Order data must be a dictionary")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(order_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print_error(f"Failed to save order data to '{file_path}': {e}")



#---------- Users json I/O ----------#


def load_users_data(USERS_FILE):
    # ensured for first user too
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True) # if directory or path doesn't exist it will create 
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}")
        return {}

    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        print_warning("User file is empty or invalid. Resetting it.")
        USERS_FILE.write_text("{}")
        return {}
    

def save_users_data(users, USERS_FILE):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    except Exception as e:
        print_error(f"Error saving users: {e}")
    
    