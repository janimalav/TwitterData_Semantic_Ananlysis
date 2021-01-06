import tweepy   
from pymongo import MongoClient
import stream_listner as streamListener
import sys

def main():
    consumer_key = 'aeKdmwjd0O5x9xJA8dm5fYgBI'
    consumer_secret = 'C9Pscj881gtqUEitBrvxTFaYIEHJXQ5ohf1PCZkddxhYmKqDmm'
    access_token = '1509923156-J5N3ZYwkMF3SkyADj2dohUCDbIHuOHG2hQb9l66'
    access_token_secret = '4KWd9pJTU5al0Dosn1GBsAN9NWHrYWiRvmUumSR6lKp3y'
    
    client = MongoClient("mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/raw_db?retryWrites=true&w=majority")
    db = client.raw_db
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    search_words = ['Storm OR Winter OR Canada OR Temperature OR Flu OR Snow OR Indoor OR Safety']
    stream_words=['Storm','Winter','Canada','Temperature','Flu','Snow','Indoor','Safety']
    tweets = tweepy.Cursor(api.search, q=search_words).items(2000)

    for index,tweet in enumerate(tweets, start=1):
        
        if hasattr(tweet, 'retweeted_status'):
            row = to_row(tweet, "RETWEET")
            db.search_tweets.insert_one(row).inserted_id
                
            print(row)

        elif hasattr(tweet, 'quoted_status'):
            row = to_row(tweet, "QUOTED_TWEET")           
            db.search_tweets.insert_one(row).inserted_id
            
            print(row)


        elif hasattr(tweet, 'truncated'):
            row = to_row(tweet, "EXTENDED_TWEET")                
            db.search_tweets.insert_one(row).inserted_id

            print(row)

        else:
            row = to_row(tweet, "TWEET")
            db.search_tweets.insert_one(row).inserted_id
            print(row)

    twitterStreamListener = streamListener.TwitterStreamListener()
    twitterStream = tweepy.Stream(auth, twitterStreamListener)
    twitterStream.filter(track=stream_words)

def to_row(tweet, type):
        row = {}

        row['Timestamp'] = tweet.created_at
        row['ID'] = tweet.id
        row['Content'] = to_text(tweet.text)
        row['Username'] = to_text(tweet.user.name)
        row['User ScreenName'] = to_text(tweet.user.screen_name)
        row['User Location'] = to_text(tweet.user.location)

        row['Truncated'] = tweet.truncated if hasattr(tweet, 'Truncated') else ''
        row['Extended Tweet'] = to_text(tweet.extended_tweet.full_text) if hasattr(tweet, 'Truncated') else ''

        if type == 'RETWEET':
            row['Timestamp - Original Tweet'] = tweet.retweeted_status.created_at
            row['ID - Original Tweet'] = tweet.retweeted_status.id
            row['Content - Original Tweet'] = to_text(tweet.retweeted_status.text)
            row['Username - Original Tweet'] = to_text(tweet.retweeted_status.user.name)
            row['User ScreenName - Original Tweet'] = to_text(tweet.retweeted_status.user.screen_name)
            row['User Location - Original Tweet'] = to_text(tweet.retweeted_status.user.location)

        if type == 'QUOTED_TWEET':
            row['Timestamp - Original Tweet'] = tweet.quoted_status.created_at
            row['ID - Original Tweet'] = tweet.quoted_status.id
            row['Content - Original Tweet'] = to_text(tweet.quoted_status.text)
            row['Username - Original Tweet'] = to_text(tweet.quoted_status.user.name)
            row['User ScreenName - Original Tweet'] = to_text(tweet.quoted_status.user.screen_name)
            row['User Location - Original Tweet'] = to_text(tweet.quoted_status.user.location)
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

if __name__ == "__main__":
    main()
