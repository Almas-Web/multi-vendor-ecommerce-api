import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# =========================
# CLIENT FIXTURE
# =========================
@pytest.fixture
def client_fixture():
    return client


# =========================
# VENDOR TOKEN FIXTURE
# =========================
@pytest.fixture
def vendor_token():

    response = client.post(
        "/auth/token",
        data={
            "username": "vendor@gmail.com",
            "password": "1234abc"
        }
    )

    assert response.status_code == 200
    return response.json()["access_token"]


# =========================
# PRODUCT FIXTURE
# =========================
@pytest.fixture
def create_product(vendor_token):

    response = client.post(
        "/products",
        json={
            "title": "Fixture Product",
            "price": 100,
            "stock": 10,
            "is_active": True
        },
        headers={
            "Authorization": f"Bearer {vendor_token}"
        }
    )

    assert response.status_code == 200
    return response.json()