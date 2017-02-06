from labeled_tweets import labeled_tweets_tsv_to_list
import spanglish_preprocessing as preprocess
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from pprint import pprint
import nltk
import regex


raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
used_raw_tweets = raw_labeled_tweets[:500]

print('Counts')
print('Positive: ' + str(pos) + '  Negative: ' + str(neg))
pprint(used_raw_tweets)
print()



tweets = []
#Case 3: Spanglish Lexical Experiment
print("CASE 3: SPANGLISH")
for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	tweet_words = regex.tokenize(tweet)
	cleansed_words = preprocess.spanglish_cleanse(tweet_words)
	tweets.append((cleansed_words, sentiment))


print()
pprint(tweets)
#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
print()
pprint(scored_tweets)


#create training set
training_set = build_feature_set(scored_tweets[:250])
test_set = build_feature_set(scored_tweets[251:500])
print("Training Set")
pprint(training_set)
print("Test Set")
pprint(test_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))
