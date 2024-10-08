import jwt
import pytest
from fastapi import status
from httpx import AsyncClient
from jwt import InvalidTokenError

from forum.user.dependencies import ALGORITHM, SECRET_KEY


def verify_jwt(token) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except InvalidTokenError:
        return False


@pytest.mark.anyio
async def test_users_read_all(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"email": "user1@email.com", "id": 1, "is_active": True},
        {"email": "user2@email.com", "id": 2, "is_active": True},
    ]


@pytest.mark.anyio
async def test_users_read_one(client: AsyncClient):
    response = await client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"email": "user1@email.com", "id": 1, "is_active": True}


@pytest.mark.anyio
async def test_users_create_one(client: AsyncClient):
    response = await client.post(
        "/users/", json={"email": "email3@mail.com", "password": "password"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 3, "email": "email3@mail.com", "is_active": True}


@pytest.mark.anyio
async def test_users_update_one(client: AsyncClient):
    response = await client.put("/users/2", json={"email": "new_email@mail.com"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "email": "new_email@mail.com",
        "is_active": True,
    }


@pytest.mark.anyio
async def test_users_delete_one(client: AsyncClient):
    response = await client.delete("/users/2")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "email": "new_email@mail.com",
        "is_active": True,
    }


@pytest.mark.anyio
async def test_user_token(client: AsyncClient):
    response = await client.post(
        "/users/token", data={"username": "user1@email.com", "password": "password"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert verify_jwt(response.json()["access_token"])
