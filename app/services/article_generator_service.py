from app.services.openai_service import generate_article
from app.database.article_repository import ArticleRepository
from datetime import datetime, timezone
from app.config import config

class ArticleGeneratorService:
    """Handles AI-based article generation and saving to the database."""

    @staticmethod
    async def generate_and_save_articles():
        """Generates AI-powered articles for different sectors and saves them to the DB."""
        now = datetime.now(timezone.utc).isoformat()
        new_articles = []

        for sector in config.SECTORS:
            for subsector in sector["subsectors"]:
                content = await generate_article(sector, subsector)
                print('Generated content: ', content)

                article_data = {
                    "title": content.split("\n\n")[0].strip("*"),
                    "description": "\n\n".join(content.split("\n\n")[1:]), 
                    "tags": [sector["sector"], subsector] + sector["keywords"], 
                    "img": f"https://picsum.photos/800/450?{sector['sector']}", 
                    "authors": ['AI'],
                    "created_at": now,
                    "updated_at": now
                }
                new_articles.append(article_data)

        await ArticleRepository.bulk_insert_articles(new_articles)
        return {"message": "Articles generated successfully!"}
