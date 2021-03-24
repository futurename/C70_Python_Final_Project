from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import database
import json

app = Flask(__name__, template_folder="flask_template")


@app.route("/")
def home():
    database.get_db()
    records = database.get_symbols()
    print(type(records))
    return render_template("home.html", records=records)


@app.route("/logout")
def logout():
    session.pop("user", None)


if __name__ == "__main__":
    app.run(debug=True)
