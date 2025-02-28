import unittest
from app import create_app
from models.database import db
from models.invoice import Invoice

class InvoiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test pour créer une facture
    def test_create_invoice(self):
        response = self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 666.66
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("John Doe", str(response.data))

    # Test pour créer une facture avec des données manquantes
    def test_create_invoice_missing_data(self):
        response = self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "total": 666.66
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name, items, and total are require", str(response.data))

    # Test pour récupérer toutes les factures
    def test_get_invoices(self):
        self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 666.66
        })
        response = self.client.get("/api/invoices")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    # Test pour récupérer une facture par ID
    def test_get_invoice(self):
        self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 666.66
        })
        response = self.client.get("/api/invoices/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    # Test pour récupérer une facture qui n'existe pas
    def test_get_invoice_not_found(self):
        response = self.client.get("/api/invoices/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invoice not found", str(response.data))

    # Test pour mettre à jour une facture
    def test_update_invoice(self):
        self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 666.66
        })
        response = self.client.put("/api/invoices/1", json={
            "customer_name": "Jane Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 1099.99
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", str(response.data))

    # Test pour mettre à jour une facture qui n'existe pas
    def test_update_invoice_not_found(self):
        response = self.client.put("/api/invoices/999", json={
            "customer_name": "Non Existent",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 1099.99
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invoice not found", str(response.data))

    # Test pour supprimer une facture
    def test_delete_invoice(self):
        self.client.post("/api/invoices", json={
            "customer_name": "John Doe",
            "items": [{"product": "Ordi", "price": 666.66}],
            "total": 666.66
        })
        response = self.client.delete("/api/invoices/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invoice deleted successfully", str(response.data))

    # Test pour supprimer une facture qui n'existe pas
    def test_delete_invoice_not_found(self):
        response = self.client.delete("/api/invoices/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invoice not found", str(response.data))

if __name__ == "__main__":
    unittest.main()
