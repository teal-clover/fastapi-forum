import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_comments_read_all(client: AsyncClient):
    response = await client.get("/comments/")
    print(response)
    assert response.status_code == 200
    assert response.json() == [
        {"content": "content1", "id": 1, "owner_id": 1},
        {"content": "content2", "id": 2, "owner_id": 1},
    ]


@pytest.mark.anyio
async def test_comments_create_one(client: AsyncClient):
    response_token = await client.post(
        "/users/token", data={"username": "user2@email.com", "password": "password"}
    )

    token = response_token.json()["access_token"]

    response = await client.post(
        "/comments/",
        json={"content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 201
    assert response.json() == {
        "content": "new_content",
        "id": 3,
        "owner_id": 2,
    }
