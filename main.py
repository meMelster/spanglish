from labeled_tweets import labeled_tweets_tsv_to_list
from english_preprocessing import preprocess
#from spanish_preprocessing import sp_preprocess
from english_preprocessing import cleanse_tweet_words
#from spanish_preprocessing import sp_cleanse_tweet_words
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from pprint import pprint
import nltk


raw_labeled_tweets = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
#raw_labeled_train_tweets = raw_labeled_tweets[:10]
#print(raw_labeled_train_tweets)
#raw_labeled_test_tweets = raw_labeled_tweets[11:21]
#print(raw_labeled_test_tweets)
tweets = []
used_raw_tweets = raw_labeled_tweets[:501]

#Case 1: English Lexical Experiment
for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	tweet_words = preprocess(tweet)
	words_filtered = cleanse_tweet_words(tweet_words)
	tweets.append((words_filtered, sentiment))


#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
#pprint(scored_tweets)


#create training set
training_set, test_set = build_feature_set(scored_tweets[:250]), build_feature_set(scored_tweets[251:501])
#pprint(test_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))

#test_tweet = 'this class is pura mierda'
#print(classifier.classify(extract_features(test_tweet.split())))
