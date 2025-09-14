import logging
from poetry_handler import get_random_poem_message
from config import load_env
from utils import post_tweet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Main entry point: build a poem message and post it."""
    load_env()
    message = get_random_poem_message()
    post_tweet(message)

if __name__ == "__main__":
    main()
