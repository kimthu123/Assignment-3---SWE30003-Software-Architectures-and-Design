from utils.db_handler import read_json
from repositories.product_repository import ProductRepository
from collections import defaultdict
from datetime import datetime

class VisualiseStatistics:
    def __init__(self):
        self.orders = read_json('data/orders.json')
        self.product_repo = ProductRepository()
    
    def get_mode(self): # most bought product
        product_quantities = defaultdict(int)
        
        for order in self.orders:
            if order.get('items'):
                for item in order['items']:
                    product_quantities[item['product_id']] += item['quantity']
        
        if not product_quantities:
            return {"product_name": "N/A", "total_quantity": 0}
        
        most_bought_id = max(product_quantities.items(), key=lambda x: x[1])[0]
        product = self.product_repo.get_id(most_bought_id)
        
        return {
            "product_name": product['name'] if product else f"Product ID {most_bought_id}",
            "product_id": most_bought_id,
            "total_quantity": product_quantities[most_bought_id]
        }
    
    def get_average_revenue(self): # per month
        monthly_revenue = defaultdict(list)
        
        for order in self.orders:
            if order.get('created_at') and order.get('total_amount'):
                try:
                    date = datetime.strptime(order['created_at'], "%Y-%m-%d %H:%M:%S")
                    month_key = f"{date.year}-{date.month:02d}"
                    monthly_revenue[month_key].append(order['total_amount'])
                except ValueError:
                    continue
        
        if not monthly_revenue:
            return {}
        
        average_by_month = {}
        for month, amounts in monthly_revenue.items():
            average_by_month[month] = round(sum(amounts) / len(amounts), 2)
        
        return average_by_month
    
    def get_average_quantity(self):
        product_orders = defaultdict(list)
        
        for order in self.orders:
            if order.get('items'):
                for item in order['items']:
                    product_orders[item['product_id']].append(item['quantity'])
        
        if not product_orders:
            return {}
        
        averages = {}
        for product_id, quantities in product_orders.items():
            product = self.product_repo.get_id(product_id)
            product_name = product['name'] if product else f"Product ID {product_id}"
            averages[product_name] = round(sum(quantities) / len(quantities), 2)
        
        return averages
    
    def get_all_stats(self):
        return {
            "most_bought_product": self.get_mode(),
            "average_revenue_by_month": self.get_average_revenue(),
            "average_quantity_per_product": self.get_average_quantity()
        }
