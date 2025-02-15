from motor.motor_asyncio import AsyncIOMotorClient
from app.config import config

client = AsyncIOMotorClient(config.MONGO_DB_URL)
client.admin.command('ping')
print("Connection successful!")
db = client["CollaborativeArticles"]



