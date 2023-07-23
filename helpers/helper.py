# tpost-bot/helper.py
import os
import random

from googletrans import Translator
from logger import _logger
from services import database_service

translator = Translator()
should_translate = os.environ.get('TRANSLATE')
trans_lang = os.environ.get('LANGUAGE')


def get_heading(db_connection):
    db_headings = database_service.slogan_or_heading(db_connection, "headings")
    heading = random.choice(db_headings)

    heading = translate_to_lang(heading)

    return heading


def generate_tweet(db_connection):
    # get the generated heading 1
    heading = get_heading(db_connection)

    # embed the keyword in the tweet message
    my_tweet = "{heading}\n".format(heading=heading)

    _logger().info(f"Before check:{len(my_tweet)}")
    if len(my_tweet) > 278:
        generate_tweet(db_connection)

    _logger().info(f"After check:{len(my_tweet)}")
    return my_tweet


def translate_to_lang(message):
    if should_translate:
        translated_message = translator.translate(message, dest=trans_lang)

        return translated_message.text
    else:
        return message
