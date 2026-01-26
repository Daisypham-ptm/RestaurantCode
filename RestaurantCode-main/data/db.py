import sqlite3
import os

# Root project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database folder
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "restaurant_menu.db")


def get_connection():
    """
    Tạo và trả về kết nối SQLite
    """
    os.makedirs(DB_DIR, exist_ok=True)  # database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # connect
    return conn


def close_connection(conn):
    if conn:
        conn.close()

