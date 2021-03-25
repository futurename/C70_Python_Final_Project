from flask import Flask, redirect, url_for, render_template, request
from datetime import timedelta
import json

from loadStickersToDatabase import get_header
import database

app = Flask(__name__, template_folder="flask_template")


@app.route("/")
def home():
    database.get_db()
    records = database.get_symbols()
    header = get_header()
    return render_template("home.html", header=header, records=records)


if __name__ == "__main__":
    app.run(debug=True)
