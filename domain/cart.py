"""Shopping cart management module."""

from utils.db_handler import read_json, write_json
from repositories.product_repository import ProductRepository


class Cart:
    """Handles cart operations: add, calculate total, view, and clear."""

    def __init__(self):
        """Initialize cart with items loaded from storage."""
        self.items = read_json('data/cart.json')
        self.product_repo = ProductRepository()

    def add_item(self, product_id, quantity):
        """Add a product to the cart, validating stock and availability."""
        products = self.product_repo.get_data()
        product = next((p for p in products if p['id'] == product_id), None)

        if not product:
            return {"error": "Product not found"}

        if not product.get('on_shelf', True):
            return {"error": "Product is not available"}

        if product["stock"] < quantity:
            return {"error": "Not enough stock"}

        existing = next(
            (item for item in self.items if item['product_id'] == product_id),
            None
        )

        if existing:
            existing['quantity'] += quantity
        else:
            self.items.append({
                "product_id": product_id,
                "quantity": quantity
            })

        write_json('data/cart.json', self.items)

        return {
            "message": f"Added {quantity} {product['name']} to shopping cart."
        }

    def calculate_total(self):
        """Calculate total cart value based on product prices."""
        products = self.product_repo.get_data()
        total = 0

        for item in self.items:
            product = next(
                (p for p in products if p['id'] == item['product_id']), None
            )
            if product:
                total += product['price'] * item['quantity']

        # Tax assumed to be included in price
        return round(total, 2)

    def get_cart_info(self):
        """Return cart details including items and total cost."""
        return {
            "items": self.items,
            "total": self.calculate_total()
        }

    def clear(self):
        """Empty the shopping cart and update storage."""
        self.items = []
        write_json('data/cart.json', self.items)
        return {"message": "Cart cleared"}
