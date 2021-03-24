from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import database

app = Flask(__name__, template_folder="flask_template")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/logout")
def logout():
    session.pop("user", None)


if __name__ == "__main__":
    app.run(debug=True)
