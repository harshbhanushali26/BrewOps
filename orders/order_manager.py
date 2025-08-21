from utils.json_io import load_order_data, save_order_data
from orders.order import Order
from utils.filtering import filter_orders_by_criteria, filter_by_month 


class OrderManager:
    def __init__(self, file_path="data/orders.json", menu_manager=None):
        self.file_path = file_path
        self.orders = {}  # {order_id: Order}
        self.menu_manager = menu_manager  # ✅ reference to the same menu manager
        self.load_orders()


    def load_orders(self):
        raw_data = load_order_data(self.file_path)
        self.orders = { order_id : Order.from_dict(order) for order_id, order in raw_data.items() }


    def save_orders(self):
        order_dict = {
            order_id : order.to_dict() for order_id, order in self.orders.items()
        }
        save_order_data(self.file_path, order_dict) 


    def generate_order_id(self, timestamp):
        # Use passed timestamp, not datetime.now()
        year_month_str = timestamp[:7]  # "YYYY-MM"
        orders_in_month = []

        for order in self.orders.values():
            order_month = order.timestamp[:7]
            if order_month == year_month_str:
                orders_in_month.append(order)

        if not orders_in_month:
            new_id_suffix = "0001"
        else:
            existing_numbers = [
                int(order.order_id.split('-')[3]) for order in orders_in_month
            ]
            new_number = max(existing_numbers) + 1
            new_id_suffix = str(new_number).zfill(4)

        new_order_id = f"ORD-{year_month_str}-{new_id_suffix}"
        return new_order_id


    def add_order(self, order:Order):
       
        if not isinstance(order, Order):
            raise ValueError("Must be a Order")
        
        if order.order_id in self.orders:
            return False

        self.orders[order.order_id] = order
        self.save_orders()

        for item in order.items:
            item_id = item.get("item_id")
            qty = item.get("qty", 1)
            self.menu_manager.increment_order_count(item_id, qty)
            self.menu_manager.save_menu()
            
        return True


    def update_status(self, order_id, new_status):
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        order.status = new_status
        self.save_orders()
        return True


    def mark_paid(self, order_id):
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.paid = True
        self.save_orders()
        return True


    def get_order(self, order_id):
        if order_id not in self.orders:
            return False
        
        return self.orders[order_id]


    def get_all_orders(self):
        return list(self.orders.values())
    

    def filter_orders(self, status=None, paid=None, date=None):
        return filter_orders_by_criteria(self.orders, status=status, paid=paid, date=date)


    def remove_order(self, order_id):
        if order_id not in self.orders:
            return False
        
        order = self.orders.pop(order_id)
        if self.menu_manager:
            for item in order.items:
                self.menu_manager.decrement_order_count(item['item_id'], item['qty'])
            self.menu_manager.save_menu()

        self.save_orders()
        return True


