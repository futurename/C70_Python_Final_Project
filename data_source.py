import pandas as pd
import plotly as py
import numpy as np
import json
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from plotly import subplots
from pandas import DataFrame
import database


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
        width=1600,
        height=800,
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
    low_high_lines = px.line(df, x=data.index, y=[high_series, low_series])

    return [candles.to_html(), area_chart.to_html(), df.to_html(), sc.to_html(), low_high_lines.to_html()]


def get_comp_disc_dict(df):
    result = {}
    for country in df['Country']:
        if country in result:
            result[country] += 1
        else:
            result[country] = 1

    return result


def get_comp_by_ipo_year(df):
    result = []
    for item in df:



def render_company_distribution():
    df = pd.read_csv('data_source/nasdaq.csv')
    comp_dis = get_comp_disc_dict(df)

    country_names = list(comp_dis.keys())
    num_of_comp = list(comp_dis.values())

    world_dis_color = go.Figure(data=go.Choropleth(
        locations=country_names,
        locationmode='country names',
        z=num_of_comp,
        colorscale='Blues',
        autocolorscale=True,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Number Of Companies',
    ))

    world_dis_color.update_layout(
        width=1600,
        height=900,
        title_text='Company Distribution',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    world_dis_scatter = px.scatter_geo(
        (country_names, num_of_comp),
        locations=country_names,
        size=num_of_comp,
        locationmode='country names',
        size_max=200,
        width=1600,
        height=900,
    )

    comp_by_ipo_year = get_comp_by_ipo_year(df)
    world_dis_scatter_animation = px.scatter_geo(
        (country_names, num_of_comp),
        locations=country_names,
        size=num_of_comp,
        locationmode='country names',
        size_max=200,
        width=1600,
        height=900,
    )

    return [world_dis_color.to_html(), world_dis_scatter.to_html(), world_dis_scatter_animation.to_html()]
