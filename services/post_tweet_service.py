import os
import time
from datetime import datetime

from dotenv import load_dotenv

from constants import constants
from helpers.helper import generate_tweet
from logger import _logger
from services import media_service

load_dotenv()

bot_id = os.environ.get('BOT_ID')
bot_name = os.environ.get('BOT_NAME')
bot_target_country = os.environ.get('BOT_TARGET_COUNTRY')


# function for sending the tweet
def send_tweet(api, db_connection):
    try:
        my_tweet = generate_tweet(db_connection)

        # send the tweet message
        _logger().info("sending tweet...")
        image = media_service.attach_file_to_tweet()
        api.update_with_media(filename=image, status=my_tweet)
        _logger().info("Tweet sent successfully")

        # save the tweets posted to a file
        _logger().info("saving tweet...")
        current_data_time = datetime.now()
        date = current_data_time.strftime("%Y-%m-%d %H:%M")
        with open(f"{constants.bot_name}_logs.txt", 'a', encoding="utf-8") as f:
            f.write(f"\nPosted on {date} \n\n")
            f.write(my_tweet)
            f.write("\n************************************************************************************\n")
            f.close()

        _logger().info("Tweet saved successfully")
        _logger().info("sleeping...")
        _logger().info("\n")

        # setting interval between tweets
        time.sleep(600)
    except Exception as e:
        _logger().error(f"An error occurred when posting tweet {e}", exc_info=True)
        time.sleep(100)
