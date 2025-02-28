from flask import Blueprint, request, jsonify
from models.database import db
from models.invoice import Invoice

invoice_routes = Blueprint("invoice_routes", __name__)

# 1. Créer une facture (POST /api/invoices)
@invoice_routes.route("/invoices", methods=["POST"])
def create_invoice():
    data = request.get_json()
    
    # Vérifier que les données requises sont présentes
    if not data.get("customer_name") or not data.get("items") or not data.get("total"):
        return jsonify({"error": "Name, items, and total are required"}), 400

    # Créer la nouvelle facture
    new_invoice = Invoice(
        customer_name=data["customer_name"],
        items=data["items"],
        total=data["total"]
    )
    
    # Ajouter la facture à la base de données et valider
    db.session.add(new_invoice)
    db.session.commit()
    
    # Retourner la réponse avec les données de la facture créée
    return jsonify(new_invoice.to_dict()), 201


# 2. Récupérer toutes les factures (GET /api/invoices)
@invoice_routes.route("/invoices", methods=["GET"])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice.to_dict() for invoice in invoices]), 200


# 3. Récupérer une facture par ID (GET /api/invoices/:id)
@invoice_routes.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = db.session.get(Invoice,invoice_id)
    
    # Vérifier si la facture existe
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    return jsonify(invoice.to_dict()), 200


# 4. Mettre à jour une facture (PUT /api/invoices/:id)
@invoice_routes.route("/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    invoice = db.session.get(Invoice,invoice_id)
    
    # Vérifier si la facture existe
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    data = request.get_json()
    
    # Mettre à jour les champs de la facture
    invoice.customer_name = data.get("customer_name", invoice.customer_name)
    invoice.items = data.get("items", invoice.items)
    invoice.total = data.get("total", invoice.total)
    
    db.session.commit()
    
    return jsonify(invoice.to_dict()), 200


# 5. Supprimer une facture (DELETE /api/invoices/:id)
@invoice_routes.route("/invoices/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    invoice = db.session.get(Invoice,invoice_id)
    
    # Vérifier si la facture existe
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    # Supprimer la facture de la base de données
    db.session.delete(invoice)
    db.session.commit()
    
    return jsonify({"message": "Invoice deleted successfully"}), 200
