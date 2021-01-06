import os
import re
from pymongo import MongoClient

def main():
    client = MongoClient("mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_raw = client.raw_db
    db_processed = client.ProcessedDb
    data_search = db_raw.search_tweets
    data_stream=db_raw.stream_tweets


    tweetlist_search= data_search.find()
    tweetlist_stream= data_stream.find()

    for row in tweetlist_search:
        row['Content'] = process(row['Content'])
        row['Username'] = process(row['Username'])
        row['User ScreenName'] = process(row['User ScreenName'])
        row['User Location'] = process(row['User Location'])
        if "Content - Original Tweet" in row:
            row['Content - Original Tweet'] = process(row['Content - Original Tweet'])
        if "Username - Original Tweet" in row:
            row['Username - Original Tweet'] = process(row['Username - Original Tweet'])
        if "User ScreenName - Original Tweet" in row:
            row['User ScreenName - Original Tweet'] = process(row['User ScreenName - Original Tweet'])
        if "User Location - Original Tweet" in row:
            row['User Location - Original Tweet'] = process(row['User Location - Original Tweet'])
        
        db_processed.search_tweets.insert_one(row).inserted_id

        print("Tweet:")
        print(row)
    
    for row in tweetlist_stream:
        row['Content'] = process(row['Content'])
        row['Username'] = process(row['Username'])
        row['User ScreenName'] = process(row['User ScreenName'])
        row['User Location'] = process(row['User Location'])
        if "'Content_OT'" in row:
            row['Content_OT'] = process(row['Content_OT'])
        if "Username_OT" in row:
            row['Username_OT'] = process(row['Username_OT'])
        if "User ScreenName_OT" in row:
            row['User ScreenName_OT'] = process(row['User ScreenName_OT'])
        if "user Location_OT" in row:
            row['user Location_OT'] = process(row['user Location_OT'])
        
        db_processed.stream_tweets.insert_one(row).inserted_id
        print("Tweet:")
        print(row)

def process(text):
    try:
        #to remove emoticons
        text=re.sub(r"\U0001F600-\U0001F64F",'',text)

        text=re.sub(r"[^\w\s]",'',text)            
        #remove URL
        text = re.sub(r"https\S+", '', text)

        text = re.sub(r"http\S+", '', text)
    except:
        pass
    return text

if __name__ == "__main__":
    main()