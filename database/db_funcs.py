import sqlite3
from config import db_name


def add_user(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    result = False
    try:
        cursor.execute("INSERT INTO Users (Name) VALUES (?)", (name, ))
        conn.commit()
        result = True
    except Exception as err:
        print(f"Произошла ошибка при добавлении пользователя: {err}")
    finally:
        conn.close()
        return result


def list_of_users() -> str:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT UserID, Name, TelegramID FROM Users")
    users = cursor.fetchall()
    conn.close()
    if not users:
        return "Нет пользователей"
    else:
        text = "<b>Список пользователей</b>\n"
        for user in users:
            user_id, name, tg_id = user
            text += f"{user_id}. {name} - {'Активен' if tg_id else 'Неактивен'}\n"
    return text


def process_delete_user_db(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Users WHERE UserID = ?", (user_id, ))
    user = cursor.fetchone()
    conn.close()
    return user


def complete_deletion(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    result = False
    try:
        cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id, ))
        cursor.execute("DELETE FROM Auth_links WHERE UserID = ?", (user_id, ))
        conn.commit()
        result = True
    except Exception as err:
        print(f"Ошибка при удалении пользователя {err}")
    finally:
        conn.close()
        return result
