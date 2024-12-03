import pytest
from app import app, db

@pytest.fixture(scope='module')
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  # Create tables
            yield testing_client
            db.drop_all()  # Clean up after tests
