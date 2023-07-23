import os
from datetime import datetime
from dotenv import load_dotenv
from logger import _logger

load_dotenv()
bot_id = os.environ.get('BOT_ID')
bot_name = os.environ.get('BOT_NAME')
bot_user_id = os.environ.get('BOT_USER_ID')


def keyword(db_connection, sub_reddit_id):
    db_cursor = db_connection.cursor(buffered=True, dictionary=True)
    keyword_result = get_keyword_from_db(db_cursor)
    if keyword_result is not None:
        update_keyword_is_extracted_status(db_connection, keyword_result['id'])
        db_cursor.close()

        # return keyword name
        return {
            'set_to_default': 0,
            'keyword_name': keyword_result['name']
        }
    else:
        # mark keywords as un-extracted/is_extracted = 0
        update_all_keywords_is_extracted_status(db_connection, sub_reddit_id)

        _result = get_keyword_from_db(db_cursor)
        db_cursor.close()
        # set extracted status to true
        update_keyword_is_extracted_status(db_connection, _result['id'])

        return {
            'set_to_default': 1,
            'keyword_name': _result['name']
        }


def get_keyword_from_db(cursor):
    keyword_query = "SELECT * FROM keywords WHERE (bot_id=%s AND is_extracted=%s)"
    cursor.execute(keyword_query, (bot_id, 0))
    result = cursor.fetchone()

    return result


def update_all_keywords_is_extracted_status(db_connection, sub_reddit_id):
    try:
        db_cursor = db_connection.cursor(buffered=True)
        # update all keywords for this bot to false
        update_query = "UPDATE keywords SET is_extracted=%s WHERE bot_id=%s"
        db_cursor.execute(update_query, (0, bot_id))
        db_connection.commit()
        db_cursor.close()
    except Exception as e:
        _logger().error(f"Failed updating all keywords is extracted status with error : {e}", exc_info=True)
        db_connection.rollback()


def update_keyword_is_extracted_status(db_connection, keyword_id):
    db_cursor = db_connection.cursor(buffered=True)
    # mark keyword as extracted
    update_query = "UPDATE keywords SET is_extracted=%s, updated_at=%s WHERE id=%s"
    current_data_time = datetime.now()
    date = current_data_time.strftime("%Y-%m-%d %H:%M")
    try:
        db_cursor.execute(update_query, (1, date, keyword_id))
        db_connection.commit()
        db_cursor.close()
    except Exception as e:
        _logger().error(f"Failed updating keyword is_ extracted status with error : {e}", exc_info=True)
        db_connection.rollback()
