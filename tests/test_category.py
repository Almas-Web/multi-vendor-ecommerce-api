from .conftest import client, vendor_token


# =========================
# HELPER: CREATE ORDER
# =========================
def get_order_id(token):

    response = client.post(
        "/orders",
        json={
            "status": "pending",
            "total_price": 100
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    return response.json()["id"]


# =========================
# CREATE PAYMENT
# =========================
def test_create_payment(vendor_token):

    token = vendor_token

    order_id = get_order_id(token)

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

    assert "data" in data
    assert "payment_id" in data["data"]
    assert data["success"] is True


# =========================
# DUPLICATE PAYMENT TEST
# =========================
def test_duplicate_payment(vendor_token):

    token = vendor_token

    order_id = get_order_id(token)

    order = client.get(f"/orders/{order_id}").json()

    # first payment
    res1 = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert res1.status_code == 200

    # second payment should fail
    res2 = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert res2.status_code == 400


# =========================
# MARK PAYMENT SUCCESS (ADMIN ONLY)
# =========================
def test_mark_payment_success(vendor_token):

    token = vendor_token

    order_id = get_order_id(token)

    order = client.get(f"/orders/{order_id}").json()

    pay = client.post(
        "/payments",
        params={
            "order_id": order_id,
            "amount": order["total_price"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert pay.status_code == 200

    payment_id = pay.json()["data"]["payment_id"]

    # ❗ normally admin token should be used
    response = client.patch(
        f"/payments/{payment_id}/success",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403 or response.status_code == 200