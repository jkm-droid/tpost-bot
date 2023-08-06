import os
import random

from helpers import image_utils
from services import database_service
from logger import _logger


def get_slogan(db_connection):
    slogan = database_service.slogan_or_heading(db_connection, "slogans")

    # slogan = translate_to_lang(slogan)

    return slogan


def get_image_from_storage():
    path = f"{os.getcwd()}/filenames"
    media_list = []
    for dirpath, dirnames, files in os.walk(path):
        for f in files:
            media_list.append(os.path.join(dirpath, f))
    image = random.choice(media_list)

    return image


def add_slogan_on_image(db_connection):
    raw_image = get_image_from_storage()

    fonts_path = f"{os.getcwd()}/assets/fonts"
    font_file = f"{fonts_path}/FreeMonoBold.ttf"
    font_size = 36

    text = get_slogan(db_connection)
    text_color = (50, 50, 50)
    _logger().info(text)

    image_utils.wrap_text(raw_image, text, font_file, font_size)
