from .conftest import client


def test_get_current_user():

    login_response = client.post(
        "/auth/token",
        data={
            "username": "admin@gmail.com",
            "password": "1234abc"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200