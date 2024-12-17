from flask import Blueprint, request, jsonify
from models.driver import Driver
from models.database import db

driver_routes = Blueprint("driver_routes", __name__)

# GET /drivers - Récupérer tous les chauffeurs
@driver_routes.route("/drivers", methods=["GET"])
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([driver.to_dict() for driver in drivers]), 200

# GET /drivers/<id> - Récupérer un chauffeur par ID
@driver_routes.route("/drivers/<int:id>", methods=["GET"])
def get_driver(id):
    driver = Driver.query.get(id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    return jsonify(driver.to_dict()), 200

# POST /drivers - Créer un chauffeur
@driver_routes.route("/drivers", methods=["POST"])
def create_driver():
    data = request.json
    if not data.get("name") or not data.get("license_number"):
        return jsonify({"error": "Name and license_number are required"}), 400

    new_driver = Driver(name=data["name"], license_number=data["license_number"])
    db.session.add(new_driver)
    db.session.commit()
    return jsonify(new_driver.to_dict()), 201

# PUT /drivers/<id> - Mettre à jour un chauffeur
@driver_routes.route("/drivers/<int:id>", methods=["PUT"])
def update_driver(id):
    driver = Driver.query.get(id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    data = request.json
    driver.name = data.get("name", driver.name)
    driver.license_number = data.get("license_number", driver.license_number)
    db.session.commit()
    return jsonify(driver.to_dict()), 200

# DELETE /drivers/<id> - Supprimer un chauffeur
@driver_routes.route("/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):
    driver = Driver.query.get(id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": "Driver deleted successfully"}), 200
