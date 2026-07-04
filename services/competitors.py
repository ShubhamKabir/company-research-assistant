import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_competitors(company_name: str, model: str):

    system_prompt = """
You are a senior business analyst.

Generate professional competitor analysis in Markdown.

Rules:
- Return ONLY Markdown.
- Do NOT include introductions.
- Do NOT include conclusions.
- Do NOT say "Here is the analysis".
- Return EXACTLY 5 competitors.
- Never include the target company itself.
- Keep the response concise.
- Use factual information only.
- Keep each competitor between 4 and 6 lines.
- Total response should be under 350 words.
"""

    user_prompt = f"""
Analyze the competitive landscape for:

{company_name}

For each competitor use EXACTLY this format:

## Competitor Name

Industry:
Why they compete:
Key strengths:
Key weaknesses:

Do not use tables.
Do not use bullet lists.
Do not add extra sections.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )

    return response.choices[0].message.content