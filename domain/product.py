from utils.db_handler import read_json

class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity):
        return self.stock >= quantity

    @staticmethod
    def get_all():
        return read_json('data/products.json')
