#Essential Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Dashboard Modules
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import datetime as dt
from io import BytesIO
from wordcloud import WordCloud
from collections import deque
import pybase64
import os
import json
import sqlite3
from unidecode import unidecode
import time
from application import app

##from apps import live_twitter_sentiment_streaming
#Twitter Modules
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import random
import plotly
from navbar import Navbar
navs=Navbar()

conn = sqlite3.connect('twitter.db')
c = conn.cursor()




# app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])




layout=dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Live Twitter Sentiment", className="card-title"),
                dcc.Graph(id="live-graph"),
                dcc.Interval(
                  id="graph-update",
                  interval=1*1000
                  )
            ]
        ),
    ],
)

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment ORDER BY unix DESC LIMIT 1000", conn)
    # df.sort_values('unix', inplace=True)
    df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
    df.dropna(inplace=True)
    X = df.unix.values[:]
    Y = df.sentiment_smoothed.values[:]
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(dict(xaxis={'range':[min(X),max(X)],'title':'Timestamp(ms)'},
                                                yaxis={'range':[min(Y),max(Y)],'title':'Compound Sentiment'}
                                                     )
                                                )
            }

# if __name__=="__main__":
#     application.run_server(debug=True)
