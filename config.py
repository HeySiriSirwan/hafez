import os
from dotenv import load_dotenv

def load_env() -> None:
    load_dotenv()

def get_api_credentials():
    return {
        "API_KEY": os.getenv("API_KEY"),
        "API_SECRET": os.getenv("API_SECRET"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET"),
    }
