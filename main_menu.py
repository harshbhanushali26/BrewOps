from cli.admin_cli import admin_main
from cli.customer_cli import handle_customer_menu
from utils.display import print_header, display_dashboard, console, print_error, datetime, date
from utils.filtering import filter_by_month
from analytics.analyzer import get_menu_insights
from rich.prompt import Prompt
from datetime import timedelta
from collections import Counter

from collections import defaultdict
from shared.managers import menu_manager, order_manager


def get_todays_insights(target_date:str):

    item_counts  = defaultdict(int)
    hour_counter = Counter()
    total_orders = 0
    total_revenue = 0.00
    avg_order_value = 0.00
    peak_hour = ""

    filtered_orders = order_manager.filter_orders(status=None, paid=None, date=target_date)

    # total orders
    # completed orders with peak time
    all_items = menu_manager.menu_items
    for order in filtered_orders.values():
        
        if order.status == "completed":
            
            ts = order.timestamp
            hour = datetime.fromisoformat(ts).hour
            hour_counter[hour] += 1
            
            total_orders += 1
            total_revenue += order.total_amount
            
            for item in order.items:
                item_id = item["item_id"]
                item_name = all_items[item_id].name
                item_counts[item_name] += item["qty"]
            
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
            
    # Get top item 
    if item_counts:
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        top_item = top_items[0][0]
    else:
        top_item = "No items sold"
        
    # Get peak hour
    if hour_counter:
        peak_hour_num = hour_counter.most_common(1)[0][0]
        next_hour = (peak_hour_num + 1) % 24
        peak_hour = f"{peak_hour_num:02d} - {next_hour:02d}"
    else:
        peak_hour = "No peak hour data"
            
    return {
        "total_orders" : total_orders,
        "total_revenue" : total_revenue,
        "avg_order_value" : avg_order_value,
        "top_item" : top_item,
        "peak_hour" : peak_hour   
    }
        

def get_monthly_insights(target_month):
    
    count_map_top_items = defaultdict(int)
    total_orders = 0
    total_revenue = 0.00
    avg_order_value = 0.00
    
    filtered_orders = filter_by_month(order_manager.orders, target_month)
    
    all_items = menu_manager.menu_items
    for order in filtered_orders.values():
        
        if order.status == "completed":
            
            total_orders += 1
            total_revenue += order.total_amount
            
            for item in order.items:
                item_id = item["item_id"]
                item_name = all_items[item_id].name
                count_map_top_items[item_name] += item["qty"]
    
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    
    if count_map_top_items:
        top_items = sorted(count_map_top_items.items(), key=lambda x: x[1], reverse=True)
        bottom_items = sorted(count_map_top_items.items(), key=lambda x: x[1])
        
        top_item = top_items[0][0]
        bottom_1 = bottom_items[0][0]
        bottom_2 = bottom_items[1][0] if len(bottom_items) > 1 else "-"
    else:
        top_item = "No sales"
        bottom_1 = "No sales" 
        bottom_2 = "No sales"
    
    return {
        "total_orders" : total_orders,
        "total_revenue" : total_revenue,    
        "avg_order_value" : avg_order_value, # Avg. Daily Revenue
        "top_item" : top_item,
        "least_item" : bottom_1,
        "second_least_item" : bottom_2
    }
    

def get_weekly_sales_details():
    
    weekly_summary = []
    total_revenue = 0.00
    
    for i in range(7):
        target_date = date.today() - timedelta(days=i)
        target_date_str = str(target_date)
        filtered_orders = {}
        try:
            filtered_orders = order_manager.filter_orders(status=None, paid=None, date=target_date_str)
        except Exception as e:
            # Log error and continue with empty orders for this day
            filtered_orders = {}
            continue
        # filtered_orders = order_manager.filter_orders(status=None, paid=None, date=target_date_str)

        per_day_orders = 0
        per_day_revenue = 0.00
        weekday = target_date.strftime("%A")
        
        for order in filtered_orders.values():
            if order.status == "completed":
                per_day_orders += 1
                per_day_revenue += order.total_amount
        
        total_revenue += per_day_revenue

        weekly_summary.append({
            "date": target_date_str,
            "weekday": weekday,
            "per_day_orders": per_day_orders,
            "per_day_revenue": per_day_revenue
        })

    daily_avg = total_revenue / 7 if total_revenue > 0 else 0.00    
    
    return {
        "daily_avg" : daily_avg,
        "total_revenue" : total_revenue,
        "weekly_summary" : weekly_summary
    }
        
    
def handle_dashboard():
    today_date = date.today()
    current_year_month = datetime.today().strftime("%Y-%m")
    today_summary = get_todays_insights(today_date.strftime("%Y-%m-%d"))
    month_summary = get_monthly_insights(current_year_month)
    menu_summary = get_menu_insights()
    weekly_insights = get_weekly_sales_details()
    
    display_dashboard(today_summary, month_summary, menu_summary, weekly_insights)
    
    
    
def main_menu():
    print_header()

    while True:
        console.print("[bold cyan]1.[/bold cyan] 💻⚙️  Admin")
        console.print("[bold cyan]2.[/bold cyan] 👤  Customer")
        console.print("[bold cyan]0.[/bold cyan] 🚪  Exit")

        role = Prompt.ask("Select an option")

        if role == "1":
            handle_dashboard()
            admin_main()
        elif role == "2":
            handle_customer_menu()
        elif role == "0":
            break
        else: 
            print_error("Invalid Option, Try again!")
