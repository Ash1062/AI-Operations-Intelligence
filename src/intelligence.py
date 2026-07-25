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
    """
    Generate AI-powered operational intelligence for a single issue category.
    """
    review_text = "\n".join(reviews.tolist())

    prompt = f"""
You are a senior Operations Intelligence Consultant.

You have received customer reviews already classified into the issue category:

{issue_category}

Analyze ONLY these reviews.

Your task:

1. Identify recurring operational themes.
2. Estimate frequency of each theme.
3. Identify probable operational root causes.
4. Explain business impact.
5. Recommend executive actions.
6. Assign priority:
   High
   Medium
   Low

Return ONLY valid JSON.

Format:

{{
 "issue_category":"",

 "themes":[
   {{
      "theme":"",
      "frequency":"",
      "root_cause":"",
      "business_impact":"",
      "recommendation":"",
      "priority":""
   }}
 ]
}}

Reviews:

{review_text}

"""
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text

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