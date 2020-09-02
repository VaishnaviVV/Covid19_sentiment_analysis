import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

ckey="4GPV3M8dXW5U8zqkdyPXf91wt"
csecret="rUzto3l6WlnejAB7YjNgwJdLmNyvLvpmCWah1M5trxvtRW8K6F"
atoken="1264572913451102208-5yR98kQDUoaP6LRixvYrApS92WKwvj"
asecret="KQeshxg2BcFX9xQZ2Wy2cEl19iELVOneVljHgYgP9AdmO"


conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS discussion(id TEXT, tweet TEXT)")
        c.execute("CREATE INDEX fast_id ON discussion(id)")
        c.execute("CREATE INDEX fast_tweet ON discussion(tweet)")
        conn.commit()
    except Exception as e:
        print(str(e))


create_table()

tweet_ids=['@narendramodi',' @swamy39',' @AmitShah', '@rajnathsingh', '@smritiirani','@RahulGandhi', '@ShashiTharoor', '@PawarSpeaks',' @KapilSibal','@derekobrienmp','@myogiadityanath','@NitishKumar', '@MamataOfficial','@vijayrupanibjp','@OfficeofUT','@HardeepSPuri', '@nsitharaman','@CMOTamilNadu','@ashwinravi99', '@sachin_rt', '@imVkohli', '@harbhajan_singh', '@virendersehwag']

class listener(StreamListener):
    def on_data(self, data):
        try:
            auth = tweepy.OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            api = tweepy.API(auth)
            for id in tweet_ids:
                for tweet in tweepy.Cursor(api.user_timeline,screen_name=id,q="#covid19",tweet_mode="extended").items(20):
                    identity=tweet.user.name
                    print(identity)
                    print(tweet.full_text)
                    c.execute("INSERT INTO discussion(id, tweet) VALUES (?, ?)",(identity, tweet.full_text))
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
