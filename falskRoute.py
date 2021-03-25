from flask import Flask, redirect, url_for, render_template, request
from datetime import timedelta
import json
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

from loadStickersToDatabase import get_header
import database

app = Flask(__name__, template_folder="flask_template")


@app.route("/")
def home():
    database.get_db()
    records = database.get_symbols()
    header = get_header()
    return render_template("home.html", header=header, records=records)


@app.route("/<symbol>")
def company(symbol):
    #draw_candle_ticks(symbol)
    return render_template("company.html", symbol=symbol)


def draw_candle_ticks(symbol):
    data = yf.download(tickers=symbol, period='1d', interval='1m')

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))
    # Add titles
    fig.update_layout(
        title='Uber live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Show
    fig.show()


if __name__ == "__main__":
    app.run(debug=True)
