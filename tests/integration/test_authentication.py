import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/signup/", json={
            "email": "testuser@example.com",
            "password": "securepassword"
        })
        assert response.status_code == 200
        assert "email" in response.json()

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/login/", data={ 
            "username": "testuser@example.com",
            "password": "securepassword"
        })
        assert response.status_code == 200
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/login/", data={  
            "username": "wronguser@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 400  
