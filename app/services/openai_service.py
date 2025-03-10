import openai
from app.config import config

openai.api_key = config.OPENAI_API_KEY

async def generate_article(sector):
    prompt = f"Write a detailed news article about the latest trends in {sector}. It should be insightful and engaging."

    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a journalist writing insightful news articles."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )
    print('response: ', response.choices[0].message.content)

    return response.choices[0].message.content
