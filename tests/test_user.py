import unittest
from app import create_app
from models.database import db
from models.user import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        # Création de la base de données en mémoire
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Nettoyage de la base de données
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test GET /api/user (aucun utilisateur)
    def test_get_all_users_empty(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # Test POST /api/user (création d'un utilisateur)
    def test_create_user(self):
        response = self.client.post("/api/user/", json={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("John Doe", str(response.data))

    # Test GET /api/user/<id> (utilisateur non trouvé)
    def test_get_user_not_found(self):
        response = self.client.get('/api/user/1')
        self.assertEqual(response.status_code, 404)

    # Test GET /api/user (avec un utilisateur existant)
    def test_get_users(self):
        self.client.post("/api/user/", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    # Test GET /api/user/<id> (récupération d'un utilisateur existant)
    def test_get_user(self):
        self.client.post("/api/user/", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.get("/api/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    # Test PUT /api/user/<id> (mise à jour d'un utilisateur)
    def test_update_user(self):
        self.client.post("/api/user/", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.put("/api/user/1", json={"name": "Jane Doe"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", str(response.data))

    # Test DELETE /api/user/<id> (suppression d'un utilisateur)
    def test_delete_user(self):
        self.client.post("/api/user/", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.delete("/api/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", str(response.data))

if __name__ == "__main__":
    unittest.main()
