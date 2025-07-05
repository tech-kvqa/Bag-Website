from flask import Blueprint, jsonify
from models import db, Product

product_api = Blueprint('product_api', __name__)

@product_api.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@product_api.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())
