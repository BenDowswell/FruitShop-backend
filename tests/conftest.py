import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import User
from app.auth import hash_password
from fastapi.testclient import TestClient
from app.main import app

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the `get_db` dependency
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        # Seed the database with admin and customer users
        admin_user = User(
            username="admin", password_hash=hash_password("admin"), role="admin"
        )
        customer_user = User(
            username="customer",
            password_hash=hash_password("customer"),
            role="customer",
        )
        db.add(admin_user)
        db.add(customer_user)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c


def test_add_and_list_fruits(client):
    admin_token = get_token("admin", "admin")
    headers = auth_headers(admin_token)

    # Add a fruit
    fruit_data = {"name": "TestFruit", "prefix": "T", "price": 1.99, "quantity": 100}
    response = client.post("/fruits/", json=fruit_data, headers=headers)
    assert response.status_code == 200

    # List fruits
    response = client.get("/fruits/", headers=headers)
    assert response.status_code == 200
    fruits = response.json()
    assert any(fruit["prefix"] == "T" for fruit in fruits)
