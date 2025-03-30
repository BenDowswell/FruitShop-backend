import random
import string
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_utils import get_token, auth_headers

client = TestClient(app)


def random_prefix():
    return "".join(random.choices(string.ascii_uppercase, k=1))


@pytest.fixture(scope="function")
def admin_token():
    return get_token(client, "admin", "admin")


def test_add_and_list_fruits():
    admin_token = get_token("admin", "admin")  # Pass only username and password
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


def test_update_fruit_as_admin(admin_token):
    prefix = random_prefix()
    headers = auth_headers(admin_token)

    create_response = client.post(
        "/fruits/",
        json={"name": "UpdateFruit", "prefix": prefix, "price": 2.49, "quantity": 10},
        headers=headers,
    )
    assert create_response.status_code == 200
    fruit = create_response.json()

    update_data = {
        "name": "UpdatedFruit",
        "prefix": prefix,
        "price": 3.99,
        "quantity": 50,
    }
    update_response = client.put(
        f"/fruits/{fruit['id']}", json=update_data, headers=headers
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "UpdatedFruit"


def test_delete_fruit_as_admin(admin_token):
    prefix = random_prefix()
    headers = auth_headers(admin_token)

    response = client.post(
        "/fruits/",
        json={"name": "DeleteFruit", "prefix": prefix, "price": 2.49, "quantity": 10},
        headers=headers,
    )
    assert response.status_code == 200
    fruit_id = response.json()["id"]

    delete_response = client.delete(f"/fruits/{fruit_id}", headers=headers)
    assert delete_response.status_code == 200
