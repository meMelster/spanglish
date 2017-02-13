from labeled_tweets import labeled_tweets_tsv_to_list
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
import english_preprocessing as preprocess
from pprint import pprint
import nltk
import regex
import pickle


raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
used_raw_tweets = raw_labeled_tweets[:900]

print('Counts')
print('Positive: ' + str(pos) + '  Negative: ' + str(neg))
#pprint(used_raw_tweets)
print()


tweets = []
#Case 1: English Lexical Experiment
print("CASE 1: ENGLISH")
for (tweet, sentiment) in used_raw_tweets:
	#print(tweet)
	tweet_words = regex.tokenize(tweet)
	cleansed_words = preprocess.cleanse(tweet_words)
	tweets.append((cleansed_words, sentiment))

print()
pprint(tweets)
#list of word features to be extracted from the tweets
scored_tweets = build_features(tweets)
print()
pprint(scored_tweets)


#create training set
training_set = build_feature_set(scored_tweets[:450])
test_set = build_feature_set(scored_tweets[451:900])
print()
print("Training Set")
pprint(training_set)
print()
print("Test Set")
pprint(test_set)

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

#classifier_f = open("english_naivebayes.pickle", "rb")
#classifier = pickle.load(classifier_f)
#classifier.close()

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))

#Save classifier bc this shit takes forever yo
save_classifier = open("english_naivebayes.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()
