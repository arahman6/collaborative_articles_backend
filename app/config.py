import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_DB_URL = os.getenv("MONGODB_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    SECTORS = ["Tech", "Health", "Corporate", "Politics", "Youth", "Lifestyle"]

config = Config()
