# tpost-bot/database.py

import os

import mysql.connector as mysql
from dotenv import load_dotenv
from mysql.connector import errorcode

from logger import _logger

# load env variables
load_dotenv()

"""
Establish connection to the db
"""


def create_db_connection():
    host = os.environ.get('DB_HOST')
    database = os.environ.get('DB_DATABASE')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    try:
        connection = mysql.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        _logger().info("Database connection established successfully")
        return connection
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            _logger().error("Access denied:Please recheck your username/password", exc_info=True)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            _logger().error("Database does not exist", exc_info=True)
        else:
            _logger().error(err, exc_info=True)
