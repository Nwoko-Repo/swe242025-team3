import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class TestApp(unittest.TestCase):
    def setUp(self):
        # Configure the test client and database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
        self.app = app.test_client()

        # Initialize the database
        with app.app_context():
            db.create_all()
            # Add a test user
            test_user = User(
                email="testuser@example.com",
                password=generate_password_hash("password123"),
                username="testuser",
                address="123 Test Street"
            )
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        # Drop the test database after every test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        # Write a test for successful login
        response = self.app.post('/login', json={
            "email": "testuser@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)

    def test_login_failure(self):
        # Write a test for failed login due to incorrect password
        response = self.app.post('/login', json={
            "email": "testuser@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Incorrect password", response.data)

    def test_update_user_details_success(self):
        # Write a test for successful update
        user = User.query.filter_by(email="testuser@example.com").first()
        response = self.app.put(f'/update_user/{user.id}', json={
            "username": "updateduser",
            "address": "456 Updated Street"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User details updated successfully", response.data)

        # Verify the database changes
        updated_user = User.query.get(user.id)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.address, "456 Updated Street")

    def test_update_user_not_found(self):
        # Write a test for attempting to update a non-existent user
        response = self.app.put('/update_user/999', json={
            "username": "nonexistent",
            "address": "Nowhere"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User not found", response.data)

if __name__ == '__main__':
    unittest.main()
