from repositories.product_repository import ProductRepository

class Product:
    repository = ProductRepository()    

    def __init__(self, id, name, description, category, price, stock, on_shelf=True):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.stock = stock
        self.on_shelf = on_shelf

    def is_available(self, quantity):
        return self.stock >= quantity
    
    def to_dictionary(self):
        # retrive from json and create dictionary
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "on_shelf": self.on_shelf
        }
