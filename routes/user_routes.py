from flask import Blueprint, request, jsonify
from models.database import db
from models.user import User

# Définition du blueprint avec "user_routes"
user_routes = Blueprint("user_routes", __name__)

# Récupérer tous les utilisateurs (GET /api/user)
@user_routes.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Récupérer un utilisateur par ID (GET /api/user/<user_id>)
@user_routes.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)  # Remplacement par la nouvelle méthode
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

# Créer un utilisateur (POST /api/user)
@user_routes.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    # Correction ici : utilisation de User.query.filter_by()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Mettre à jour un utilisateur (PUT /api/user/<user_id>)
@user_routes.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)  # Correction
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict()), 200

# Supprimer un utilisateur (DELETE /api/user/<user_id>)
@user_routes.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(User, user_id)  # Correction
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
