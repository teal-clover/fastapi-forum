import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_posts_read_all(client: AsyncClient):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [
        {"title": "title1", "content": "content1", "id": 1, "owner_id": 1},
        {"title": "title2", "content": "content2", "id": 2, "owner_id": 1},
    ]


@pytest.mark.anyio
async def test_posts_create_one(client: AsyncClient):
    response_token = await client.post(
        "/users/token", data={"username": "user2@email.com", "password": "password"}
    )

    token = response_token.json()["access_token"]

    response = await client.post(
        "/posts/",
        json={"title": "new_title", "content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 201
    assert response.json() == {
        "title": "new_title",
        "content": "new_content",
        "id": 3,
        "owner_id": 2,
    }
