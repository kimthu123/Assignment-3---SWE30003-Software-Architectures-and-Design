"""Product catalogue management module."""

from domain.product import Product
from repositories.product_repository import ProductRepository


class Catalogue:
    """Handles all product catalogue operations."""

    def __init__(self):
        self.product_repo = ProductRepository()

    def get_on_shelf_products(self):
        """Retrieve all products currently on the shelf."""
        products = self.product_repo.get_data()
        return [p for p in products if p.get('on_shelf', True)]

    def get_products(self):
        """Return all available (on-shelf) products."""
        return self.get_on_shelf_products()

    def search_by_name(self, name):
        """Search available products by name (case-insensitive)."""
        products = self.get_on_shelf_products()
        name_lower = name.lower()
        return [p for p in products if name_lower in p['name'].lower()]

    def filter_by_category(self, category):
        """Filter available products by category."""
        products = self.get_on_shelf_products()
        return [p for p in products if p.get('category') == category]

    def get_product_details(self, product_id):
        """Return product details and availability status."""
        product = self.product_repo.get_id(product_id)

        if not product:
            return {"error": "Product not found"}

        if not product.get('on_shelf', True):
            return {"error": "Product not available"}

        return {
            "id": product['id'],
            "name": product['name'],
            "description": product['description'],
            "category": product['category'],
            "price": product['price'],
            "stock": product['stock'],
            "available": product['stock'] > 0,
        }

    def add_product(self, name, description, category, price, stock):
        """Add a new product to the catalogue (admin only)."""
        products = self.product_repo.get_data()

        # Generate new product ID
        new_id = max([p['id'] for p in products]) + 1 if products else 1

        # Create new product (on_shelf defaults to True)
        new_product = Product(
            new_id, name, description, category, price, stock, on_shelf=True
        )

        # Append and save
        products.append(new_product.to_dictionary())
        self.product_repo.save_all(products)

        return {
            "message": "Product added successfully",
            "product": new_product.to_dictionary(),
        }

    def remove_product(self, product_id):
        """Mark a product as removed (set on_shelf = False)."""
        products = self.product_repo.get_data()
        product = next((p for p in products if p['id'] == product_id), None)

        if not product:
            return {"error": "Product not found"}

        product['on_shelf'] = False
        self.product_repo.save_all(products)

        return {
            "message": f"Product '{product['name']}' removed from shelf successfully",
            "removed_product": product,
        }
