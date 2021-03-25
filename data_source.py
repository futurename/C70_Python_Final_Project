import pandas as pd
import plotly
import numpy as np
import json
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from plotly import subplots
from pandas import DataFrame


def create_diff_graphs(symbol):
    data = yf.download(tickers=symbol, period='1d', interval='1m')

    # declare figure
    candles = go.Figure()

    # Candlestick
    candles.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'], name='market data'))
    # Add titles
    candles.update_layout(
        title=symbol + ' live share price',
        yaxis_title='Stock Price (USD per Shares)')
    # X-Axes
    candles.update_xaxes(
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
    candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                                                 open=data['Open'],
                                                 high=data['High'],
                                                 low=data['Low'],
                                                 close=data['Close'])])
    candlestick.update_layout(xaxis_rangeslider_visible=False, title=symbol + ' SHARE PRICE')
    candlestick.update_xaxes(title_text='Date')
    candlestick.update_yaxes(title_text=symbol + ' Close Price', tickprefix='$')

    # area chart
    area_chart = px.area(data, title=symbol + ' TRADED VOLUMES')
    area_chart.update_xaxes(title_text='Date')
    area_chart.update_yaxes(title_text='Trading Volumes')
    area_chart.update_layout(showlegend=False)

    # line chart
    df = px.line(x=data.index, y=data['High'])

    # scatter chart
    sc = px.scatter(x=data.index, y=data['Low'], labels={'x': 'Time', 'y': 'High'})

    # two lines
    high_series = data['High']
    low_series = data['Low']
    low_high_lines = px.line(df,x=data.index, y=[high_series, low_series])

    return [candles.to_html(), area_chart.to_html(), df.to_html(), sc.to_html(), low_high_lines.to_html()]
