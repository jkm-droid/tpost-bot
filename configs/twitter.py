# tpost-bot/twitter.py

import os

import tweepy
from dotenv import load_dotenv

from logger import _logger

load_dotenv()


def create_api():
    # getting the required keys and tokens from environment
    api_key = os.getenv('API_KEY')
    api_secret_key = os.getenv('API_SECRET_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret_token = os.getenv('ACCESS_SECRET_TOKEN')

    # Authenticating to twitter account
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret_token)

    # creating API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        username = api.me()
    except Exception as e:
        _logger().error("Error creating twitter api : {e}", exc_info=True)
        raise e

    _logger().info(f"connected to api successfully as {username.name}")

    return api
