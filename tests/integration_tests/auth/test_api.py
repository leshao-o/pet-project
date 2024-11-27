import pytest


@pytest.mark.parametrize(
    "email, password",
    [
        ("user@mail.ru", "password123"),
        ("qwe123@yandex.ru", "yandex_qwe"),
        ("example@gmail.com", "12345qwert"),
    ],
)
async def test_authentication_and_authorization(email, password, ac):
    response_register = await ac.post("/auth/register", json={"email": email, "password": password})
    assert response_register.status_code == 200

    response_login = await ac.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert response_login.status_code == 200
    assert ac.cookies["access_token"]

    response_get_me = await ac.get(
        "/auth/me",
    )
    assert response_get_me.status_code == 200
    assert response_get_me.json()["email"] == email

    response_logout = await ac.post("/auth/")
    assert response_logout.status_code == 200

    response_get_me = await ac.get(
        "/auth/me",
    )
    assert response_get_me.status_code == 401
