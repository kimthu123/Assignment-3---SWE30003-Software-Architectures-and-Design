from utils.db_handler import read_json

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id, quantity):
        products = read_json('data/products.json')
        product = next((p for p in products if p['id'] == product_id), None)

        if not product:
            return {"error": "Product not found"}
        if product["stock"] < quantity:
            return {"error": "Not enough stock"}

        self.items.append({"product_id": product_id, "quantity": quantity})
        return {"message": f"Added {quantity} of {product['name']}"}

    def calculate_total(self):
        products = read_json('data/products.json')
        total = 0
        for item in self.items:
            p = next(p for p in products if p['id'] == item['product_id'])
            total += p['price'] * item['quantity']
        return round(total * 1.1, 2)  # +10% tax
