from csv import reader
import database

CSV_PATH = "data_source/nasdaq.csv"
TICKERS_TABLE = "Tickers"


def loadStickersToDb():
    with open(CSV_PATH, "r") as csv_f:
        csv_reader = reader(csv_f)
        header = next(csv_reader)

        # Drop table if exists
        database.drop_table(TICKERS_TABLE)

        header_cols = ""
        for i in range(len(header) - 1):
            header_cols += header[i] + ","
        header_cols += header[len(header) - 1]

        database.create_table(TICKERS_TABLE, header_cols)

        # Insert data to the stickers table
        for row in csv_reader:
            row_str = "INSERT INTO " + TICKERS_TABLE + "("
            row_str += header_cols + ") VALUES("
            for i in range(len(row) - 1):
                row_str += "\"" + row[i] + "\","

            row_str += "\"" + row[len(row) - 1] + "\");"
            database.insert_row(row_str)

    print("Import data ends")


if __name__ == '__main__':
    loadStickersToDb()
