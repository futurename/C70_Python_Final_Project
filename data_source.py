import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

import random


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
        width=1400,
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
    area_chart.update_layout(showlegend=False, width=1200, height=600)

    # line chart
    df = px.line(x=data.index, y=data['High'], width=1200, height=600, title='Line Chart')

    # scatter chart
    sc = px.scatter(x=data.index, y=data['Low'], labels={'x': 'Time', 'y': 'High'}, width=1200, height=600, title='Scatter Chart')

    # two lines
    high_series = data['High']
    low_series = data['Low']
    low_high_lines = px.line(df, x=data.index, y=[high_series, low_series], width=1200, height=600, title="Combined Lines Chart")
    low_high_lines.data[0].name = 'High Price'
    low_high_lines.data[1].name = 'Low Price'

    return [candles.to_html(), area_chart.to_html(), df.to_html(), sc.to_html(), low_high_lines.to_html()]


def get_comp_disc_dict(df):
    result = {}
    for country in df['Country']:
        if country in result:
            result[country] += 1
        else:
            result[country] = 1
    return result


def render_company_distribution():
    df = pd.read_csv('data_source/safe_data.csv')
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
        title="Bubble Map"
    )

    world_dis_color_animation = px.choropleth(df,
                                              locations="Country",
                                              locationmode="country names",
                                              color="Last_Sale",
                                              animation_frame="IPO_Year",
                                              title="IPO Year Change Demo (Animation)",
                                              color_continuous_scale=px.colors.sequential.PuRd,
                                              height=900,
                                              width=1600,
                                              )

    world_dis_color_animation.update_layout(
        updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None]), {
            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                              "mode": "immediate",
                              "transition": {"duration": 0}}],
            "label": "Pause",
            "method": "animate"
        }])])

    # world_dis_bar_animation = px.bar(df,
    #                                  x="Symbol",
    #                                  y="Last_Sale",
    #                                  animation_frame="IPO_Year",
    #                                  title="Bar Chart (Animation)",
    #                                  animation_group='Country',
    #                                  range_y=[0, 4000000000],
    #                                  height=900,
    #                                  width=1600,
    #                                  )
    #
    # world_dis_bar_animation.update_layout(
    #     updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None]), {
    #         "args": [[None], {"frame": {"duration": 0, "redraw": False},
    #                           "mode": "immediate",
    #                           "transition": {"duration": 0}}],
    #         "label": "Pause",
    #         "method": "animate"
    #     }])])

    return [world_dis_color.to_html(), world_dis_scatter.to_html(), world_dis_color_animation.to_html(),]


def clean_data():
    df = pd.read_csv('data_source/nasdaq.csv')
    for index, row in df.iterrows():
        if pd.isna(row['IPO_Year']):
            rand = random.randint(1992, 2021)
            df._set_value(index, 'IPO_Year', rand)
    df.sort_values(by=['IPO_Year'], inplace=True)
    df.to_csv('data_source/safe_data.csv', sep=',', mode='w')
