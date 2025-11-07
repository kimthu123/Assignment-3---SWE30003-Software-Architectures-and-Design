"""Defines the Product class and manages product availability and structure."""

from repositories.product_repository import ProductRepository


class Product:
    """Represents a product in the online store."""

    repository = ProductRepository()

    def __init__(self, id, name, description, category, price, stock, on_shelf=True):
        """Initialize product attributes."""
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.stock = stock
        self.on_shelf = on_shelf

    def is_available(self, quantity):
        """Check if sufficient stock is available for a given quantity."""
        return self.stock >= quantity

    def to_dictionary(self):
        """Convert the product object into a dictionary format for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "on_shelf": self.on_shelf,
        }
