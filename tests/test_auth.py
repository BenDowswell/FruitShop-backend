from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
from jose import jwt
from app.auth import SECRET_KEY, ALGORITHM

client = TestClient(app)


def test_login_admin():
    response = client.post(
        "/auth/login", data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_login_customer():
    response = client.post(
        "/auth/login", data={"username": "customer", "password": "customer"}
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login", data={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username or password"


def test_expired_token():
    # Create an expired token
    expired_token = jwt.encode(
        {"sub": "admin", "exp": datetime.utcnow() - timedelta(minutes=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    # Attempt to access a protected route
    response = client.get(
        "/fruits/", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"
