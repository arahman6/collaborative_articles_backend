import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_add_contribution():
    article_id = "some_valid_article_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/contributions/", json={
            "article_id": article_id,
            "content": "Adding a valuable contribution!"
        })
        assert response.status_code == 200
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_contributions():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/contributions/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_contribution_by_id():
    contribution_id = "some_valid_contribution_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/api/v1/contributions/{contribution_id}")
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_update_contribution():
    contribution_id = "some_valid_contribution_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/api/v1/contributions/{contribution_id}", json={
            "content": "Updated contribution content."
        })
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_delete_contribution():
    contribution_id = "some_valid_contribution_id"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/contributions/{contribution_id}")
        assert response.status_code in [200, 404]
