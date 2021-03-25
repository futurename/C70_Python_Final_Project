import sqlite3

import loadStickersToDatabase

SQLITE_PATH = "data_source/database.db"

DB_CONN = sqlite3.connect(SQLITE_PATH, check_same_thread=False)


def get_db():
    return DB_CONN


def close_db():
    if DB_CONN is not None:
        DB_CONN.close()


def drop_table():
    sql_str = "DROP TABLE IF EXISTS " + loadStickersToDatabase.TICKERS_TABLE
    DB_CONN.execute(sql_str)


def create_table(header_cols):
    # Generate sql string for create table
    sql_str = "CREATE TABLE " + loadStickersToDatabase.TICKERS_TABLE
    sql_str += " (Id INTEGER PRIMARY KEY AUTOINCREMENT,"
    DB_CONN.execute(sql_str + header_cols + ")")
    print(">>>> table created <<<<")


def insert_row(row_str):
    cur = DB_CONN.cursor()
    cur.execute(row_str)
    DB_CONN.commit()


def get_symbols(fromTicker="", number=20):
    fromId = 1
    if not fromTicker == "":
        sql_str = "SELECT Id FROM " + loadStickersToDatabase.TICKERS_TABLE + " WHERE Symbol='" + fromTicker + "'"
        cursor = DB_CONN.cursor()
        cursor.execute(sql_str)
        records = cursor.fetchall()
        fromId = records[0][0] + 1
    toId = fromId + number - 1

    sql_str = "SELECT * FROM " + loadStickersToDatabase.TICKERS_TABLE + " WHERE Id BETWEEN " + str(fromId) + " AND " + str(toId)
    cursor = DB_CONN.cursor()
    cursor.execute(sql_str)
    return cursor.fetchall()
