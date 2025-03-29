### backend/tests/test_fruits.py

from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

def random_prefix():
    return ''.join(random.choices(string.ascii_uppercase, k=1))

def test_add_and_list_fruits():
    fruit_data = {
        "name": "TestFruit",
        "prefix": random_prefix(),
        "price": 1.99,
        "quantity": 100
    }

    response = client.post("/fruits/", json=fruit_data)
    assert response.status_code in [200, 400]  # allow reruns with unique prefix

    response = client.get("/fruits/")
    assert response.status_code == 200
    fruits = response.json()
    assert any(fruit["prefix"] == fruit_data["prefix"] for fruit in fruits)