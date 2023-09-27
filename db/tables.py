from db.base import connect_db, commit_and_close


def create_users_table():
    connection, cursor = connect_db("../weather.db")
    sql = '''
    drop table if exists users;
    create table if not exists users(
    user_id integer primary key autoincrement,
    username text
    );
    '''
    cursor.executescript(sql)

    commit_and_close(connection)


def create_weather_table():
    connection, cursor = connect_db("../weather.db")
    sql = '''
    drop table if exists weather;
    create table if not exists weather(
        weather_id integer primary key autoincrement,
        name text,
        tz integer,
        sunrise datetime,
        dt datetime,
        speed decimal,
        
        user_id integer references users(user_id)        
    );
    '''
    cursor.executescript(sql)
    commit_and_close(connection)

# create_weather_table()
# create_users_table()
