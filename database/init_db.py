import sqlite3
from config import db_name


def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        TelegramID INTEGER
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Auth_links(
        LinkCode TEXT NOT NULL,
        UserID INTEGER NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
        )""")

    conn.commit()
    cursor.close()
    conn.close()