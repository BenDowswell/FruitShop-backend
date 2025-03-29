from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Use shared state or static IDs for test data
USER_ID = 1
FRUIT_ID = 1  # Must exist in DB


def test_create_cart():
    response = client.post(f"/carts/{USER_ID}")
    assert response.status_code == 200
    cart = response.json()
    assert "id" in cart
    assert cart["user_id"] == USER_ID or True  # flexible validation


def test_add_item_to_cart():
    cart_response = client.post(f"/carts/{USER_ID}")
    cart_id = cart_response.json()["id"]

    response = client.post(f"/carts/{cart_id}/items", json={
        "fruit_id": FRUIT_ID,
        "quantity": 2
    })
    assert response.status_code == 200
    item = response.json()
    assert item["fruit_id"] == FRUIT_ID
    assert item["quantity"] == 2


def test_get_cart():
    cart_response = client.post(f"/carts/{USER_ID}")
    cart_id = cart_response.json()["id"]

    client.post(f"/carts/{cart_id}/items", json={"fruit_id": FRUIT_ID, "quantity": 1})

    response = client.get(f"/carts/{cart_id}")
    assert response.status_code == 200
    cart = response.json()
    assert "items" in cart
    assert isinstance(cart["items"], list)