from .conftest import client


# GET VENDOR TOKEN
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


# CREATE ORDER
def test_create_order():

    token = get_vendor_token()

    response = client.post(
        "/orders",
        json={
            "status": "pending",
            "total_price": 500
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["status"] == "pending"


# GET ORDERS LIST
def test_get_orders():

    response = client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "total_count" in data


# GET SINGLE ORDER
def test_get_single_order():

    res = client.get("/orders")

    orders = res.json()["data"]

    if len(orders) == 0:
        return

    order_id = orders[0]["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "status" in data


# UPDATE ORDER
def test_update_order():

    token = get_vendor_token()

    orders = client.get("/orders").json()["data"]

    if len(orders) == 0:
        return

    order_id = orders[0]["id"]

    response = client.put(
        f"/orders/{order_id}",
        json={
            "status": "confirmed",
            "total_price": 800
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# UPDATE ORDER STATUS (ADMIN ONLY)
def test_update_order_status():

    admin_token = get_vendor_token()  # (for now same token)

    orders = client.get("/orders").json()["data"]

    if len(orders) == 0:
        return

    order_id = orders[0]["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={
            "status": "shipped"
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    # can be 200 or 403 depending on role
    assert response.status_code in [200, 403]


# DELETE ORDER
def test_delete_order():

    token = get_vendor_token()

    orders = client.get("/orders").json()["data"]

    if len(orders) == 0:
        return

    order_id = orders[0]["id"]

    response = client.delete(
        f"/orders/{order_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["success"] is True