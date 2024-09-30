import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_one_comment(client: AsyncClient, token: str):
    # given
    post_id = 1
    # when
    response = await client.post(
        f"/comments/{post_id}",
        json={"content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )
    # then
    assert response.status_code == 201
    assert response.json() == {
        "content": "new_content",
        "id": 3,
        "user_id": 2,
    }


@pytest.mark.anyio
async def test_like_a_comment(client: AsyncClient, token: str):
    # given
    comment_id = 1
    # when
    like_response = await client.post(
        f"/comments/likes/{comment_id}",
        headers={"Authorization": "Bearer " + token},
    )
    list_likes_response = await client.get(
        f"/comments/likes/{comment_id}", headers={"Authorization": "Bearer " + token}
    )
    # then
    assert like_response.status_code == 200
    assert list_likes_response.status_code == 200
    assert list_likes_response.json() == [
        {"email": "user2@email.com", "id": 2, "is_active": True}
    ]


@pytest.mark.anyio
async def test_edit_comment(client: AsyncClient, token: str):
    # given
    comment_id = 1
    # when
    response = await client.put(
        f"/comments/{comment_id}",
        json={"content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )
    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_delete_comment(client: AsyncClient, token: str):
    # given
    comment_id = 1
    # when
    response = await client.put(
        f"/comments/{comment_id}",
        json={"content": "new_content"},
        headers={"Authorization": "Bearer " + token},
    )
    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_get_comment_by_post(client: AsyncClient, token: str):
    # given
    post_id = 1
    # when
    response = await client.get(
        f"/comments/post/{post_id}",
        headers={"Authorization": "Bearer " + token},
    )
    # then
    assert response.status_code == status.HTTP_200_OK
