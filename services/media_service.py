import os
import pathlib
import random

from PIL import ImageFont, Image, ImageDraw
from helpers.image_utils import ImageText
from helpers.helper import *
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
    image = Image.open(raw_image)
    image_extension = pathlib.Path(raw_image).suffix
    _logger().info(image_extension)

    fonts_path = f"{os.getcwd()}/assets/fonts"
    font_file = f"{fonts_path}/FreeMonoBold.ttf"
    font_size = 60

    text = get_slogan(db_connection)
    text_color = (50, 50, 50)
    _logger().info(text)

    image_width, image_height = image.size
    if image_width > 400 and image_height > 300:
        final_image = ImageText(image)
    else:
        final_image = ImageText((800, 600), background='darkorange') # 200 = alpha

    final_image.write_text_box(
        (0, image_height/2),
        text,
        box_width=image_width,
        font_filename="FreeMonoBold.ttf",
        font_size=font_size,
        color=text_color,
        place='center'
    )
    final_image.save(f"sample{image_extension}")
    final_image.show()
