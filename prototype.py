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

#Twitter Modules
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import random
import plotly

external_stylesheets = [dbc.themes.YETI]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)




card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-1", className="card-title"),
                html.P("This card contains a table")
            ]
        ),
    ],
)
card2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-2", className="card-title"),
                html.P("This card contains a table")
            ]
        ),
    ],
    
)
card3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-3", className="card-title"),
                html.P("This card contains a graph")
            ]
        ),
    ],
)

card4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-4", className="card-title"),
                html.P("This card contains a graph")
            ]
        ),
    ],
)
card5 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-5",className="card-title"),
                html.P("This card contains an image")
            ]
        ),
    ],
)
card6 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-6", className="card-title"),
                html.P("This card contains an image")
            ]
        ),
    ],
)
card7 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-7", className="card-title"),
                html.P("This card contains an image")
            ]
        ),
    ],
)

card8 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-8", className="card-title"),
                html.P("This card contains an image")
            ]
        ),
    ],
)

card9 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-9", className="card-title"),
                html.P("This card contains a graph")
            ]
        ),
    ],
)

card10 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Card-10", className="card-title"),
                html.P("This card contains an user input box")
            ]
        ),
    ],
)




app.layout= dbc.Jumbotron(
  [
    dbc.Container(
      [
          html.Div(children=[
            html.H1(children='Sentimental Analysis of Covid-19 Tweets from Indians')],
                   style={'textAlign':'center'}),
          html.Div([
              dbc.Row([
                  dbc.Col([card1]),dbc.Col([card2])
                  ]),
              dbc.Row([
                dbc.Col([card3])
                ]),
              dbc.Row([
                dbc.Col([card4])
                ]),
              dbc.Row([
                dbc.Col([card5]),dbc.Col([card6])
                ]),
              dbc.Row([
                dbc.Col([card7]),dbc.Col([card8])
                ]),
              dbc.Row([
                dbc.Col([card10])
                ]),
              dbc.Row([
                dbc.Col([card9])
                ]),
              ]),
        ],
      fluid=True,
      )
    ],
  fluid=True,
)
            
#-------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
