import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_competitors(company_name: str, model: str):

    prompt = f"""
You are an experienced business analyst.

For the company "{company_name}", generate a competitor analysis.

Return exactly FIVE competitors.

For each competitor provide:

## Competitor Name

Industry

Why they compete

Key strengths

Key weaknesses

Keep the answer concise and professional.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content