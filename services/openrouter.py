import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Change to True only if you need debugging
DEBUG = False


def generate_company_report(company_data: str, model: str):

    system_prompt = """
You are a senior business analyst.

Generate a professional company research report.

Rules:
- Return ONLY Markdown.
- Do NOT include conversational text.
- Do NOT say:
  - Certainly
  - Here is the report
  - Based on the provided information
  - Below is the analysis
  - Let me know if...
- Start immediately with the first heading.
- Do NOT include your own instructions or the word "Requirements" in the output.
- Do NOT repeat the prompt.
- Do NOT list products belonging to the company as competitors.
- Use concise, factual language.
- Use bullet points where appropriate.
- Use tables only if they genuinely improve readability.

The report must contain these sections in this exact order:

# Company Summary

# Products & Services

# AI-Generated Pain Points

# Suggested Competitors
"""

    user_prompt = f"""
Company Information:

{company_data}
"""

    if DEBUG:
        print(f"Using model: {model}")

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
        temperature=0.3,
    )

    if DEBUG:
        print("=" * 80)
        print(f"Model Used: {response.model}")
        print(f"Provider: {response.provider}")
        print(response.choices[0].message.content[:500])
        print("=" * 80)

    return response.choices[0].message.content