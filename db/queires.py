from .base import connect_db, commit_and_close


def check_user_exists(db_name, username):
    connection, cursor = connect_db(db_name)

    cursor.execute('select * from users where username = ?;', (username,))
    user = cursor.fetchone()
    if not user:
        return False, False
    return True, user[0]


def add_user(db_name, username):
    connection, cursor = connect_db(db_name)
    cursor.execute('insert into users(username) values (?);', (username,))
    commit_and_close(connection)
    print("user added:", username)


def add_weather(db_name, **kwargs):
    connection, cursor = connect_db(db_name)
    keys = ", ".join(list(kwargs.keys()))
    values = tuple(kwargs.values())
    signs = ", ".join(["?" for _ in range(len(values))])
    sql = f"insert into weather({keys}) values ({signs});"
    cursor.execute(sql, values)
    commit_and_close(connection)


def get_user_weather(db_name, user_id):
    connection, cursor = connect_db(db_name)
    sql = "select * from weather where user_id = ?;"
    cursor.execute(sql, (user_id,))
    return cursor.fetchall()


def clear_user_weather(db_name, user_id):
    connection, cursor = connect_db(db_name)

    sql = "delete from weather where user_id = ?"
    cursor.execute(sql, (user_id,))
    commit_and_close(connection)
