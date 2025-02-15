import os
import openai
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB Connection
MONGO_DB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client["CollaborativeArticles"]

# List of sectors for article generation
SECTORS = ["Tech", "Health", "Corporate", "Politics", "Youth", "Lifestyle"]

async def generate_articles():
    """
    Manually generates articles for different sectors and stores them in MongoDB.
    """
    now = datetime.now(timezone.utc).isoformat()
    new_articles = []

    for sector in SECTORS:
        prompt = f"Write a detailed news article about the latest trends in {sector}. It should be insightful and engaging."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a journalist writing insightful news articles."},
                    {"role": "user", "content": prompt}
                ]
            )

            article_content = response["choices"][0]["message"]["content"]

            article_data = {
                "title": f"Latest {sector} Insights - {datetime.now().strftime('%B %d, %Y')}",
                "content": article_content,
                "sector": sector,
                "created_at": now,
                "updated_at": now
            }

            new_articles.append(article_data)
            print(f"✅ Successfully generated article for {sector}")

        except Exception as e:
            print(f"❌ Error generating article for {sector}: {e}")

    # Insert all generated articles into MongoDB
    if new_articles:
        await db["articles"].insert_many(new_articles)
        print("✅ All articles stored in MongoDB!")

# Run the async function manually
if __name__ == "__main__":
    asyncio.run(generate_articles())
