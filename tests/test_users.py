from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "username": "testuser",
        "password": "testpass",
        "role": "customer"
    })
    assert response.status_code in [200, 400]  # 400 if already exists
    if response.status_code == 200:
        assert response.json()["username"] == "testuser"
        assert response.json()["role"] == "customer"

