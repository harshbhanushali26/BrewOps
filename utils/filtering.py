from datetime import date, datetime

def filter_by_category(menu_items: dict, category: str) -> dict:
    return { item_id : item for item_id, item in menu_items.items() if item.category == category }


def filter_by_available(menu_items: dict, available: bool) -> dict:
    return { item_id : item for item_id, item in menu_items.items() if item.available == available }


def filter_by_special(menu_items: dict, is_special: bool) -> dict:
    return { item_id : item for item_id, item in menu_items.items() if item.is_special == is_special }


def filter_menu_items(menu_items: dict, category=None, available=None, is_special=None):
    
    filtered = menu_items

    if category:
        filtered = filter_by_category(filtered, category)
    
    if available is not None:
        filtered = filter_by_available(filtered, available)

    if is_special is not None:
        filtered = filter_by_special(filtered, is_special)

    return filtered

#---------- Filters for Order ----------#

def filter_orders_by_criteria(orders: dict, status=None, paid=None, date=None, from_date=None, to_date=None, month=None) -> dict:
    filtered_orders = orders

    if status:
        filtered_orders = filter_by_status(filtered_orders, status)

    if paid is not None:  # use explicit check to allow False
        filtered_orders = filter_by_paid(filtered_orders, paid)

    if date:
        filtered_orders = filter_by_date(filtered_orders, date)
    
    elif from_date and to_date:  # Only apply date range if exact date is not specified
        filtered_orders = filter_by_date_range(filtered_orders, from_date, to_date)
    
    elif month:  # Only apply month filter if no date filters are applied
        filtered_orders = filter_by_month(filtered_orders, month)


    return filtered_orders


def filter_by_status(orders: dict, status: str) -> dict:
    return {
        order_id: order for order_id, order in orders.items()
        if order.status == status
    }


def filter_by_paid(orders: dict, paid: bool) -> dict:
    return {
        order_id: order for order_id, order in orders.items()
        if order.paid == paid
    }


def filter_by_date(orders: dict, date: str) -> dict:
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    return {
        order_id: order for order_id, order in orders.items()
        if datetime.fromisoformat(order.timestamp).date() == target_date
    }


def filter_by_month(orders: dict, month: str) -> dict:
    return {
        order_id: order for order_id, order in orders.items()
        if month == order.timestamp[:7]
    }
    

def filter_by_date_range(orders, from_date, to_date):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    
    return {
        key: order for key, order in orders.items() 
        if start_date <= datetime.fromisoformat(order.timestamp).date() <= end_date
    }




#---------- For Customer ----------#

def get_name_to_id_map(menu_items: dict) -> dict:
    return {
        item.name.lower(): item.item_id
        for item in menu_items.values()
        if item.available
    }


def get_id_to_name_map(menu_items: dict) -> dict:
    return {
        item.item_id: item.name
        for item in menu_items.values()
        if item.available
    }
