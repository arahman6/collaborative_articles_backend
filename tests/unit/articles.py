import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_article():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/articles/", json={
            "title": "New Tech Trends",
            "content": "Exploring AI and cloud technologies.",
            "tags": ["AI", "Cloud"]
        })
        assert response.status_code == 200
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_articles():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/articles/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_article_by_id():
    article_id = "some_valid_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/api/v1/articles/{article_id}")
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_update_article():
    article_id = "some_valid_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/api/v1/articles/{article_id}", json={
            "title": "Updated Tech Trends",
            "content": "Latest updates on AI and Cloud"
        })
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_delete_article():
    article_id = "some_valid_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/articles/{article_id}")
        assert response.status_code in [200, 404]
