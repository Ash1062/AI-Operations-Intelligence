import pandas as pd

def sentiment_bucket(score):
    """
    Convert a review score into a sentiment label.
    """

    if score <= 2:
        return "Negative"

    elif score == 3:
        return "Neutral"

    else:
        return "Positive"

def clean_reviews(df):
    """
    Clean and enrich the review DataFrame.
    """

    df = df.copy()

    df["review_length"] = df["content"].str.len()

    df["sentiment"] = df["score"].apply(sentiment_bucket)

    return df

def save_cleaned_reviews(df, output_path):
    """
    Save the cleaned reviews to CSV.
    """

    df.to_csv(output_path, index=False)