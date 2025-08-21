from datetime import datetime

class Order:
    def __init__(self, items, total_amount = 0.0,  status="pending", timestamp=None, paid=False, order_id=None, name=None):
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.timestamp = timestamp or datetime.now().isoformat()
        self.paid = paid
        self.order_id = order_id
        self.name = name


    def to_dict(self):
        return {
            "order_id" : self.order_id,
            "items" : self.items,
            "status" : self.status,
            "total_amount" : self.total_amount,
            "timestamp" : self.timestamp,
            "name" : self.name,
            "paid" : self.paid
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            items = data['items'],
            total_amount = data['total_amount'],
            status = data['status'],
            timestamp = data['timestamp'],
            paid = data['paid'],
            order_id = data['order_id'],
            name = data.get("name")
            )
    
    
    def calculate_total(self):
        self.total_amount = sum(item['qty'] * item['price'] for item in self.items)
        return self.total_amount
    

    def __str__(self):
        return f"Order({self.order_id}) by {self.name} | Total: ₹{self.total_amount:.2f} | Paid: {self.paid}"
    

    