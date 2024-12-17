import unittest
from app import create_app
from models.database import db

class BusTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_bus(self):
        """Test de la création d'un bus"""
        response = self.client.post("/api/bus/buses", json={
            "bus_number": "BUS100",
            "capacity": 50
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["bus_number"], "BUS100")

    def test_get_all_buses(self):
        """Test de récupération de tous les bus"""
        # Créer un bus
        self.client.post("/api/bus/buses", json={
            "bus_number": "BUS200",
            "capacity": 60
        })

        # Vérifier la récupération
        response = self.client.get("/api/bus/buses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["bus_number"], "BUS200")

    def test_get_bus_by_id(self):
        """Test de récupération d'un bus par ID"""
        # Créer un bus
        self.client.post("/api/bus/buses", json={
            "bus_number": "BUS300",
            "capacity": 40
        })

        # Récupérer le bus par ID
        response = self.client.get("/api/bus/buses/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["bus_number"], "BUS300")

    def test_update_bus(self):
        """Test de mise à jour d'un bus"""
        # Créer un bus
        self.client.post("/api/bus/buses", json={
            "bus_number": "BUS400",
            "capacity": 55
        })

        # Mettre à jour le bus
        response = self.client.put("/api/bus/buses/1", json={
            "bus_number": "BUS400-Updated",
            "capacity": 70
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["bus_number"], "BUS400-Updated")

    def test_delete_bus(self):
        """Test de suppression d'un bus"""
        # Créer un bus
        self.client.post("/api/bus/buses", json={
            "bus_number": "BUS500",
            "capacity": 30
        })

        # Supprimer le bus
        response = self.client.delete("/api/bus/buses/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted", response.json["message"])

        # Vérifier que le bus n'existe plus
        response = self.client.get("/api/bus/buses/1")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
