import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_users_read_all(client: AsyncClient):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "title1",
            "content": "content1",
            "id": 1,
            "owner_id": 1
        },
        {
            "title": "title2",
            "content": "content2",
            "id": 2,
            "owner_id": 1
        }
    ]


@pytest.mark.anyio
async def test_users_create_one(client: AsyncClient):
    response = await client.post("/users/2/posts/", json={
        "title": "new_title",
        "content": "new_content"
    })
    assert response.status_code == 201
    assert response.json() == {
        "title": "new_title",
        "content": "new_content",
        "id": 3,
        "owner_id": 2
    }
