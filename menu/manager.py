from menu.item import MenuItem
from utils.json_io import load_menu_data, save_menu_data
from utils.filtering import filter_menu_items

class MenuManager:
    def __init__(self, file_path="data/menu.json"):
        self.file_path = file_path
        self.menu_data = {}
        self.load_menu()  


    def load_menu(self):
        raw_data = load_menu_data(self.file_path)
        self.menu_data["categories"] = raw_data.get("categories", [])
        self.menu_data["items"] = { item_id: MenuItem.from_dict(item_id, data) for item_id, data in raw_data.get("items", {}).items()}
         

    def save_menu(self):
        menu_dict = {
            "categories" : self.categories,
            "items" : {item_id : item.to_dict() for item_id, item in self.menu_items.items()}
        }
        save_menu_data(self.file_path, menu_dict)


    def add_item(self, item_detail: MenuItem):
        if not isinstance(item_detail, MenuItem):
            raise ValueError("Must be a MenuItem")
        
        if item_detail.item_id in self.menu_items:
            return False
        
        self.menu_items[item_detail.item_id] = item_detail
        self.save_menu()
        return True


    def remove_item(self, item_id):
        if item_id not in self.menu_items:
            return False
        
        del self.menu_items[item_id]
        self.save_menu()
        return True
    

    def update_item(self, item_id:str, updated_fields):
        if item_id not in self.menu_items:
            return False
        
        menu_item = self.menu_items[item_id]
        allowed_fields = {"name", "price", "available", "is_special"}

        for key, value in updated_fields.items():
            if key in allowed_fields and value is not None:
                setattr(menu_item, key, value)
        
        self.save_menu()
        return True


    def add_category(self, category_name):
        if category_name in self.categories:
            return False
        
        self.categories.append(category_name)    # it is list of categories in dictionary
        self.save_menu()
        return True


    def remove_category(self, category_name):
        category_name = category_name.strip()
        if category_name not in self.categories: 
            return False
        
        count = 0
        for item in self.menu_items.values():
            if item.category.strip().lower() == category_name.strip().lower():
                count += 1

        if count > 0:
            return False
        else:
            self.categories.remove(category_name)
            self.save_menu()
            return True


    @property
    def categories(self):
        return self.menu_data.get("categories", [])


    @property
    def menu_items(self):
        return self.menu_data.get("items", {})


    def get_item(self, item_id):
        if item_id not in self.menu_items:
            return False
        
        return self.menu_items[item_id]


    def get_all_item_objects(self):     # list of all items for cli display
        return list(self.menu_items.values())
    

    def get_all_item_dicts(self):       # dictionary or json for export/pdf
        return {
            item_id: item.to_dict()
            for item_id, item in self.menu_items.items()
        }


    def list_items_by_category(self, category_name):
        return filter_menu_items(self.menu_items, category_name, available=True)


    def generate_new_item_id(self, category_name):
        prefix = category_name.strip().lower()[:3]
        existing_numbers = []

        for item_id, item in self.menu_items.items():
            if item.category.strip().lower() == category_name.strip().lower():
                number_part = item_id.split('_')[0]
                if number_part.isdigit():
                    existing_numbers.append(int(number_part))

        next_number = max(existing_numbers, default=0) + 1
        new_id = f"{str(next_number).zfill(3)}_{prefix}"
        return new_id
        
        
    def toggle_special(self, item_id):
        if item_id not in self.menu_items:
            return False
        
        menu_item = self.menu_items[item_id]
        menu_item.is_special = not menu_item.is_special
        self.save_menu()
        return True


    def list_special_items(self):
        return filter_menu_items(self.menu_items, available=True, is_special=True)
    

    def count_items_by_category(self):
        counts = {}
        

        for item in self.menu_items.values():
            cat = item.category.strip().lower()
            counts[cat] = counts.get(cat, 0) + 1
        items_per_category = sorted(counts.items(), key=lambda x: x[0])
        return items_per_category
        
        
    def count_special_items(self):
        return sum(1 for item in self.menu_items.values() if item.is_special)
    

    def count_available_items(self):
        return sum(1 for item in self.menu_items.values() if item.available)
    
    # all time
    def get_most_ordered_items(self):
        if not self.menu_items:
            return []

        max_count = max(item.order_count for item in self.menu_items.values())
        if max_count == 0:
            return []

        return [
            item for item in self.menu_items.values()
            if item.order_count == max_count
        ]


    def increment_order_count(self, item_id: str, qty=1):
        if item_id in self.menu_items:
            self.menu_items[item_id].order_count += qty


    def decrement_order_count(self, item_id:str, qty=1):
         if item_id in self.menu_items:
            self.menu_items[item_id].order_count = max(0, self.menu_items[item_id].order_count - qty)
            
            

    
