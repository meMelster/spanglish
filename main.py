from labeled_tweets import labeled_tweets_tsv_to_list
from preprocessing import preprocess
from preprocessing import cleanse_tweet_words
from sentiment_analysis import get_words_in_tweets
from sentiment_analysis import get_word_features
import nltk.classify


raw_labeled_tweets = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
tweets = []
for (tweet, sentiment) in raw_labeled_tweets:
	tweet_words = preprocess(tweet)
	words_filtered = cleanse_tweet_words(tweet_words)
	tweets.append((words_filtered, sentiment))
	
	
#make same list for test_tweets
#raw_labeled_test_tweets = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled__test_tweets.tsv')
#test_tweets = []
#for (tweet, sentiment) in raw_labeled_test_tweets:
	#tweet_words = preprocess(tweet)
	#words_filtered = cleanse_tweet_words(tweet_words)
	#test_tweets.append((words_filtered, sentiment))



#list of word features to be extracted from the tweets
word_features = get_word_features(get_words_in_tweets(tweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


training_set = nltk.classify.apply_features(extract_features, tweets)

print(training_set)


