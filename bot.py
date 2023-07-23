import threading

from configs.database import create_db_connection
from configs.twitter import create_api
from logger import _logger
from services import bot_service, post_tweet_service


def bot_main():
    _logger().info("connecting to twitter api...")
    api = create_api()
    if api:
        _logger().info("connecting to database...")
        db_connection = create_db_connection()

        _logger()("initializing bot...")
        result = bot_service.initialize_bot(db_connection)
        while result:
            init_msg = result['initialized']
            if init_msg == 0:
                _logger().info("Some errors occurred when initializing bot. See more details in the error log file")
                break
            elif init_msg == 1:
                _logger().info("initialized bot successfully")
                # trend_thread = threading.Thread(target=hashtag_service.get_trends_by_location(api, db_connection))
                tweet_thread = threading.Thread(target=post_tweet_service.send_tweet(api, db_connection))
                # trend_thread.start()
                tweet_thread.start()
            else:
                _logger().info("An error occurred when initializing bot", exc_info=True)

    else:
        _logger().error("Connection to the api could not be established", exc_info=True)


if __name__ == "__main__":
    bot_main()
