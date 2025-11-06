from utils.db_handler import read_json, write_json

class ProductRepository:
    def __init__(self):
        self.file_path = 'data/products.json'

    def get_data(self):
        return read_json(self.file_path)

    def get_id(self, product_id):
        products = read_json(self.file_path)
        return next((p for p in products if p['id'] == product_id), None)

    def save_all(self, products):
        write_json(self.file_path, products)

