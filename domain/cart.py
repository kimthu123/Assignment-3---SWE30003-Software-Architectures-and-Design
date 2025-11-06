from utils.db_handler import read_json, write_json
from repositories.product_repository import ProductRepository

class Cart:
    def __init__(self):
        # Load existing cart items from JSON (automatically creates [] if missing)
        self.items = read_json('data/cart.json')
        self.product_repo = ProductRepository()

    def add_item(self, product_id, quantity):
        products = self.product_repo.get_data()
        product = next((p for p in products if p['id'] == product_id), None)

        if not product:
            return {"error": "Product not found"}
        if not product.get('on_shelf', True):
            return {"error": "Product is not available"}
        if product["stock"] < quantity:
            return {"error": "Not enough stock"}

        existing = next((item for item in self.items if item['product_id'] == product_id), None)

        if existing:
            existing['quantity'] += quantity
        else:
            self.items.append({"product_id": product_id, "quantity": quantity})

        write_json('data/cart.json', self.items)
        return {"message": f"Added {quantity} {product['name']} to shopping cart."}

    def calculate_total(self):
        products = self.product_repo.get_data()
        total = 0
        for item in self.items:
            p = next((p for p in products if p['id'] == item['product_id']), None)
            if p:
                total += p['price'] * item['quantity']
        return round(total, 2) # no need for tax just assumes its included in price of items

    def get_cart_info(self):
        return {
            "items": self.items,
            "total": self.calculate_total()
        }

    def clear(self):
        self.items = []
        write_json('data/cart.json', self.items)
        return {"message": "Cart cleared"}
