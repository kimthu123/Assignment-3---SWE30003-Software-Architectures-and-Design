from flask import Flask, request, jsonify
from domain.product import Product
from domain.cart import Cart
from domain.checkout import Checkout
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
cart = Cart()

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(Product.get_all())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    result = cart.add_item(data['product_id'], data['quantity'])
    return jsonify(result)

@app.route('/checkout', methods=['POST'])
def checkout():
    checkout_process = Checkout(cart)
    result = checkout_process.confirm_order()
    if isinstance(result, dict) and 'error' not in result:
        cart.clear()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
