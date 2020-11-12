import tweepy
import sys
import json
from pymongo import MongoClient


class TwitterStreamListener(tweepy.streaming.StreamListener):
    tweetCounter = 0

    def on_data(self, data):
        client = MongoClient("mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/raw_db?retryWrites=true&w=majority")
        db = client.raw_db
   
        print(data)

        tweet = json.loads(data)

        row = self.to_row(tweet, 'TWEET')
        db.stream_tweets.insert_one(row).inserted_id

        TwitterStreamListener.tweetCounter += 1
        if TwitterStreamListener.tweetCounter == 2000:
            sys.exit()
        else:
            pass

    
    def on_error(self, error):
        print(error)

    
    def to_row(self,tweet,tweet_type):
            row = {}

            row['Timestamp'] = tweet['created_at']
            row['ID'] = tweet['id']
            row['Content'] = to_text(tweet['text'])
            row['Username'] = to_text(tweet['user']['name'])
            row['User ScreenName'] = to_text(tweet['user']['screen_name'])
            row['User Location'] = to_text(tweet['user']['location'])
            
            if tweet['retweeted']:
                row['Timestamp_OT'] = tweet['retweeted_status']['created_at']
                row['ID_OT'] = tweet['retweeted_status']['id']
                row['Content_OT'] = to_text(tweet['retweeted_status']['text'])
                row['Username_OT'] = to_text(tweet['retweeted_status']['user']['name'])
                row['User ScreenName_OT'] = to_text(tweet['retweeted_status']['user']['screen_name'])
                row['user Location_OT'] = to_text(tweet['retweeted_status']['user']['location'])
            else:
                row['Timestamp_OT'] = ''
                row['ID_OT'] = ''
                row['Content_OT'] = ''
                row['Username_OT'] = ''
                row['User ScreenName_OT'] = ''
                row['user Location_OT'] = ''
            return row
def to_text(text):
    try:
        text = re.sub(r"http\S+", '', text)

        text = re.sub(r'\\u[A-Za-z0-9]{4}', '', text)

        text = re.sub(r'&amp;', '&', text)

        text = re.sub(r"[^a-zA-Z0-9@',.:\$& ]+", '', text)

        text = re.sub(r'\\n', ' ', text)

        text = re.sub(r'\s+', ' ',text)
    except:
        pass
    return text