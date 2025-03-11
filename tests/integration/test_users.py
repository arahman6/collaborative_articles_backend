import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db
from bson import ObjectId
from datetime import datetime

# Test user data
TEST_USER = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "Test@1234",
}

@pytest.fixture
def client():
    """Create a test client using FastAPI"""
    return TestClient(app)

@pytest.fixture(scope="session")
def event_loop():
    """Ensure a single event loop for all tests"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def setup_test_user():
    """Set up a test user in the mock database"""
    hashed_password = "$2b$12$examplehashedpassword"
    user_data = {
        "_id": ObjectId(),
        "username": TEST_USER["username"],
        "email": TEST_USER["email"],
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc),
    }
    await db["users"].insert_one(user_data)
    yield user_data
    await db["users"].delete_many({})  # Cleanup

def test_signup(client):
    """Test user signup"""
    response = client.post("/signup/", json=TEST_USER)
    assert response.status_code == 201
    assert "email" in response.json()

def test_login(client):
    """Test user login"""
    response = client.post("/login/", data={"username": TEST_USER["email"], "password": TEST_USER["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_profile(client, setup_test_user):
    """Test retrieving user profile"""
    token = test_login(client)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/profile/", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER["email"]

def test_update_profile(client, setup_test_user):
    """Test updating user profile"""
    token = test_login(client)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"bio": "Updated bio", "profile_picture": "https://example.com/profile.jpg"}
    response = client.put("/profile/", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"

def test_change_password(client, setup_test_user):
    """Test changing user password"""
    token = test_login(client)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/change-password/", json={"old_password": "Test@1234", "new_password": "NewPass@123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

def test_delete_account(client, setup_test_user):
    """Test deleting user account"""
    token = test_login(client)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/delete-account/", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully"
