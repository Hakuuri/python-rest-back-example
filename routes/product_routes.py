from flask import Blueprint, request, jsonify
from models.database import db
from models.product import Product

product_routes = Blueprint("product_routes", __name__)

# GET /products - Récupérer tous les produits
@product_routes.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# GET /products/<id> - Récupérer un produit par ID
@product_routes.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = db.session.get(Product, product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404

# POST /products - Créer un produit
@product_routes.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data.get("name") or not data.get("price") or not data.get("stock"):
        return jsonify({"error": "Name, price, and stock are required"}), 400
    
    new_product = Product(name=data["name"], price=data["price"], stock=data["stock"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# PUT /products/<id> - Mettre à jour un produit
@product_routes.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = db.session.get(Product,product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# DELETE /products/<id> - Supprimer un produit
@product_routes.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
