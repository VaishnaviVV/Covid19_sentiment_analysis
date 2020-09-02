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
#Twitter Modules
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import random
import plotly
from navbar import Navbar
navd=Navbar()
#Please change data_dir variable accordingly ma'am/sir
data_dir = 'C:\\Users\\Hi\\Desktop\\mydashapp\\dash-app-example\\apps'
data = []


url1 = 'https://drive.google.com/file/d/1oTe9DijHzaQvdHeBrMCIG2bWBa9lme1C/view?usp=sharing'
path1 = 'https://drive.google.com/uc?export=download&id='+url1.split('/')[-2]
url2 = 'https://drive.google.com/file/d/1oTe9DijHzaQvdHeBrMCIG2bWBa9lme1C/view?usp=sharing'
path2 = 'https://drive.google.com/uc?export=download&id='+url2.split('/')[-2]
url3 = 'https://drive.google.com/file/d/1oTe9DijHzaQvdHeBrMCIG2bWBa9lme1C/view?usp=sharing'
path3 = 'https://drive.google.com/uc?export=download&id='+url3.split('/')[-2]
url4 = 'https://drive.google.com/file/d/1oTe9DijHzaQvdHeBrMCIG2bWBa9lme1C/view?usp=sharing'
path4 = 'https://drive.google.com/uc?export=download&id='+url4.split('/')[-2]
url5 = 'https://drive.google.com/file/d/1oTe9DijHzaQvdHeBrMCIG2bWBa9lme1C/view?usp=sharing'
path5 = 'https://drive.google.com/uc?export=download&id='+url5.split('/')[-2]
data.append(pd.read_csv(path1,sep=',',error_bad_lines=False))
data.append(pd.read_csv(path2,sep=',',error_bad_lines=False))
data.append(pd.read_csv(path3,sep=',',error_bad_lines=False))
data.append(pd.read_csv(path4,sep=',',error_bad_lines=False))
data.append(pd.read_csv(path5,sep=',',error_bad_lines=False))
dataset=pd.concat(data)
for row in dataset.index:
  print(row) 


#cols=[1,2,3,4,13,20,21]
#dataset=dataset[dataset.columns[cols]]

#dataset=dataset[dataset['lang']=='en']
#dataset=dataset[dataset['country_code']=='IN']

dataset['Index'] = range(0, len(dataset))
dataset.set_index('Index',inplace=True)

#Cleaning the dataset1
import re
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords') #req only once to be executed #this package contains the list of irrelevant words

from nltk.corpus import stopwords #corpus(collection of text of same type) of reviews

stop_words = set(stopwords.words('english'))
stop_words.update(['#coronavirus', '#coronavirusoutbreak', '#coronavirusPandemic', '#covid19', '#covid_19', '#epitwitter', '#ihavecorona', 'amp', 'coronavirus', 'covid19'])

tweets = dataset['text']
tweets.head()

tweets=tweets.apply(lambda x:re.sub('[^a-zA-Z]',' ',str(x))) #keeping only letters
tweets.head()

tweets = tweets.apply(lambda x: re.sub(r"https\S+", "", str(x))) #removing URLs
tweets.head()

tweets = tweets.apply(lambda x: x.lower()) #converting to lowercase
tweets.head()

tweets = tweets.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
tweets.head()

words = [word for line in tweets for word in line.split()]
# words[0:10]

#Top 50 most frequent words in tweets

from collections import Counter

top50_word_count = Counter(words).most_common(50)
top50_word_count=pd.DataFrame(top50_word_count)
top50_word_count=top50_word_count.rename(columns = {0:'Word',1:'Frequency'})

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
sentiment_scores = tweets.apply(lambda x: sid.polarity_scores(x))
sentiment_scores = pd.DataFrame(list(sentiment_scores))
sentiment_scores.head()


sentiment_scores['Sentiment'] = sentiment_scores['compound'].apply(lambda x: 'Neutral' if (x > -0.05 and x<0.05) else ('Positive' if x >= 0.05 else 'Negative'))




Senti_Count = pd.DataFrame.from_dict(Counter(sentiment_scores['Sentiment']), orient = 'index').reset_index()
Senti_Count.head()
Senti_Count=Senti_Count.rename(columns={'index':'Sentiment',0:'Count'})
Senti_Count.head()
x=['Neutral','Positive','Negative']
y=[]
for i in range(0,3):
  if(Senti_Count['Sentiment'][i]==x[i]):
    y.append(Senti_Count['Count'][i])


# !pip install dash


# -------------------------------------------------------------------------------------
# Import the cleaned data (importing csv into pandas)
df = dataset


def generate_table(dataframe,max_rows=10):
    return dbc.Table.from_dataframe(dataframe.head(max_rows),bordered=True,dark=True,striped=True)

import datetime as dt
sentiments_time_series = pd.DataFrame()
sentiments_time_series['Time'] = dataset['created_at']
sentiments_time_series['Polarity'] = sentiment_scores['compound']
sentiments_time_series.index = pd.to_datetime(sentiments_time_series['Time'])
sentiments_time_series.head()

