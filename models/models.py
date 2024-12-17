from flask import Blueprint, request, jsonify
from models.database import db
from models.user import User

users_bp = Blueprint('users', __name__)

# GET /users - Récupérer tous les utilisateurs
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    return jsonify(result), 200

# GET /users/<id> - Récupérer un utilisateur par ID
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

# POST /users - Créer un utilisateur
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"message": "Champs requis manquants"}), 400
    
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email}), 201

# PUT /users/<id> - Mettre à jour un utilisateur
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

# DELETE /users/<id> - Supprimer un utilisateur
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé"}), 200
