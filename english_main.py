from labeled_tweets import labeled_tweets_tsv_to_list
from english_preprocessing import preprocess
from english_preprocessing import cleanse_tweet_words
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from pprint import pprint
import nltk


raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
used_raw_tweets = raw_labeled_tweets[:10]

print('Counts')
print('Positive: ' + str(pos) + '  Negative: ' + str(neg))
#pprint(used_raw_tweets)
print()


tweets = []
#Case 1: English Lexical Experiment
print("CASE 1: ENGLISH")
for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	tweet_words = preprocess(tweet)
	words_filtered = cleanse_tweet_words(tweet_words)
	tweets.append((words_filtered, sentiment))

#print()
#pprint(tweets)
#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
#print()
pprint(scored_tweets)


#create training set
training_set = build_feature_set(scored_tweets[:5])
test_set = build_feature_set(scored_tweets[6:10])
#print("Training Set")
#pprint(training_set)
#print("Test Set")
#pprint(test_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))

