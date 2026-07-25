import pandas as pd
from google_play_scraper import reviews, Sort


def collect_reviews(app_id, count=500, lang="en", country="us"):
    """
    Collect Google Play Store reviews for the specified application.
    """

    result, continuation_token = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count
    )

    df = pd.DataFrame(result)

    return df


def save_reviews(df, output_path):
    """
    Save reviews to CSV.
    """

    df.to_csv(output_path, index=False)    