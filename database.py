import sqlite3

SQLITE_PATH = "data_source/database.db"

DB_CONN = sqlite3.connect(SQLITE_PATH)


def get_db():
    return DB_CONN


def close_db():
    if DB_CONN is not None:
        DB_CONN.close()


def drop_table(table):
    sql_str = "DROP TABLE IF EXISTS " + table
    DB_CONN.execute(sql_str)


def create_table(table, header_cols):
    # Generate sql string for create table
    sql_str = "CREATE TABLE " + table
    sql_str += " (Id INTEGER PRIMARY KEY AUTOINCREMENT,"
    DB_CONN.execute(sql_str + header_cols + ")")


def insert_row(row_str):
    cur = DB_CONN.cursor()
    cur.execute(row_str)
    DB_CONN.commit()

def get_symbols(fromTicker = "", number = 50):
    return True
