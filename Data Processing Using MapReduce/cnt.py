from pymongo import MongoClient
from pyspark import SparkContext


def main():
    sc = SparkContext("local", "word count")
    count_keywords = ["storm", "winter", "canada", "hot", "cold", "flu", "snow", "indoor", "safety", "rain", "ice"]
    client = MongoClient(
        "mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_processed = client.ProcessedDb
    db_reuters = client.reuter_data
    data_reuter=db_reuters.reuter
    data_search = db_processed.search_tweets
    data_stream=db_processed.stream_tweets

    tweetlist_search = data_search.find()
    tweetlist_stream=data_stream.find()
    reuter=data_reuter.find()
    
    row=[]
    for tweet in tweetlist_search:
        value=tweet['Content']
        if 'Content - Original Tweet' in tweet:
            value=value+tweet['Content - Original Tweet']
        for val in value.split(' '):
            row.append(val)

    for tweet in tweetlist_search:
        value=tweet['Content']
        original_value=tweet['Content_OT']
        for val,val2 in zip(value.split(' '),original_value.split(' ')):
            row.append(val)
            row.append(val2)
         
    for content in reuter:
        value=content['body']
        for val in value.split(' '):
            row.append(val)
    words=[]
    all_lower=[]
    list(row)
    filtered=filter(lambda x: x.lower() in count_keywords, row)
    words.extend(list(filtered))
    for wrd in words:
        all_lower.append(wrd.lower())
    words_rdd = sc.parallelize(all_lower)

    counts = words_rdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1], False)
    for word, count in counts.toLocalIterator():
        print(u"{} --> {}".format(word, count))

if __name__ == "__main__":
    main()