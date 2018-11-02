import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time

app = dash.Dash('stock-advisor')
server = app.server

app.scripts.config.serve_locally = False
#dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

df = pd.read_csv('stock-ticker.csv')

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

app.layout = html.Div([
    html.Div([
        html.H2('Finance Explorer',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                style={
                    'height': '100px',
                    'float': 'right'
                },
        ),
    ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df.Stock.unique(), df.Stock.unique())],
        value=['YHOO', 'GOOGL'],
        multi=True
    ),
#    dcc.Graph(id='test-graph'),
    html.Div(id='stock-graphs'),
    html.H2('Bottom',
            style={'display': 'inline',
                   'float': 'left',
                   'font-size': '2.65em',
                   'margin-left': '7px',
                   'font-weight': 'bolder',
                   'font-family': 'Product Sans',
                   'color': "rgba(117, 117, 117, 0.95)",
                   'margin-top': '20px',
                   'margin-bottom': '0'
                   })
], className="container")

'''@app.callback(
    dash.dependencies.Output('test-graph','figure'),
    [dash.dependencies.Input('stock-ticker-input','value')])
def update_test_graph(tickers):
    ticker = 'YHOO'
    dff = df[df['Stock'] == ticker]
    candlestick = {
        'x': dff['Date'],
        'open': dff['Open'],
        'high': dff['High'],
        'low': dff['Low'],
        'close': dff['Close'],
        'type': 'candlestick',
        'name': ticker,
        'legendgroup': ticker,
        'increasing': {'line': {'color': colorscale[0]}},
        'decreasing': {'line': {'color': colorscale[1]}}
    }
    return {
        'data': [candlestick],
        'layout': {
            'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
            'legend': {'x': 0}
        }
    }'''

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

            dff = df[df['Stock'] == ticker]

            candlestick = {
                'x': dff['Date'],
                'open': dff['Open'],
                'high': dff['High'],
                'low': dff['Low'],
                'close': dff['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(dff.Close)
            bollinger_traces = [{
                'x': dff['Date'], 'y': y,
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
    print(len(graphs))
    return graphs


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
