import json
import os

#---------- Menu json I/O ----------#

def load_menu_data(file_path):
    if not os.path.exists(file_path):
            return {}
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("⚠️ JSON file is empty or corrupted. Starting fresh.")
        return {}
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {}


def save_menu_data(file_path, menu_data):
    if not isinstance(menu_data, dict):
        raise ValueError("Data must be a dictionary")
    
    with open(file_path, 'w') as file:
         json.dump(menu_data, file, indent=4)


#---------- Order json I/O ----------#

def load_order_data(file_path):
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"⚠️ Order file '{file_path}' is empty or corrupted. Starting fresh.")
        return {}
    except Exception as e:
        print(f"❌ Error reading '{file_path}': {e}")
        return {}


def save_order_data(file_path, order_data):
    if not isinstance(order_data, dict):
        raise ValueError("Order data must be a dictionary")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(order_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Failed to save order data to '{file_path}': {e}")
