import sqlite3
from config import db_name


def add_user(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Name) VALUES (?) RETURNING UserID", (name,))
        row = cursor.fetchone()
        conn.commit()
        if row:
            return row[0]
        else:
            return None
    except Exception as err:
        print(f"Произошла ошибка при добавлении пользователя: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


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
    cursor.execute("SELECT Name FROM Users WHERE UserID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def complete_deletion(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    result = False
    try:
        cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
        cursor.execute("DELETE FROM Auth_links WHERE UserID = ?", (user_id,))
        conn.commit()
        result = True
    except Exception as err:
        print(f"Ошибка при удалении пользователя {err}")
    finally:
        conn.close()
        return result


def add_link_code(user_id, link_code):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Auth_Links (UserID, LinkCode) VALUES (?, ?)", (user_id, link_code))
        conn.commit()
    except Exception as err:
        print(f"Произошла ошибка при добавлении пользователя: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def link_checking(link_code):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT LinkCode FROM Auth_links")
    linkcodes = cursor.fetchall()
    linkcodes = ["".join(linkcode) for linkcode in linkcodes]
    print(linkcodes)
    conn.close()
    if link_code in linkcodes:
        return True
    return False


# def fetch_link_data(link_code):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute("SELECT UserID FROM Auth_links WHERE LinkCode=?", (link_code,))
#     row = cursor.fetchone()
#     if row:
#         cursor.execute("DELETE FROM Auth_links WHERE UserID = ?", row)
#         conn.commit()
#     cursor.close()
#     conn.close()

