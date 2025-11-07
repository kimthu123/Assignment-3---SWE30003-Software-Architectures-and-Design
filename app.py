from flask import Flask, request, jsonify, render_template
from domain.product import Product
from domain.cart import Cart
from domain.checkout import Checkout
from domain.account_manager import AccountManager
from domain.catalogue import Catalogue
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
cart = Cart()
account_manager = AccountManager()
catalogue = Catalogue()

@app.route('/')
def index():
    products = catalogue.get_products()  # get products in Python
    return render_template("index.html", products=products)

@app.route('/catalogue', methods=['GET'])
def get_catalogue():
    return jsonify(catalogue.get_products())

@app.route('/cart_page')
def cart_page():
    return render_template('cart.html')

def index():
    products = catalogue.get_products()  # get products in Python
    return render_template("index.html", products=products)

@app.route('/cart', methods=['GET'])
def view_cart():
    return jsonify(cart.get_cart_info())

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    return jsonify(cart.clear())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    result = cart.add_item(data['product_id'], data['quantity'])
    return jsonify(result)

@app.route('/checkout', methods=['POST'])
def checkout():
    checkout_process = Checkout(cart)
    return jsonify(checkout_process.process_checkout())

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    result = account_manager.create_account(
        data['email'],
        data['password'],
        data.get('account_type')
    )
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    result = account_manager.login(data['email'], data['password'])
    return jsonify(result)

@app.route('/admin/products', methods=['POST'])
def add_product():
    data = request.json
    result = catalogue.add_product(
        data['name'],
        data['description'],
        data['category'],
        data['price'],
        data['stock']
    )
    return jsonify(result)

@app.route('/admin/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    result = catalogue.remove_product(product_id)
    return jsonify(result)

@app.route('/catalogue/search', methods=['GET'])
def search_products():
    name = request.args.get('name', '')
    return jsonify(catalogue.search_by_name(name))

@app.route('/catalogue/category', methods=['GET'])
def filter_products():
    category = request.args.get('category', '')
    return jsonify(catalogue.filter_by_category(category))

@app.route('/catalogue/product/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    return jsonify(catalogue.get_product_details(product_id))

if __name__ == '__main__':
    app.run(debug=True)
