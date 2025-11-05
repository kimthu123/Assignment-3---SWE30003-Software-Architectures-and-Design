from utils.db_handler import read_json, write_json
import datetime

class Delivery:
    def __init__(self, order_id, address):
        self.order_id = order_id
        self.address = address

    def start_delivery(self):
        deliveries = read_json('data/deliveries.json')
        delivery_id = len(deliveries) + 1

        delivery = {
            "delivery_id": delivery_id,
            "order_id": self.order_id,
            "address": self.address,
            "status": "on the way",
            "dispatched_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        deliveries.append(delivery)
        write_json('data/deliveries.json', deliveries)

        return {
            "message": f"Delivery for order {self.order_id} dispatched.",
            "delivery": delivery
        }
