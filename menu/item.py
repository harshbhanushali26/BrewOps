class MenuItem:
    def __init__(self, category, name, price, available=True, is_special=False, order_count=0, item_id=None):
        self.category = category.strip().title()
        self.name = name.strip().title()
        self.price = price
        self.available = available
        self.is_special = is_special
        self.order_count = order_count
        self.item_id = item_id


    def to_dict(self):
        return {
            "category":self.category,
            "name":self.name,
            "price":self.price,
            "available":self.available,
            "is_special":self.is_special,
            "order_count":self.order_count
        }


    @classmethod
    def from_dict(cls, item_id, data):
        return cls(
            category = data['category'],
            name = data['name'],
            price = data['price'],
            available = data['available'],
            is_special = data['is_special'],
            order_count = data['order_count'],
            item_id = item_id,
            )
    
    
    def __str__(self):
        special = "⭐ Special" if self.is_special else ""
        status = "✅ Available" if self.available else "❌ Unavailable"
        return f"{[self.item_id]}: {self.name} - ₹{self.price} ({self.category}) {status} {special}"

