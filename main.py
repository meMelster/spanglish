from labeled_tweets import labeled_tweets_tsv_to_list
from english_preprocessing import preprocess
from english_preprocessing import cleanse_tweet_words
from sentiment_analysis import build_features
from sentiment_analysis import build_training_set
from pprint import pprint
import nltk


raw_labeled_tweets = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
tweets = []

#Case 1: English Lexical Experiment
for (tweet, sentiment) in raw_labeled_tweets:
	tweet_words = preprocess(tweet)
	words_filtered = cleanse_tweet_words(tweet_words)
	tweets.append((words_filtered, sentiment))


#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
pprint(scored_tweets)


#create training set
training_set = build_training_set(scored_tweets)
pprint(training_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

test_tweet = 'this class is pura mierda'
print(classifier.classify(extract_features(test_tweet.split())))
