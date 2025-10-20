import unittest
from app import app  

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_products_page_status_code(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_items_listed(self):
        response = self.client.get('/products/')
        html = response.get_data(as_text=True)
        self.assertIn('Вітаміни', html)
        self.assertIn('Парацетамол', html)
        self.assertIn('Назол', html)

if __name__ == "__main__":
    unittest.main()
