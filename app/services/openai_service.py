import openai
from app.config import config

openai.api_key = config.OPENAI_API_KEY

async def generate_article(sector, word_count=500, tone="insightful and engaging"):
    """Generates an AI-written article for a given sector using OpenAI API."""
    prompt = (
        f"Write a detailed news article about the latest trends in {sector}. "
        f"Make it {word_count} words long and ensure it is {tone}."
    )

    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a journalist writing insightful news articles."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )

    return response.choices[0].message.content
