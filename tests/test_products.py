import unittest
from app import create_app
from models.database import db
from models.product import Product

class ProductTestCase(unittest.TestCase):
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

    def test_create_product(self):
        response = self.client.post("/api/products", json={"name": "Product A", "price": 19.99, "stock": 100})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product A", str(response.data))

    def test_get_products(self):
        self.client.post("/api/products", json={"name": "Product A", "price": 19.99, "stock": 100})
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product A", str(response.data))

    def test_get_product(self):
        self.client.post("/api/products", json={"name": "Product A", "price": 19.99, "stock": 100})
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product A", str(response.data))

    def test_update_product(self):
        self.client.post("/api/products", json={"name": "Product A", "price": 19.99, "stock": 100})
        response = self.client.put("/api/products/1", json={"name": "Updated Product", "price": 29.99, "stock": 150})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Product", str(response.data))

    def test_delete_product(self):
        self.client.post("/api/products", json={"name": "Product A", "price": 19.99, "stock": 100})
        response = self.client.delete("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product deleted successfully", str(response.data))

    def test_get_product_not_found(self):
        response = self.client.get("/api/products/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found", str(response.data))

    def test_create_product_missing_data(self):
        response = self.client.post("/api/products", json={"name": "Product B", "price": 9.99})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name, price, and stock are required", str(response.data))

    def test_update_product_not_found(self):
        response = self.client.put("/api/products/999", json={"name": "Non Existent Product", "price": 39.99, "stock": 200})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found", str(response.data))

    def test_delete_product_not_found(self):
        response = self.client.delete("/api/products/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found", str(response.data))

if __name__ == "__main__":
    unittest.main()
