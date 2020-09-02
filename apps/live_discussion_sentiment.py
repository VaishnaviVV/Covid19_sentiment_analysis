
#Essential Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Dashboard Modules
import dash
import dash_table
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

# app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
layout=dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Expert Insights", className="card-title"),
                html.Div(html.Div(id="recent-tweets-table")),
                 dcc.Interval(
                 id='recent-table-update',
                 interval=1*1000
                 )
            ]
        ),
    ],
)
def generate_table(dataframe,max_rows=10):
    return dbc.Table.from_dataframe(dataframe.tail(10),bordered=True,striped=True)


@app.callback(Output('recent-tweets-table', 'children'),
              [Input('recent-table-update', 'n_intervals')])
def update_recent_tweets(input_data):
    conn = sqlite3.connect('twitter.db',check_same_thread=False)
    df = pd.read_sql("SELECT * FROM discussion", conn)
    return generate_table(df,max_rows=10)
# 
# if __name__=="__main__":
#     app.run_server(debug=False)
