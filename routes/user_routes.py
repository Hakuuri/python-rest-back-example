from flask import Blueprint, request, jsonify
from models.database import db
from models.user import User

user_routes = Blueprint("user_routes", __name__)

# GET /users - Récupérer tous les utilisateurs
@user_routes.route("/users", methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    return jsonify([user.to_dict() for user in users]), 200

# GET /users/<int:user_id> - Récupérer un utilisateur par ID
@user_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)  # Utiliser db.session.get() pour SQLAlchemy 2.0
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

# POST /users - Créer un nouvel utilisateur
@user_routes.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# PUT /users/<int:user_id> - Mettre à jour un utilisateur
@user_routes.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)  # Utiliser db.session.get() pour récupérer l'utilisateur
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict()), 200

# DELETE /users/<int:user_id> - Supprimer un utilisateur
@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(User, user_id)  # Utiliser db.session.get() pour récupérer l'utilisateur
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
