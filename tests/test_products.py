from .conftest import client


def test_create_product(vendor_token):
    response = client.post(
        "/products",
        json={
            "title": "Test Product",
            "price": 100,
            "stock": 10,
            "is_active": True
        },
        headers={"Authorization": f"Bearer {vendor_token}"}
    )

    assert response.status_code == 200


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert "data" in response.json()


def test_update_product(vendor_token, create_product):
    product_id = create_product["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "title": "Updated Product",
            "price": 200,
            "stock": 5
        },
        headers={"Authorization": f"Bearer {vendor_token}"}
    )

    assert response.status_code == 200


def test_delete_product(vendor_token, create_product):
    product_id = create_product["id"]

    response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {vendor_token}"}
    )

    assert response.status_code == 200