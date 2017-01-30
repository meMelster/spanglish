from labeled_tweets import labeled_tweets_tsv_to_list
from english_preprocessing import preprocess

from english_preprocessing import cleanse_tweet_words
from spanish_preprocessing import sp_cleanse_tweet_words
from spanglish_preprocessing import spanglish_cleanse_tweet_words

from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from pprint import pprint
import nltk


raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
used_raw_tweets = raw_labeled_tweets[:41]
print('Counts')
print('Positive: ' + str(pos) + '  Negative: ' + str(neg))
#pprint(used_raw_tweets)



tweets = []
#Case 1: English Lexical Experiment
print("CASE 1: ENGLISH")
for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	tweet_words = preprocess(tweet)
	words_filtered = cleanse_tweet_words(tweet_words)
	tweets.append((words_filtered, sentiment))


#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
#pprint(scored_tweets)


#create training set
training_set, test_set = build_feature_set(scored_tweets[:5]), build_feature_set(scored_tweets[6:41])
pprint(test_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))





#tweets = []
#Case 2: Spanish Lexical Experiment
#print("CASE 2: SPANISH")
#for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	#tweet_words = preprocess(tweet)
	#print(tweet_words)
	#words_filtered = sp_cleanse_tweet_words(tweet_words)
	#print(words_filtered)
	#tweets.append((words_filtered, sentiment))


#list of word features to be extracted from the tweets
#scored_tweets = build_features(tweets)
#pprint(scored_tweets)


#create training set
#training_set, test_set = build_feature_set(scored_tweets[:25]), build_feature_set(scored_tweets[26:51])
#pprint(test_set)

#train our classifier
#classifier = nltk.NaiveBayesClassifier.train(training_set)

#print(classifier.show_most_informative_features(32))
#print(nltk.classify.accuracy(classifier, test_set))




#tweets = []
#Case 3: Spanglish Lexical Experiment
#print("CASE 3: SPANGLISH")
#for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	#tweet_words = preprocess(tweet)
	#print(tweet_words)
	#words_filtered = spanglish_cleanse_tweet_words(tweet_words)
	#print(words_filtered)
	#tweets.append((words_filtered, sentiment))


#list of word features to be extracted from the tweets
#scored_tweets = build_features(tweets)
#pprint(scored_tweets)


#create training set
#training_set, test_set = build_feature_set(scored_tweets[:25]), build_feature_set(scored_tweets[26:51])
#pprint(test_set)

#train our classifier
#classifier = nltk.NaiveBayesClassifier.train(training_set)

#print(classifier.show_most_informative_features(32))
#print(nltk.classify.accuracy(classifier, test_set))
