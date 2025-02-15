import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_add_comment():
    article_id = "some_valid_article_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/comments/", json={
            "article_id": article_id,
            "content": "This is a great article!"
        })
        assert response.status_code == 200
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_comments():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/comments/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_comment_by_id():
    comment_id = "some_valid_comment_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/api/v1/comments/{comment_id}")
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_update_comment():
    comment_id = "some_valid_comment_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/api/v1/comments/{comment_id}", json={
            "content": "Updated comment content."
        })
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_delete_comment():
    comment_id = "some_valid_comment_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/comments/{comment_id}")
        assert response.status_code in [200, 404]
