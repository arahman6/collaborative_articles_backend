import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
client.admin.command('ping')
print("Connection successful!")
db = client["CollaborativeArticles"]