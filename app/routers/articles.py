from fastapi import APIRouter, HTTPException, Depends
from app.database import db
from app.models import Article
from datetime import datetime, timezone
from app.services.openai_service import generate_article
from bson import ObjectId

articles_router = APIRouter()

# Create a new article
@articles_router.post("/articles/")
async def create_article(article: Article):
    article_data = article.dict()
    article_data["created_at"] = datetime.now(timezone.utc)
    article_data["updated_at"] = datetime.now(timezone.utc)
    result = await db["articles"].insert_one(article_data)
    return {"id": str(result.inserted_id)}

# Get all articles
@articles_router.get("/articles/")
async def get_articles():
    articles = await db["articles"].find().to_list(100)
    for article in articles:
        article["_id"] = str(article["_id"])
    return articles

# Get a single article by ID
@articles_router.get("/articles/{article_id}")
async def get_article(article_id: str):
    article = await db["articles"].find_one({"_id": ObjectId(article_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article["_id"] = str(article["_id"])
    return article

# Update an article by ID
@articles_router.put("/articles/{article_id}")
async def update_article(article_id: str, article: Article):
    article_data = article.dict(exclude_unset=True)
    article_data["updated_at"] = datetime.now(timezone.utc)
    result = await db["articles"].update_one({"_id": ObjectId(article_id)}, {"$set": article_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Article not found or no changes made")
    return {"message": "Article updated successfully"}

# Delete an article by ID
@articles_router.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    result = await db["articles"].delete_one({"_id": ObjectId(article_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted successfully"}

# Generate articles for each sector
@articles_router.post("/articles/generate/")
async def create_article():
    now = datetime.now(timezone.utc).isoformat()
    new_articles = []

    for sector in ["Tech", "Health", "Corporate", "Politics", "Youth", "Lifestyle"]:
        content = await generate_article(sector)
        article_data = {
            "title": f"Latest {sector} Insights - {datetime.now().strftime('%B %d, %Y')}",
            "description": content,  # Renamed 'content' to 'description'
            "tags": [sector],  # Changed 'sector' to a list of tags
            "img": "https://source.unsplash.com/random/800x450?{sector}",  # Added a default image
            "authors": [],  # Placeholder for authors
            "created_at": now,
            "updated_at": now
        }
        new_articles.append(article_data)

    await db["articles"].insert_many(new_articles)
    return {"message": "Articles generated successfully!"}