temp = sentiments_time_series
temp['Time'] = pd.to_datetime(temp['Time'])
temp.index = pd.to_datetime(temp['Time'])
temp.sort_index(inplace=True)
temp['Expanding'] = temp['Polarity'].expanding().mean()
temp['Rolling'] = temp['Polarity'].rolling('1h').mean()


sentimentdistribution = go.Figure([go.Bar(x=x, y=y,marker_color=['grey','green','red'])])
import plotly.tools as tls

sentimentfluctuation=tls.make_subplots(rows=1,cols=1,shared_xaxes=True)
sentimentfluctuation['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
tweetsentiment=go.Scatter(x=temp['Time'],y=temp['Polarity'],mode='markers',line=dict(color='green'),name='Tweet Sentiment')
rollingmean=go.Scatter(x=temp['Time'],y=temp['Rolling'],mode='lines',line=dict(color='red'),name='Rolling Mean')
expandingmean=go.Scatter(x=temp['Time'],y=temp['Expanding'],mode='lines',line=dict(color='blue'),name='Expanding Mean')
sentimentfluctuation.add_trace(tweetsentiment,1,1)
sentimentfluctuation.add_trace(rollingmean,1,1)
sentimentfluctuation.add_trace(expandingmean,1,1)


sentiment_tweets = pd.DataFrame()
sentiment_tweets['Tweet'] = tweets
sentiment_tweets['Sentiment'] = sentiment_scores['Sentiment']

positive_tweets = sentiment_tweets[sentiment_tweets['Sentiment'] == 'Positive']['Tweet']
negative_tweets= sentiment_tweets[sentiment_tweets['Sentiment'] == 'Negative']['Tweet']
neutral_tweets = sentiment_tweets[sentiment_tweets['Sentiment'] == 'Neutral']['Tweet']



def plot_wordcloud(data):
    wordgroups = [word for line in data for word in line.split()]
    wc = WordCloud(background_color='black', width=480, height=360).generate(' '.join(wordgroups))
    return wc.to_image()

@application.callback(Output('positive', 'src'), [Input('positive', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=positive_tweets).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(pybase64.b64encode(img.getvalue()).decode())

@application.callback(Output('negative', 'src'), [Input('negative', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=negative_tweets).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(pybase64.b64encode(img.getvalue()).decode())

@application.callback(Output('neutral', 'src'), [Input('neutral', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=neutral_tweets).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(pybase64.b64encode(img.getvalue()).decode())

@application.callback(Output('words', 'src'), [Input('words', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=tweets).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(pybase64.b64encode(img.getvalue()).decode())

cols=[2,3]
dframetemp=dataset[dataset.columns[cols]]

card0=Navbar()
card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Few Tweets from Indians during the CoVid-19", className="card-title"),
                generate_table(dframetemp,4)
            ]
        ),
    ],
)
card2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Top 10 Frequently Occuring Words", className="card-title"),
                generate_table(top50_word_count)
            ]
        ),
    ],

)
card3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Sentiment Distribution", className="card-title"),
                dcc.Graph(figure=sentimentdistribution)
            ]
        ),
    ],
)

card4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Sentiment Fluctuations Over Time", className="card-title"),
                dcc.Graph(figure=sentimentfluctuation)
            ]
        ),
    ],
)
card5 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Frequently Used Words", className="card-title"),
                html.Img(id='words')
            ]
        ),
    ],
)
card6 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Frequently Used Positive Words", className="card-title"),
                html.Img(id='positive')
            ]
        ),
    ],
)
card7 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Frequently Used Negative Words", className="card-title"),
                html.Img(id='negative')
            ]
        ),
    ],
)

card8 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Frequently Used Neutral Words", className="card-title"),
                html.Img(id='neutral')
            ]
        ),
    ],
)


analyser=SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(text):
    score = analyser.polarity_scores(text)
    lb = score['compound']
    if lb >= 0.05:
        return "Your sentiment is Positive"
    elif (lb > -0.05) and (lb < 0.05):
        return "Your sentiment is Neutral"
    else:
        return "Your sentiment is Negative"

card9=dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Analyse Your Sentiment", className="card-title"),
                dbc.Label("Type a sentence in the given input box:"),
                dbc.Input(id="input",placeholder="Your sentence goes here...",type="text"),
                html.Br(),
                html.P(id="output")
            ]
        ),
    ],
)

@application.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
    return sentiment_analyzer_scores(value)


#------------------------------------------------
#Updating vizualizations for live sentiments
tab2_content=dbc.Jumbotron(
  [
    dbc.Container(
      [
          html.Div(children=[
            html.H1(children='Sentimental Analysis of Covid-19 Tweets from Indians')],
                   style={'textAlign':'center'}),
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
                dbc.Col([card9])
                ]),
              ]),
        ],
      fluid=True
      )
##    ],
##  fluid=True,
##)


layout=dbc.Jumbotron([
  html.Div(children=[
    dbc.Row([
      dbc.Col([tab2_content])
      ])
    ])
  ])

#-------------------------------------------------------------------------------------
