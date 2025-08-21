from rich.prompt import Prompt
from utils.display import analytics_menu, print_error,display_multiple_summary, display_menu_summary
from utils.filtering import filter_by_month
from collections import defaultdict
from shared.managers import menu_manager, order_manager

def get_daily_summary(orders: dict, menu_items: dict, target_date=None):

    total_orders = 0
    total_revenue = 0.0

    one_day_orders = order_manager.filter_orders(status=None, paid=None, date=target_date)
    
    for order in one_day_orders.values():
        total_orders += 1
        total_revenue += order.total_amount   
        
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    
    top_items, least_items = get_top_and_least_ordered_items(orders, menu_items,  3, 2, is_date=True, target_date=target_date, month=None)
    top_cat_by_orders, top_cat_by_revenue = top_categories(orders, menu_items, is_date=True, target_date=target_date, month=None)
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "top_items": top_items,
        "least_items": least_items,
        "best_category_by_orders": (
        top_cat_by_orders[:2] if len(top_cat_by_orders) > 1 and top_cat_by_orders[0][1] == top_cat_by_orders[1][1]
        else top_cat_by_orders[0] if top_cat_by_orders else None
        ),
        "best_category_by_revenue": (
        top_cat_by_revenue[:2] if len(top_cat_by_revenue) > 1 and top_cat_by_revenue[0][1] == top_cat_by_revenue[1][1]
        else top_cat_by_revenue[0] if top_cat_by_revenue else None
        ),
    }


def get_monthly_summary(orders: dict, menu_items:dict, month):

    total_orders = 0
    total_revenue = 0.0
    
    month_orders = filter_by_month(orders, month)
    
    for order in month_orders.values():
        total_orders += 1
        total_revenue += order.total_amount
        
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    
    top_items, least_items = get_top_and_least_ordered_items(orders, menu_items, 5, 5, is_date=False,target_date=None, month=month)
    top_cat_by_orders, top_cat_by_revenue = top_categories(orders, menu_items, is_date=False, target_date=None, month=month)
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "top_items": top_items,
        "least_items": least_items,
        "best_category_by_orders": (
        top_cat_by_orders[:2] if len(top_cat_by_orders) > 1 and top_cat_by_orders[0][1] == top_cat_by_orders[1][1]
        else top_cat_by_orders[0] if top_cat_by_orders else None
        ),
        "best_category_by_revenue": (
    top_cat_by_revenue[:2] if len(top_cat_by_revenue) > 1 and top_cat_by_revenue[0][1] == top_cat_by_revenue[1][1]
    else top_cat_by_revenue[0] if top_cat_by_revenue else None
        ),
    }


def get_top_and_least_ordered_items(orders: dict, menu_items: dict,  top_n=5, bottom_n=5, is_date=True,  target_date=None, month=None):
    count_map = defaultdict(int)
    
    
    if is_date:
        daily_orders = order_manager.filter_orders(status=None, paid=None, date=target_date)
        for order in daily_orders.values():
            for item in order.items:
                item_id = item["item_id"]
                item_name = menu_items[item_id].name
                count_map[item_name] += item["qty"]
                
    else: 
        monthly_orders = filter_by_month(orders, month)
        for order in monthly_orders.values():
            for item in order.items:
                item_id = item["item_id"]
                item_name = menu_items[item_id].name
                count_map[item_name] += item["qty"]
    
    top_items = sorted(count_map.items(), key=lambda x: x[1], reverse=True)  # top n ordered items in tuple form (item, count)
    bottom_items = sorted(count_map.items(), key=lambda x: x[1]) # least n ordered items
    return top_items[:top_n] if top_items else [], bottom_items[:bottom_n] if bottom_items else []


def top_categories(orders: dict, menu_items: dict, is_date=True, target_date=None, month=None):
   
    top_category_order_count_map = defaultdict(int)
    top_category_revenue_map = defaultdict(float)
    
    
    if is_date:
        daily_orders = order_manager.filter_orders(status=None, paid=None, date=target_date)
        
        for order in daily_orders.values():
            for item in order.items:
                item_id = item["item_id"] # get item id from order
                category = menu_items[item_id].category # get category using item id from item data
                
                top_category_order_count_map[category] += item["qty"] 
                top_category_revenue_map[category] = top_category_revenue_map[category] + (item["qty"] * item["price"])
    
    else:
        monthly_orders = filter_by_month(orders, month)
        
        for order in monthly_orders.values():
            for item in order.items:
                item_id = item["item_id"] # get item id from order
                category = menu_items[item_id].category # get category using item id from item data
                
                top_category_order_count_map[category] += item["qty"] 
                top_category_revenue_map[category] = top_category_revenue_map[category] + (item["qty"] * item["price"])
            
    top_categories_by_order_count = sorted(top_category_order_count_map.items(), key=lambda x: x[1], reverse=True)
    top_categories_by_revenue = sorted(top_category_revenue_map.items(), key=lambda x: x[1], reverse=True)
    
    return top_categories_by_order_count[:3] if top_categories_by_order_count else [], top_categories_by_revenue[:3] if top_categories_by_revenue else []
 

def get_menu_insights():
    total_items = len(menu_manager.menu_items)
    total_categories = len(menu_manager.categories)
    available_count = menu_manager.count_available_items()
    special_count = menu_manager.count_special_items()
    category_wise_items = menu_manager.count_items_by_category()
    
    category_wise_orders = order_per_category(order_manager.orders, menu_manager.menu_items)
    
    return {
        "total_items" : total_items,
        "total_categories" : total_categories,
        "available_count" : available_count,
        "special_count" : special_count,
        "category_wise_items" : category_wise_items,
        "category_wise_orders" : category_wise_orders if category_wise_orders else []
    }
    

def order_per_category(orders, menu_items):
    category_map = defaultdict(int)
    for order in orders.values():
        for item in order.items:
            item_id = item["item_id"] # get item id from order
            category = menu_items[item_id].category # get category using item id from item data
            category_map[category] += item["qty"] # for particular category counting ordered items
    order_per_categories = sorted(category_map.items(), key=lambda x: x[1], reverse=True)
    return order_per_categories   


def main_analytics_management():
    while True:
        print(" ")
        analytics_menu()

        choice = Prompt.ask("\n👉 Select an option")

        if choice == "1":
            target_date = input("Enter date (YYYY-MM-DD): ").strip()
            if not target_date:
                print_error("Date cannot be empty")
                return

            daily_summary = get_daily_summary(order_manager.orders, menu_manager.menu_items, target_date)
            display_multiple_summary(daily_summary)
        
        elif choice == "2":
            month = input("Enter month (YYYY-MM): ").strip()
            
            monthly_summary = get_monthly_summary(order_manager.orders, menu_manager.menu_items, month)
            display_multiple_summary(monthly_summary)
              
        elif choice == "3":
            summary = get_menu_insights()
            display_menu_summary(summary)
            
        elif choice == "0":
            break

        else:
            print_error("Invalid choice. Please try again.")
        
        input("\n[Press Enter to return to analytics menu...]")
 
        
if __name__ == "__main__":
    main_analytics_management()
