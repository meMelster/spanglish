# spanglish


get_tweets.py
Uses twitter Streaming API to retrieve tweets from the US & Mexico

spanglish_tweets.py <file_created_by_get_tweets.json>
Filters through all tweets streamed in the in get_tweets.py and writes them to spanglish_tweets.txt 
While processing words that appear in both the English language dictionary and the Spanish language dictionary are added to the exclusion_list.txt


Then manually label a portion of these tweets for sentiment (positive, or negative) delimited by tabs for training
The unlabeled portion will be used for testing


main.py
calls label_tweets.py
takes a tab delimited file of tweet sentiment and stores it in a list of tuples
apply feature extraction, train classifier, and test
