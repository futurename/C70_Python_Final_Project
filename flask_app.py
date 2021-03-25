from flask import Flask, redirect, render_template, request, url_for
from loadStickersToDatabase import get_header
import database
import data_source as my_data

app = Flask(__name__, template_folder="flask_template")


@app.route("/")
def home():
    database.get_db()
    records = database.get_symbols()
    header = get_header()
    return render_template("home.html", header=header, records=records)


@app.route("/company/<symbol>")
def company(symbol):
    result = my_data.create_diff_graphs(symbol)
    return render_template("company.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
