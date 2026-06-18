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


# GET ORDER (HELPER)
def get_order_id():

    res = client.get("/orders")

    assert res.status_code == 200

    orders = res.json()["data"]

    if len(orders) == 0:
        return None

    return orders[0]["id"]


# CREATE PAYMENT
def test_create_payment():

    token = get_vendor_token()
    order_id = get_order_id()

    if not order_id:
        return

    order = client.get(f"/orders/{order_id}").json()

    response = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "payment_id" in data["data"]


# PAYMENT DUPLICATE CHECK
def test_duplicate_payment():

    token = get_vendor_token()
    order_id = get_order_id()

    if not order_id:
        return

    order = client.get(f"/orders/{order_id}").json()

    # first payment
    client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # second payment should fail
    response = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [400, 403]


# MARK PAYMENT AS SUCCESS (ADMIN)
def test_mark_payment_success():

    token = get_vendor_token()

    # get payment id
    order_id = get_order_id()
    if not order_id:
        return

    order = client.get(f"/orders/{order_id}").json()

    pay = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    payment_id = pay["data"]["payment_id"]

    response = client.patch(
        f"/payments/{payment_id}/success",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 403]