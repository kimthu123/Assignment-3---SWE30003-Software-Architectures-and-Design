import datetime
from utils.db_handler import read_json, write_json

class Payment:
    def __init__(self, order_id, amount, method="card"):
        self.order_id = order_id
        self.amount = amount
        self.method = method
        self.status = "unpaid"
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_payment(self):
        # Simulate payment success (no real gateway)
        self.status = "paid"
        print(f"Payment successful for Order #{self.order_id}")
        return {
            "order_id": self.order_id,
            "amount": self.amount,
            "status": self.status,
            "method": self.method,
            "timestamp": self.timestamp
        }
