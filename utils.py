import logging
import requests
from requests_oauthlib import OAuth1
from config import get_api_credentials

def latin_to_persian_digits(text: str) -> str:
    return text.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))

def post_tweet(message: str) -> None:
    creds = get_api_credentials()
    if not all(creds.values()):
        logging.error("Missing API credentials in environment variables.")
        return

    auth = OAuth1(
        client_key=creds["API_KEY"],
        client_secret=creds["API_SECRET"],
        resource_owner_key=creds["ACCESS_TOKEN"],
        resource_owner_secret=creds["ACCESS_TOKEN_SECRET"],
    )

    url = "https://api.x.com/2/tweets"
    payload = {"text": message}

    try:
        response = requests.post(url, json=payload, auth=auth, timeout=10)
        response.raise_for_status()
        logging.info("tweet posted successfully: %s", response.json())
    except requests.exceptions.RequestException as e:
        logging.error("error posting tweet: %s", str(e))
