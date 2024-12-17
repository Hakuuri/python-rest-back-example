from flask import Blueprint, request, jsonify
from models.bus import Bus
from models.database import db



bus_routes = Blueprint("bus_routes", __name__)

# GET /buses - Récupérer tous les bus
@bus_routes.route("/buses", methods=["GET"])
def get_buses():
    buses = Bus.query.all()
    return jsonify([bus.to_dict() for bus in buses]), 200

# GET /buses/<id> - Récupérer un bus par ID
@bus_routes.route("/buses/<int:id>", methods=["GET"])
def get_bus(id):
    bus = db.session.get(Bus, id)
        
    if not bus:
        return jsonify({"error": "Bus not found"}), 404
    return jsonify(bus.to_dict()), 200

# POST /buses - Créer un bus
@bus_routes.route("/buses", methods=["POST"])
def create_bus():
    data = request.json
    if not data.get("bus_number") or not data.get("capacity"):
        return jsonify({"error": "Bus number and capacity are required"}), 400

    new_bus = Bus(bus_number=data["bus_number"], capacity=data["capacity"])
    db.session.add(new_bus)
    db.session.commit()
    return jsonify(new_bus.to_dict()), 201

# PUT /buses/<id> - Mettre à jour un bus
@bus_routes.route("/buses/<int:id>", methods=["PUT"])
def update_bus(id):
    bus = db.session.get(Bus, id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404

    data = request.json
    bus.bus_number = data.get("bus_number", bus.bus_number)
    bus.capacity = data.get("capacity", bus.capacity)
    db.session.commit()
    return jsonify(bus.to_dict()), 200

# DELETE /buses/<id> - Supprimer un bus
@bus_routes.route("/buses/<int:id>", methods=["DELETE"])
def delete_bus(id):
    bus = db.session.get(Bus, id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404

    db.session.delete(bus)
    db.session.commit()
    return jsonify({"message": "Bus deleted successfully"}), 200
