from .conftest import client


# GET TOKEN (VENDOR)
def get_vendor_token():
    response = client.post(
        "/auth/token",
        data={
            "username": "vendor@gmail.com",
            "password": "1234abc"
        }
    )

    assert response.status_code == 200
    return response.json()["access_token"]


# GET ANY ORDER (HELPER)
def get_order_id():

    res = client.get("/orders")

    assert res.status_code == 200

    orders = res.json()["data"]

    if len(orders) == 0:
        return None

    return orders[0]["id"]


# GET ANY PRODUCT (HELPER)
def get_product_id():

    res = client.get("/products")

    assert res.status_code == 200

    products = res.json()["data"]

    if len(products) == 0:
        return None

    return products[0]["id"]


# CREATE ORDER ITEM
def test_create_order_item():

    token = get_vendor_token()

    order_id = get_order_id()
    product_id = get_product_id()

    if not order_id or not product_id:
        return

    response = client.post(
        "/order-items",
        json={
            "order_id": order_id,
            "product_id": product_id,
            "quantity": 2,
            "price": 100
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["quantity"] == 2


# GET ORDER ITEMS
def test_get_order_items():

    response = client.get("/order-items")

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "total_count" in data


# GET SINGLE ORDER ITEM
def test_get_single_order_item():

    res = client.get("/order-items")

    items = res.json()["data"]

    if len(items) == 0:
        return

    item_id = items[0]["id"]

    response = client.get(f"/order-items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "product_id" in data


# UPDATE ORDER ITEM
def test_update_order_item():

    token = get_vendor_token()

    res = client.get("/order-items")
    items = res.json()["data"]

    if len(items) == 0:
        return

    item_id = items[0]["id"]

    response = client.put(
        f"/order-items/{item_id}",
        json={
            "quantity": 5,
            "price": 200
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] == "Order item updated successfully"


# DELETE ORDER ITEM
def test_delete_order_item():

    token = get_vendor_token()

    res = client.get("/order-items")
    items = res.json()["data"]

    if len(items) == 0:
        return

    item_id = items[0]["id"]

    response = client.delete(
        f"/order-items/{item_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] == "Order item deleted successfully"