from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token(username: str, password: str) -> str:
    """
    Get an authentication token for a given username and password.
    """
    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert response.status_code == 200, f"Failed to get token: {response.json()}"
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    """
    Generate headers with the Authorization token.
    """
    return {"Authorization": f"Bearer {token}"}
