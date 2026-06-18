from .conftest import client


# -------------------------
# GET TOKEN
# -------------------------
def get_token():

    response = client.post(
        "/auth/token",
        data={
            "username": "vendor@gmail.com",
            "password": "1234abc"
        }
    )

    return response.json()["access_token"]


# -------------------------
# CREATE PRODUCT (for cart testing)
# -------------------------
def create_product(token):

    response = client.post(
        "/products",
        json={
            "title": "Cart Test Product",
            "price": 100,
            "stock": 10,
            "is_active": True
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.json()


# -------------------------
# CREATE CART
# -------------------------
def create_cart(token):

    response = client.post(
        "/carts",
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.json()


# -------------------------
# ADD ITEM TO CART
# -------------------------
def test_cart_flow():

    token = get_token()

    product = create_product(token)
    cart = create_cart(token)

    cart_id = cart["id"]
    product_id = product["id"]

    # ADD ITEM
    response = client.post(
        "/cart-items",
        json={
            "cart_id": cart_id,
            "product_id": product_id,
            "quantity": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    # GET CART ITEMS
    res = client.get(f"/cart-items/cart/{cart_id}",
                     headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200

    items = res.json()
    assert len(items) > 0

    item_id = items[0]["id"]

    # UPDATE ITEM
    res2 = client.put(
        f"/cart-items/{item_id}",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res2.status_code == 200

    # DELETE ITEM
    res3 = client.delete(
        f"/cart-items/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res3.status_code == 200