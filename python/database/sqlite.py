import sqlite3
import os

from flask import g

init = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);
"""

def init_db():
    connection = connect()
    cursor = connection.cursor()
    cursor.executescript(init)
    connection.commit()
    connection.close()

def connect():
    db_path = os.getenv("DATABASE_PATH", "../database.sqlite")
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection