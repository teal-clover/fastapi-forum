import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_posts_read_all(client: AsyncClient):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [
        {"title": "title1", "content": "content1", "id": 1, "user_id": 1},
        {"title": "title2", "content": "content2", "id": 2, "user_id": 1},
    ]


@pytest.mark.anyio
async def test_posts_create_one(client: AsyncClient, token: str):

    response = await client.post(
        "/posts/",
        json={"title": "new_title", "content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json() == {
        "title": "new_title",
        "content": "new_content",
        "id": 3,
        "user_id": 2,
    }


@pytest.mark.anyio
async def test_posts_read_one(client: AsyncClient):
    response = await client.get("/posts/1")
    assert response.status_code == 200
    assert response.json() == {
        "title": "title1",
        "content": "content1",
        "id": 1,
        "user_id": 1,
    }


@pytest.mark.anyio
async def test_posts_update(client: AsyncClient, token: str):
    response = await client.put(
        "/posts/1",
        json={"title": "updated_title", "content": "updated_content"},
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "updated_title",
        "content": "updated_content",
        "id": 1,
        "user_id": 1,
    }


@pytest.mark.anyio
async def test_posts_delete(client: AsyncClient, token: str):
    response = await client.delete(
        "/posts/3", headers={"Authorization": "Bearer " + token}
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "new_title",
        "content": "new_content",
        "id": 3,
        "user_id": 2,
    }

    response = await client.get("/posts/3")
    assert response.status_code == 404
