from flask import Blueprint, request, jsonify
from models.driver import Driver
from models.database import db

# Définition du Blueprint
driver_routes = Blueprint("driver_routes", __name__)

# GET / - Récupérer tous les chauffeurs
@driver_routes.route("/", methods=["GET"])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([driver.to_dict() for driver in drivers]), 200

# GET /<int:id> - Récupérer un chauffeur par ID
@driver_routes.route("/<int:id>", methods=["GET"])
def get_driver(id):
    driver = db.session.get(Driver, id)  # Correction ici
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    return jsonify(driver.to_dict()), 200

# POST / - Créer un chauffeur
@driver_routes.route("/", methods=["POST"])
def create_driver():
    data = request.json
    if not data or not data.get("name") or not data.get("license_number"):
        return jsonify({"error": "Name and license_number are required"}), 400

    # Vérification des doublons (numéro de licence unique)
    if Driver.query.filter_by(license_number=data["license_number"]).first():
        return jsonify({"error": "License number already exists"}), 400

    # Création d'un nouveau chauffeur
    new_driver = Driver(name=data["name"], license_number=data["license_number"])
    db.session.add(new_driver)
    db.session.commit()
    return jsonify(new_driver.to_dict()), 201

# PUT /<int:id> - Mettre à jour un chauffeur
@driver_routes.route("/<int:id>", methods=["PUT"])
def update_driver(id):
    driver = db.session.get(Driver, id)  # Correction ici
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    # Mise à jour des champs
    data = request.json
    driver.name = data.get("name", driver.name)
    driver.license_number = data.get("license_number", driver.license_number)
    db.session.commit()
    return jsonify(driver.to_dict()), 200

# DELETE /<int:id> - Supprimer un chauffeur
@driver_routes.route("/<int:id>", methods=["DELETE"])
def delete_driver(id):
    driver = db.session.get(Driver, id)  # Correction ici
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": "Driver deleted successfully"}), 200
