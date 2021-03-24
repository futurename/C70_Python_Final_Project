from csv import reader
import database

CSV_PATH = "data_source/nasdaq.csv"
STICKERS_TABLE = "Stickers"


def loadStickersToDb():
    with open(CSV_PATH, "r") as csv_f:
        csv_reader = reader(csv_f)
        header = next(csv_reader)

        # Drop table if exists
        if STICKERS_TABLE:
            database.drop_table(STICKERS_TABLE)

        # Generate sql string for create table
        insert_header_str = "CREATE TABLE " + STICKERS_TABLE
        header_cols = "("
        for i in range(len(header) - 1):
            header_cols += header[i] + ","
        header_cols += header[len(header) - 1] + ")"

        db = database.DB_CONN
        db.execute(insert_header_str + header_cols)

        # Insert data to the stickers table
        for row in csv_reader:
            row_str = "INSERT INTO " + STICKERS_TABLE
            row_str += header_cols + " VALUES("
            for i in range(len(row) - 1):
                row_str += "\"" + row[i] + "\","

            row_str += "\"" + row[len(row) - 1] + "\");"

            cur = db.cursor()
            cur.execute(row_str)
            db.commit()

    print("Import data ends")


if __name__ == '__main__':
    loadStickersToDb()
