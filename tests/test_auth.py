from .conftest import client


def test_login():

    response = client.post(
        "/auth/token",
        data={
            "username": "admin@gmail.com",
            "password": "1234abc"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data