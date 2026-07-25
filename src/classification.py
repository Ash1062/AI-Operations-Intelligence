import pandas as pd


# -----------------------------
# Rating Sentiment
# -----------------------------

def rating_sentiment(score):
    if score <= 2:
        return "Negative"
    elif score == 3:
        return "Neutral"
    else:
        return "Positive"


# -----------------------------
# Text Sentiment
# -----------------------------

positive_words = [
    "good", "great", "helpful", "wonderful", "excellent",
    "easy", "love", "perfect", "awesome",
    "simple", "useful", "convenient"
]

negative_words = [
    "sucks", "doesn't work", "does not work",
    "terrible", "bad", "horrible",
    "useless", "frustrating",
    "hate", "awful",
    "broken", "worst",
    "problem", "issue",
    "bug", "crash", "slow"
]


def detect_text_sentiment(text):
    text = str(text).lower()

    if any(word in text for word in positive_words):
        return "Positive Text"

    elif any(word in text for word in negative_words):
        return "Negative Text"

    else:
        return "Unclear Text"


# -----------------------------
# Main Classification Pipeline
# -----------------------------

# Rules based classifier
def classify_issue(text):
    """
    Assign an operational issue category to a single review.
    """
    text = str(text).lower()

    if any(word in text for word in [
        "payment", "pay rent", "rent", "processing fee", "fee",
        "charge", "charges", "transaction", "bank", "card", "pay"
    ]):
        return "Payments"

    elif any(word in text for word in [
        "login", "log in", "logout", "logged out", "sign in",
        "signin", "password", "reset password", "can't login",
        "cannot login", "access", "account", "let me"
    ]):
        return "Authentication"

    elif any(word in text for word in [
        "maintenance", "repair", "request", "service request",
        "work order", "callback", "call back", "no response"
    ]):
        return "Maintenance"

    elif any(word in text for word in [
        "doesn't work", "does not work", "hard to use", "difficult to use", "not working",
        "confusing", "interface", "ui", "upload", "bright", "screen",
        "navigate", "navigation", "usability", "complicated", "app", "bad", "sucks"
    ]):
        return "UI / Usability"

    elif any(word in text for word in [
        "slow", "lag", "lagging", "loading", "takes forever",
        "freezing", "frozen"
    ]):
        return "Performance"

    elif any(word in text for word in [
        "won't open", "will not open", "doesn't open", "does not open",
        "crash", "crashes", "crashing", "bug", "blank", "white screen",
        "error", "glitch"
    ]):
        return "Stability"

    else:
        return "Other Operational Issue"

def classify_reviews(df):
    """
    Classify all operational reviews into issue categories.
    """
    df = df.copy()

    # Rating sentiment
    df["rating_sentiment"] = (
        df["score"].apply(rating_sentiment)
    )

    # Text sentiment
    df["text_sentiment"] = (
        df["content"].apply(detect_text_sentiment)
    )

    # Rating/Text validation
    df["rating_text_check"] = "Aligned"

    df.loc[
        (df["score"] <= 2) &
        (df["text_sentiment"] == "Positive Text"),
        "rating_text_check"
    ] = "Rating/Text Mismatch"

    df.loc[
        (df["score"] >= 4) &
        (df["text_sentiment"] == "Negative Text"),
        "rating_text_check"
    ] = "Rating/Text Mismatch"

    # Keep only operational reviews
    operational_reviews = df[
        (df["score"] <= 3) &
        (df["rating_text_check"] == "Aligned")
    ].copy()

    operational_reviews["issue_category"] = (
        operational_reviews["content"]
        .apply(classify_issue)
    )

    return operational_reviews



# -----------------------------
# Summary Table
# -----------------------------

def calculate_issue_summary(df):
    """
    Generate a summary of review counts for each issue category.
    """
    issue_counts = (
        df["issue_category"]
        .value_counts()
        .reset_index()
    )

    issue_counts.columns = [
        "issue_category",
        "review_count"
    ]

    issue_counts["percentage"] = round(
        (
            issue_counts["review_count"]
            / issue_counts["review_count"].sum()
        ) * 100,
        2
    )

    return issue_counts


# -----------------------------
# Save Functions
# -----------------------------

def save_classified_reviews(df, output_path):
    """
    Save classified operational reviews to a CSV file.
    """
    df.to_csv(output_path, index=False)


def save_issue_summary(df, output_path):
    """
    Save the issue summary table to a CSV file.
    """
    df.to_csv(output_path, index=False)