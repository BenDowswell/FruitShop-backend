from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user(client):
    # Login as admin
    login_response = client.post(
        "/auth/login", data={"username": "admin", "password": "admin"}
    )
    token = login_response.json()["access_token"]

    # Create a new user
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpass", "role": "customer"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in [200, 400]  # 400 if user already exists
