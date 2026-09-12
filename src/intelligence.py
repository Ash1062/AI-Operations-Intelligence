import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# ------------------------------
# Intelligence Engine
# ------------------------------
def generate_operational_intelligence(issue_category, reviews):

    review_text = "\n".join(
        f"- {review}" for review in reviews
    )

    prompt = f"""
You are an Operations Intelligence Analyst.

The following customer reviews have ALREADY been classified into the issue category:

Issue Category: {issue_category}

Reviews:
{review_text}

Your job is to identify recurring operational problems and generate executive-level intelligence.

Return ONLY valid JSON in the following format:

{{
  "issue_category": "{issue_category}",
  "themes": [
    {{
      "theme": "...",
      "frequency": "...",
      "root_cause": "...",
      "business_impact": "...",
      "recommendation": "...",
      "priority": "High"
    }}
  ]
}}

Rules:
- Identify the TOP 3–5 DISTINCT recurring themes.
- Do NOT merge unrelated problems into one theme.
- Sort themes from highest to lowest frequency.
- Every theme must include frequency, root_cause, business_impact, recommendation, and priority.
- Priority must be High, Medium, or Low.
- Return ONLY JSON. No markdown or explanation.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert business operations analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def generate_all_intelligence(df):
    """
    Generate operational intelligence for every issue category in the dataset.
    """
    categories = df["issue_category"].unique()

    all_results = []

    for category in categories:

        reviews = df[
            df["issue_category"] == category
        ]["content"]

        print(f"Analyzing {category}...")

        result = generate_operational_intelligence(
            category,
            reviews
        )

        all_results.append(result)

    return all_results

# -------------------------
# Save function
# -------------------------
def save_intelligence(results, output_path):
    """
    Save generated operational intelligence to a JSON file.
    """
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )
