import os
import openai
from celery import Celery
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime, timezone
# from database import db

load_dotenv()

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
celery = Celery("tasks", broker=CELERY_BROKER_URL)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# # MongoDB Connection
MONGO_DB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client["CollaborativeArticles"]

SECTORS = ["Tech", "Health", "Corporate", "Politics", "Youth", "Lifestyle"]

@celery.task
async def generate_daily_articles():
    """
    Generates daily articles for different sectors using OpenAI.
    """
    now = datetime.now(timezone.utc).isoformat()

    for sector in SECTORS:
        prompt = f"Write a news article about the latest trends in {sector}. The article should be engaging and informative."
        
        try:
            response = openai.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a journalist writing insightful news articles."},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4o",
            )

            article_content = response["choices"][0]["message"]["content"]

            article_data = {
                "title": f"Latest {sector} Insights - {datetime.now().strftime('%B %d, %Y')}",
                "content": article_content,
                "sector": sector,
                "created_at": now,
                "updated_at": now
            }

            await db["articles"].insert_one(article_data)
            print(f"Generated article for {sector}")

        except Exception as e:
            print(f"Error generating article for {sector}: {e}")

