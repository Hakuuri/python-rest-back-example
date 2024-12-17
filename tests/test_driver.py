import unittest
from app import create_app
from models.database import db

class DriverTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_driver(self):
        """Test de la création d'un chauffeur"""
        response = self.client.post("/api/drivers", json={
            "name": "Alice Smith",
            "license_number": "LIC12345"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Alice Smith", response.json["name"])

    def test_get_all_drivers(self):
        """Test de récupération de tous les chauffeurs"""
        # Créer un chauffeur
        self.client.post("/api/drivers", json={
            "name": "Alice Smith",
            "license_number": "LIC12345"
        })

        # Vérifier la récupération
        response = self.client.get("/api/drivers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Alice Smith")

    def test_get_driver_by_id(self):
        """Test de récupération d'un chauffeur par ID"""
        # Créer un chauffeur
        self.client.post("/api/drivers", json={
            "name": "Bob Johnson",
            "license_number": "LIC67890"
        })

        # Récupérer le chauffeur par ID
        response = self.client.get("/api/drivers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Bob Johnson")

    def test_update_driver(self):
        """Test de mise à jour d'un chauffeur"""
        # Créer un chauffeur
        self.client.post("/api/drivers", json={
            "name": "Charlie Brown",
            "license_number": "LIC00001"
        })

        # Mise à jour des informations
        response = self.client.put("/api/drivers/1", json={
            "name": "Charlie Updated",
            "license_number": "LIC99999"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Charlie Updated")

    def test_delete_driver(self):
        """Test de suppression d'un chauffeur"""
        # Créer un chauffeur
        self.client.post("/api/drivers", json={
            "name": "David King",
            "license_number": "LIC54321"
        })

        # Supprimer le chauffeur
        response = self.client.delete("/api/drivers/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.json["message"])

        # Vérifier que le chauffeur n'existe plus
        response = self.client.get("/api/drivers/1")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
