import openai
from app.config import config
import datetime

openai.api_key = config.OPENAI_API_KEY

async def generate_article(sector, subsector, word_count=500, tone="insightful and engaging"):
    """Generates an AI-written article for a given sector using OpenAI API."""
    current_year = datetime.datetime.now().year
    next_year = current_year + 1
    prompt = (
        f"""
            As a {sector['sector']} journalist, write {word_count}-word article about {subsector}.
            Audience: {sector['audience']}
            Structure: Introduction -> Trend Analysis -> Challenges -> Future Predictions
            Include: 
            - Include recent market data from {current_year}-{next_year % 100:02d}
            - 2 expert quotes
            - Both optimistic and skeptical viewpoints
            - Explain technical terms
            SEO Keywords: {", ".join(sector['keywords'])}
            Perspective: {sector['perspective']}
            Tone: Insightful yet accessible
            """
    )

    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a journalist writing insightful news articles."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )

    return response.choices[0].message.content
