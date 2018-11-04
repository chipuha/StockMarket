import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time

from Models.sma import sma

app = dash.Dash('stock-advisor')
server = app.server

app.scripts.config.serve_locally = False
#dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

#find list of tickers (should be under Data/DowJonesTickers.txt
filename="Data/DowJonesTickers.txt"
print('getting tickers from '+filename)
file=open(filename,"r")
tickerList = []
for ticker in file:
    tickerList.append(ticker.strip('\n'))

def bbands(price, window_size=10, num_of_std=3):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

app.layout = html.Div([
    html.Div([
        html.H2('Stock Advisor',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(107, 107, 107, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
            ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(tickerList, tickerList)],
        value=['AAPL'],
        multi=True
    ),
    html.Div(id='stock-graphs'), #view stock prices
    html.Div([ #view SMA for the selected stock
        dcc.Graph(id='sma-graph'),
        dcc.Slider(
            id='sma-slider-short',
            min=2,
            max=50,
            value=2,
            marks={x: x for x in range(2,50,4)}
        ),
        dcc.Slider(
            id='sma-slider-long',
            min=10,
            max=200,
            value=10,
            marks={x: x for x in range(10,200,10)}
        )
    ]),
    html.Div(id='sma')
], className="container")


#functionallity for plotting stock price plots
@app.callback(
    dash.dependencies.Output('stock-graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(tickers):
    graphs = []

    if not tickers:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={'marginTop': 20, 'marginBottom': 20}
        ))
    else:
        for i, ticker in enumerate(tickers):
            print('ticker: ',ticker)
            df = pd.read_csv('Data/CSVs/'+ticker+'.csv')

            candlestick = {
                'x': df['Date'],
                'open': df['Open'],
                'high': df['High'],
                'low': df['Low'],
                'close': df['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(df.Close)
            bollinger_traces = [{
                'x': df['Date'], 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker, #was ticker
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))
    return graphs

#functionality for SMA model
@app.callback(
        dash.dependencies.Output('sma-graph','figure'),
        [dash.dependencies.Input('stock-ticker-input','value'),
         dash.dependencies.Input('sma-slider-short','value'),
         dash.dependencies.Input('sma-slider-long','value')])
def sma_model(tickers,short,long):
    print('short:',short,'long:',long)
    for ticker in tickers:
        #import needed data
        df = pd.read_csv('Data/CSVs/'+ticker+'.csv')
        #create sma model
        sma1 = sma(ticker,df)
        sma1.createSMA(short,long)
        #extract dataframe to be plotted ('short_mavg' and 'long_mavg' columns)
        df_sma = sma1.signals
        
        #convert data into figure plot
        short_mavg = [{
                'x': df['Date'], 'y': sma1.signals['short_mavg'],
                'type': 'scatter', 'mode':'lines',
                'name': 'Short Moving Ave',
                'legendgroup': 'Short Moving Ave',
                }]
        long_mavg = [{
                'x': df['Date'], 'y': sma1.signals['long_mavg'],
                'type': 'scatter', 'mode':'lines',
                'name': 'Long Moving Ave',
                'legendgroup': 'Long Moving Ave',
                }]
        close = [{
                'x': df['Date'], 'y': df['Close'],
                'type': 'scatter', 'mode':'lines',
                'name': 'Close',
                'legendgroup': 'Close',
                }]
    return {
        'data': short_mavg+long_mavg+close,
        'layout': {
            'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0}
        }}


#Extra styling stuff
external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    app.run_server(debug=True)