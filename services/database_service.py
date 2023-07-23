# tpost-bot/services/database_service.py
import os

from dotenv import load_dotenv
from logger import _logger
from datetime import datetime
load_dotenv()

bot_id = os.environ.get('BOT_ID')
bot_target_country = os.environ.get('BOT_TARGET_COUNTRY')


def slogan_or_heading(db_connection, table_name):
    db_cursor = db_connection.cursor(buffered=True, dictionary=True)
    result = get_slogan_or_heading_from_db(db_cursor, table_name)
    if result is not None:
        update_slogan_or_heading_is_posted_status(db_connection, result['id'], table_name)
        db_cursor.close()

        return result['name']
    else:
        # TODO extract slogans/heading from the web
        return


def get_slogan_or_heading_from_db(db_cursor, table_name):
    query = f"SELECT * FROM {table_name} WHERE (bot_id=%s AND is_posted=%s)"
    db_cursor.execute(query, (bot_id, 0))
    result = db_cursor.fetchone()

    return result


def update_slogan_or_heading_is_posted_status(db_connection, item_id, table_name):
    db_cursor = db_connection.cursor(buffered=True)
    # mark slogan as posted
    update_query = f"UPDATE {table_name} SET is_posted=%s, updated_at=%s WHERE id=%s"
    current_data_time = datetime.now()
    date = current_data_time.strftime("%Y-%m-%d %H:%M")
    try:
        db_cursor.execute(update_query, (1, date, item_id))
        db_connection.commit()
        db_cursor.close()
    except Exception as e:
        _logger().error(f"Failed updating {table_name} is_posted status with error : {e}", exc_info=True)
        db_connection.rollback()


def get_item_from_db(db_connection, item_table):
    cursor = db_connection.cursor(buffered=True)
    query = f"SELECT name FROM {item_table} WHERE bot_id=%s"
    cursor.execute(query, [bot_id])
    result = cursor.fetchall()
    items = []
    for item in result:
        items.append(item[0])

    return items


def count_item_in_db(db_conn, item_table):
    cursor = db_conn.cursor(buffered=True)
    query = f"SELECT COUNT(*) FROM {item_table} WHERE bot_id=%s"
    cursor.execute(query, [bot_id])

    return cursor.fetchone()
