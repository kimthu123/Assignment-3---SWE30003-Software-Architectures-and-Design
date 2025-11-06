from utils.db_handler import read_json, write_json

class Cart:
    def __init__(self):
        # Load existing cart items from JSON (automatically creates [] if missing)
        self.items = read_json('data/cart.json')

    def add_item(self, product_id, quantity):
        products = read_json('data/products.json')
        product = next((p for p in products if p['id'] == product_id), None)

        if not product:
            return {"error": "Product not found"}
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
        products = read_json('data/products.json')
        total = 0
        for item in self.items:
            p = next((p for p in products if p['id'] == item['product_id']), None)
            if p:
                total += p['price'] * item['quantity']
        return round(total * 1.1, 2)  # +10% tax

    def clear(self):
        self.items = []
        write_json('data/cart.json', self.items)
