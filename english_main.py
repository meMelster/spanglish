from labeled_tweets import labeled_tweets_tsv_to_list
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from sentiment_analysis import extract_features
import english_preprocessing as preprocess
from pprint import pprint
import nltk
import regex
import pickle
from nltk import precision
from nltk import recall
from nltk import f_measure
import collections


raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
used_raw_tweets = raw_labeled_tweets[:800]

#hand labeled tweets
neg_tweets = []
pos_tweets = []
for tweet in used_raw_tweets:
	if 'pos' in tweet[1]:
		pos_tweets.append(tweet)
	else:
		neg_tweets.append(tweet)
print(len(pos_tweets))
print(len(neg_tweets))

print('Counts')
print('Positive: ' + str(pos) + '  Negative: ' + str(neg))
#pprint(used_raw_tweets)
print()


tokenized_pos_tweets = []
tokenized_neg_tweets = []
#Case 1: English Lexical Experiment
#positive
print("CASE 1: ENGLISH")
print('Positive')
for (tweet, sentiment) in pos_tweets:
	#print(tweet)
	tweet_words = regex.tokenize(tweet)
	cleansed_words = preprocess.cleanse(tweet_words)
	tokenized_pos_tweets.append((cleansed_words, sentiment))
scored_pos_tweets = build_features(tokenized_pos_tweets)
print()
#pprint(scored_pos_tweets)
	

print()
#negative
print("Negative")
for (tweet, sentiment) in neg_tweets:
	#print(tweet)
	tweet_words = regex.tokenize(tweet)
	cleansed_words = preprocess.cleanse(tweet_words)
	tokenized_neg_tweets.append((cleansed_words, sentiment))
#pprint(tokenized_neg_tweets)
#list of word features to be extracted from the tweets
scored_neg_tweets = build_features(tokenized_neg_tweets)
print()
#pprint(scored_neg_tweets)

neg_tweets_cutoff = int(len(scored_neg_tweets)*(3/4))
pos_tweets_cutoff = int(len(scored_pos_tweets)*(3/4))
print('cutoffs')
print(neg_tweets_cutoff)
print(pos_tweets_cutoff)

print('Training')
print('Positive: ' +  str(pos_tweets_cutoff))
print('Negative: ' + str(neg_tweets_cutoff))

print('Test')
print('Positive: ' +  str(len(scored_pos_tweets) - pos_tweets_cutoff))
print('Negative: ' + str(len(scored_neg_tweets) - neg_tweets_cutoff))


#create training set
training_features = scored_neg_tweets[:neg_tweets_cutoff] + scored_pos_tweets[:pos_tweets_cutoff]
training_set = build_feature_set(training_features)
print()
#pprint(training_set)

#create test set
test_features = scored_neg_tweets[neg_tweets_cutoff:] + scored_pos_tweets[pos_tweets_cutoff:]
test_set = build_feature_set(test_features)
print()
#pprint(test_set)


#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

#classifier_f = open("english_naivebayes.pickle", "rb")
#classifier = pickle.load(classifier_f)
#classifier.close()

print(classifier.show_most_informative_features(32))
print(nltk.classify.accuracy(classifier, test_set))

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
observed = []

print('tweet features dictionary')
for i, (tweet_features, sentiment) in enumerate(test_set):
	#print(tweet_features)
	refsets[sentiment].add(i)
	observed = classifier.classify(tweet_features)
	testsets[observed].add(i)
	
	
print()	
print('Positive')
print('precision ' + str(precision(refsets['positive'], testsets['positive'])))
print('recall ' + str(recall(refsets['positive'], testsets['positive'])))
print('f-score ' + str(f_measure(refsets['positive'], testsets['positive'])))
print()

print('Negative')
print('precision ' + str(precision(refsets['negative'], testsets['negative'])))
print('recall ' + str(recall(refsets['negative'], testsets['negative'])))
print('f-score ' + str(f_measure(refsets['negative'], testsets['negative'])))


f_score = (f_measure(refsets['positive'], testsets['positive']) + f_measure(refsets['negative'], testsets['negative']))/2
print('Overall F-Score: ')
print(f_score)
print()
recall = (recall(refsets['positive'], testsets['positive']) + recall(refsets['negative'], testsets['negative']))/2
print('Overall Recall: ')
print(recall)
print()
precision = (precision(refsets['positive'], testsets['positive']) + precision(refsets['negative'], testsets['negative']))/2
print('Overall Precision: ')
print(precision)

print()

gold = (['positive'] * len(refsets['positive'])) + (['negative'] * len(refsets['negative']))
derived = (['positive'] * len(testsets['positive'])) + (['negative'] * len(testsets['negative']))
print('gold')
print('Positive: ')
print(len(refsets['positive']))
print('Negative: ')
print(len(refsets['negative']))
print(gold)
print()
print('derived')
print('Positive: ')
print(len(testsets['positive']))
print('Negative: ')
print(len(testsets['negative']))
print(derived)
print()

cm = nltk.ConfusionMatrix(gold, derived)
print(cm.pretty_format(sort_by_count=True, show_percents=False, truncate=9))
print()
print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))

#Save classifier bc this shit takes forever yo
save_classifier = open("english_naivebayes.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()


