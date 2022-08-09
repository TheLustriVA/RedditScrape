import praw
from dotenv import load_dotenv
import os
from user_agent import generate_navigator, generate_user_agent


def get_reddit_session():
    """_Return an authenticated Reddit session_

    Returns:
        _reddit_session_: _An authenticated reddit session_
    """
    load_dotenv()

    APP_NAME = os.getenv("APP_NAME")
    CLIENT_ID = os.getenv("CLIENT_ID")
    REDDIT_SECRET = os.getenv("REDDIT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    PASSWORD = os.getenv("PASSWORD")
    USERNAME = os.getenv("USERNAME")

    user_agent = "Excession MLVA_panopticon App V0.0.1"

    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=REDDIT_SECRET, password=PASSWORD, user_agent=user_agent, username=USERNAME)
    return reddit

        