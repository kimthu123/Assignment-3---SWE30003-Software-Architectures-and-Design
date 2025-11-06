from repositories.product_repository import ProductRepository
from domain.product import Product

class Catalogue:
    def __init__(self):
        self.product_repo = ProductRepository()

    # retrieve all products that are on shelf (ONLY)
    def get_on_shelf_products(self):
        products = self.product_repo.get_data()
        return [p for p in products if p.get('on_shelf', True)]

    def get_products(self):
        return self.get_on_shelf_products() # display all products that are on shelf

    def search_by_name(self, name):
        products = self.get_on_shelf_products() # search products by name (only on shelf)
        name_lower = name.lower()
        return [p for p in products if name_lower in p['name'].lower()]

    def filter_by_category(self, category):
        products = self.get_on_shelf_products() # filters products by category (only on shelf)
        return [p for p in products if p.get('category') == category]

    def get_product_details(self, product_id):
        # returns current product details and availability status (only if on shelf)
        product = self.product_repo.get_id(product_id)
        if not product:
            return {"error": "Product not found"}
        
        # check if product is on shelf
        if not product.get('on_shelf', True):
            return {"error": "Product not available"}
        
        return {
            "id": product['id'],
            "name": product['name'],
            "description": product['description'],
            "category": product['category'],
            "price": product['price'],
            "stock": product['stock'],
            "available": product['stock'] > 0
        }
    
    def add_product(self, name, description, category, price, stock):
        # add new product to catalogue (admin)
        products = self.product_repo.get_data()
        
        # create new ID for added product
        new_id = max([p['id'] for p in products]) + 1 if products else 1
        
        # create product object (on_shelf defaults to True)
        new_product = Product(new_id, name, description, category, price, stock, on_shelf=True)
        
        # add to products list (in dictionary)
        products.append(new_product.to_dictionary())
        
        # save to json file
        self.product_repo.save_all(products)
        
        return {
            "message": "Product added successfully",
            "product": new_product.to_dictionary()
        }
    
    def remove_product(self, product_id):
        # remove product from catalogue by setting on_shelf to false (admin)
        products = self.product_repo.get_data()
        
        # find product by ID
        product = next((p for p in products if p['id'] == product_id), None)
        
        if not product:
            return {"error": "Product not found"}
        
        # set on_shelf to false instead of deleting
        product['on_shelf'] = False
        
        # save to repository
        self.product_repo.save_all(products)
        
        return {
            "message": f"Product '{product['name']}' removed from shelf successfully",
            "removed_product": product
        }

  

