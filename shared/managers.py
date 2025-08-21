from menu.manager import MenuManager
from orders.order_manager import OrderManager

menu_manager = MenuManager("data/menu.json")
order_manager = OrderManager("data/orders.json", menu_manager=menu_manager)
