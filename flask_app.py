from flask import Flask, redirect, render_template, request, url_for
from loadStickersToDatabase import get_header
import database
import data_source as my_data

app = Flask(__name__, template_folder="flask_template")

START_INDEX = 1


@app.route("/")
def home():
    records = database.get_symbols()
    header = get_header()
    return render_template("home.html", header=header, records=records, index=START_INDEX)


@app.route("/company/<symbol>")
def company(symbol):
    result = my_data.create_diff_graphs(symbol)
    return render_template("company.html", result=result)


@app.route("/prev_page/<index>")
def prev_page(index):
    fromId = 0 if int(index) - database.PAGE_SYMBOLS <= 0 else int(index) - database.PAGE_SYMBOLS
    records = database.get_symbols(fromId)
    header = get_header()
    return render_template("home.html", header=header, records=records, index=fromId)


@app.route("/next_page/<index>")
def next_page(index):
    fromId = int(index) + database.PAGE_SYMBOLS
    records = database.get_symbols(fromId)
    header = get_header()
    return render_template("home.html", header=header, records=records, index=fromId)


@app.route("/search", methods=['POST'])
def search():
    search_data = request.form['search']
    print(search_data)
    records = database.search_symbols(search_data)
    header = get_header()
    return render_template("home.html", header=header, records=records, index=START_INDEX)


@app.route("/statistics")
def statistics():
    results = my_data.render_company_distribution()
    return render_template("statistics.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
