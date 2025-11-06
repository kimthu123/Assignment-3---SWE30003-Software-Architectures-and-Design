import datetime
from utils.db_handler import read_json, write_json
from domain.payment import Payment
from domain.invoice import Invoice
from domain.packaging import Packaging
from domain.delivery import Delivery

class Checkout:
    def __init__(self, cart):
        self.cart = cart

    def confirm_order(self):
        # check if cart is empty
        if not self.cart.items:
            return {"error": "Cart is empty, please add items to the cart."}

        orders = read_json('data/orders.json')
        products = read_json('data/products.json')

        # validate stock for all items
        for item in self.cart.items:
            product = next((p for p in products if p['id'] == item['product_id']), None)
            if not product:
                return {"error": f"Product {item['product_id']} not found"}
            if product['stock'] < item['quantity']:
                return {"error": f"Not enough stock for {product['name']}"}

        # decrease stock
        for item in self.cart.items:
            product = next(p for p in products if p['id'] == item['product_id'])
            product['stock'] -= item['quantity']
        write_json('data/products.json', products)

        # create order record
        order_id = len(orders) + 1
        total_amount = self.cart.calculate_total()
        order = {
            "order_id": order_id,
            "items": self.cart.items,
            "total_amount": total_amount,
            "status": "pending",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        orders.append(order)
        write_json('data/orders.json', orders)

        # process Payment
        payment = Payment(order_id, total_amount)
        payment_result = payment.process_payment()

        # generate Invoice
        invoice = Invoice(order_id, total_amount, payment_result["status"])
        invoice_data = invoice.generate_invoice()

        # update order status
        order["status"] = "paid"
        write_json('data/orders.json', orders)

        # package
        packaging = Packaging(order_id)
        package_result = packaging.prepare_package()

        # delivery
        delivery = Delivery(order_id, "123 Swanston St, Melbourne")
        delivery_result = delivery.start_delivery()

        # print receipt
        return {
            "order": order,
            "payment": payment_result,
            "invoice": invoice_data,
            "packaging": package_result,
            "delivery": delivery_result
        }
