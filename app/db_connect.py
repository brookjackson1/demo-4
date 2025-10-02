import pymysql
import pymysql.cursors
from flask import g
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        try:
            # Check if all required environment variables are set
            db_host = os.getenv('DB_HOST')
            db_user = os.getenv('DB_USER')
            db_password = os.getenv('DB_PASSWORD')
            db_name = os.getenv('DB_NAME')

            if not all([db_host, db_user, db_password, db_name]):
                print("Missing database environment variables:")
                print(f"DB_HOST: {'✓' if db_host else '✗'}")
                print(f"DB_USER: {'✓' if db_user else '✗'}")
                print(f"DB_PASSWORD: {'✓' if db_password else '✗'}")
                print(f"DB_NAME: {'✓' if db_name else '✗'}")
                g.db = None
                return None

            g.db = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=60,
                read_timeout=60,
                write_timeout=60,
                charset='utf8mb4'
            )
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            print(f"Host: {os.getenv('DB_HOST', 'Not set')}")
            print(f"Database: {os.getenv('DB_NAME', 'Not set')}")
            g.db = None
            return None
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()