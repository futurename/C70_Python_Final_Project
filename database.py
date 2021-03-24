import sqlite3

SQLITE_PATH = "data_source/database.db"

DB_CONN = sqlite3.connect(SQLITE_PATH)


def get_db():
    return DB_CONN


def close_db():
    if DB_CONN is not None:
        DB_CONN.close()


def drop_table(name):
    drop_str = "DROP TABLE " + name
    DB_CONN.execute(drop_str)
