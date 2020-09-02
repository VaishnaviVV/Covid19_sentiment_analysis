import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import pandas as pd
import re

analyzer = SentimentIntensityAnalyzer()

ckey="4GPV3M8dXW5U8zqkdyPXf91wt"
csecret="rUzto3l6WlnejAB7YjNgwJdLmNyvLvpmCWah1M5trxvtRW8K6F"
atoken="1264572913451102208-5yR98kQDUoaP6LRixvYrApS92WKwvj"
asecret="KQeshxg2BcFX9xQZ2Wy2cEl19iELVOneVljHgYgP9AdmO"


conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix TEXT, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))


create_table()



class listener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            # print(data)
            tweet = unidecode(data['text'])
            time_ms = data['created_at']
            time_ms=time_ms.replace('+0000 2020','')
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",(time_ms, tweet, sentiment))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return(True)
    def on_error(self, status):
        print(status)


while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["covid19","#covid19","corona","coronavirus","lockdown"])
    except Exception as e:
        print(str(e))
        time.sleep(5)
