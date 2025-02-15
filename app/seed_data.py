import motor.motor_asyncio
from datetime import datetime
from passlib.context import CryptContext
from collaborative_articles_backend.app.database import db


# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_data():
    now = datetime.now().isoformat()

    # Default articles
    articles = [
        {
            "title": "Introduction to AI",
            "content": "AI is changing the world. Let's dive into its impact.",
            "tags": ["AI", "Technology"],
            "created_at": now,
            "updated_at": now
        },
        {
            "title": "The Rise of Renewable Energy",
            "content": "Renewable energy sources are key to sustainability.",
            "tags": ["Energy", "Sustainability"],
            "created_at": now,
            "updated_at": now
        }
    ]

    # Default users (hashed passwords)
    users = [
        {"username": "admin", "email": "admin@example.com", "hashed_password": pwd_context.hash("adminpass123")},
        {"username": "john_doe", "email": "john.doe@example.com", "hashed_password": pwd_context.hash("password123")}
    ]

    # Check if articles already exist
    existing_articles = await db["articles"].count_documents({})
    if existing_articles == 0:
        await db["articles"].insert_many(articles)
        print("Articles seeded!")

    # Check if users already exist
    existing_users = await db["users"].count_documents({})
    if existing_users == 0:
        await db["users"].insert_many(users)
        print("Users seeded!")
