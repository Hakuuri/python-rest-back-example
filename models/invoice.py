from datetime import datetime
from models.database import db

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)  # ID de la facture
    customer_name = db.Column(db.String(100), nullable=False)  # Nom du client
    items = db.Column(db.PickleType, nullable=False)  # Liste de produits (sérialisée)
    total = db.Column(db.Float, nullable=False)  # Montant total de la facture
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création de la facture

    def __init__(self, customer_name, items, total):
        self.customer_name = customer_name
        self.items = items
        self.total = total

    def to_dict(self):
        """
        Retourne une représentation dictionnaire de la facture.
        """
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'items': self.items,
            'total': self.total,
            'created_at': self.created_at.isoformat()
        }
