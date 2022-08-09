import praw
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_ID = os.getenv("APP_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")





