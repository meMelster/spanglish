from labeled_tweets import labeled_tweets_tsv_to_list
import spanglish_preprocessing as preprocess
from sentiment_analysis import build_features
from sentiment_analysis import build_feature_set
from pprint import pprint
import pickle
import nltk
import regex

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import matthews_corrcoef

raw_labeled_tweets_f = open("raw_labeled_tweets_800.pickle", "rb")
raw_labeled_tweets = pickle.load(raw_labeled_tweets_f)
raw_labeled_tweets_f.close()

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

tokenized_pos_tweets = []
tokenized_neg_tweets = []
#Case 3: Spanglish Lexical Experiment
#positive
print("CASE 3: Spanglish")
#print('Positive')
count = 0
#for (tweet, sentiment) in pos_tweets:
	#print(tweet)
#	tweet_words = regex.tokenize(tweet)
#	cleansed_words = preprocess.spanglish_cleanse(tweet_words, count)
#	tokenized_pos_tweets.append((cleansed_words, sentiment))
#	count = count + 1
#scored_pos_tweets = build_features(tokenized_pos_tweets)
print()
#pprint(scored_pos_tweets)

#save_scored_pos_tweets = open("scored_pos_tweets_spanglish_800_new_tagger.pickle", "wb")
#pickle.dump(scored_pos_tweets, save_scored_pos_tweets)
#save_scored_pos_tweets.close()
#save_scored_pos_tweets = open("scored_pos_tweets_spanglish_800_new_process.pickle", "wb")
#pickle.dump(scored_pos_tweets, save_scored_pos_tweets)
#save_scored_pos_tweets.close()           

#scored_pos_tweets_f = open("scored_pos_tweets_spanglish_800.pickle", "rb")
#scored_pos_tweets = pickle.load(scored_pos_tweets_f)
#scored_pos_tweets_f.close()
#scored_pos_tweets_f = open("scored_pos_tweets_spanglish_800_new_tagger.pickle", "rb")
#scored_pos_tweets = pickle.load(scored_pos_tweets_f)
#scored_pos_tweets_f.close()
scored_pos_tweets_f = open("scored_pos_tweets_spanglish_800_new_process.pickle", "rb")
scored_pos_tweets = pickle.load(scored_pos_tweets_f)
scored_pos_tweets_f.close()

print()
#negative
#print("Negative")
count = 0
#for (tweet, sentiment) in neg_tweets:
	#print(tweet)
#	tweet_words = regex.tokenize(tweet)
#	cleansed_words = preprocess.spanglish_cleanse(tweet_words, count)
#	tokenized_neg_tweets.append((cleansed_words, sentiment))
#	count = count + 1
#pprint(tokenized_neg_tweets)
#list of word features to be extracted from the tweets
#scored_neg_tweets = build_features(tokenized_neg_tweets)
print()
#pprint(scored_neg_tweets)

#Save scored_neg_tweets bc this shit takes forever yo
#save_scored_neg_tweets = open("scored_neg_tweets_spanglish_800_new_tagger.pickle", "wb")
#pickle.dump(scored_neg_tweets, save_scored_neg_tweets)
#save_scored_neg_tweets.close()
#save_scored_neg_tweets = open("scored_neg_tweets_spanglish_800_new_process.pickle", "wb")
#pickle.dump(scored_neg_tweets, save_scored_neg_tweets)
#save_scored_neg_tweets.close()

#scored_neg_tweets_f = open("scored_neg_tweets_spanglish_800.pickle", "rb")
#scored_neg_tweets = pickle.load(scored_neg_tweets_f)
#scored_neg_tweets_f.close()
#scored_neg_tweets_f = open("scored_neg_tweets_spanglish_800_new_tagger.pickle", "rb")
#scored_neg_tweets = pickle.load(scored_neg_tweets_f)
#scored_neg_tweets_f.close()
scored_neg_tweets_f = open("scored_neg_tweets_spanglish_800_new_process.pickle", "rb")
scored_neg_tweets = pickle.load(scored_neg_tweets_f)
scored_neg_tweets_f.close()

print('LENGTH')
print(len(scored_neg_tweets))
print(len(scored_pos_tweets))

neg_tweets_cutoff = int(len(scored_neg_tweets)*(.70))
pos_tweets_cutoff = int(len(scored_pos_tweets)*(.70))
print('cutoffs')
print(neg_tweets_cutoff)
print(pos_tweets_cutoff)

print('Training')
print('Positive: ' +  str(pos_tweets_cutoff))
print('Negative: ' + str(neg_tweets_cutoff))

print('Test')
print('Positive: ' +  str(len(scored_pos_tweets) - pos_tweets_cutoff))
print('Negative: ' + str(len(scored_neg_tweets) - neg_tweets_cutoff))
print(scored_neg_tweets)
print()
print(scored_pos_tweets)

#create training set
training_features = scored_neg_tweets[:neg_tweets_cutoff] + scored_pos_tweets[:pos_tweets_cutoff]
training_set = build_feature_set(training_features)
print()
#pprint(training_set)
#Save training_set bc this shit takes forever yo
#save_training_set = open("training_set__spanglish_800_new _tagger.pickle", "wb")
#pickle.dump(training_set, save_training_set)
#save_training_set.close()
save_training_set = open("training_set__spanglish_800_new _process.pickle", "wb")
pickle.dump(training_set, save_training_set)
save_training_set.close()


#training_set_f = open("training_set_spanglish_800.pickle", "rb")
#training_set = pickle.load(training_set_f)
#training_set_f.close()

#create test set
test_features = scored_neg_tweets[neg_tweets_cutoff:] + scored_pos_tweets[pos_tweets_cutoff:]
print('TEST FEATURES')
#print(test_features)
test_set = build_feature_set(test_features)
print()
pprint(test_set)
#save_test_set = open("test_set_spanglish_800_new_tagger.pickle", "wb")
#pickle.dump(test_set, save_test_set)
#save_test_set.close()
save_test_set = open("test_set_spanglish_800_new_process.pickle", "wb")
pickle.dump(test_set, save_test_set)
save_test_set.close()

#test_set_f = open("test_set_spanglish_800.pickle", "rb")
#test_set = pickle.load(test_set_f)
#test_set_f.close()

print('LENGTH')
print(len(training_set))
print(len(test_set))

#train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

#classifier_f = open("spanglish_naivebayes_800.pickle", "rb")
#classifier = pickle.load(classifier_f)
#classifier_f.close()

print(classifier.show_most_informative_features(32))
print('Accuracy')
print(nltk.classify.accuracy(classifier, test_set))


refsets = []
testsets = []
observed = []

def labelToInt(label):
	if label == 'positive':
		return 1
	else:
		return 0


print('tweet features dictionary')
for i, (tweet_features, sentiment) in enumerate(test_set):
	#print(tweet_features)
	refsets.append(labelToInt(sentiment))
	observed = classifier.classify(tweet_features)
	testsets.append(labelToInt(observed))

index = [10,97,100,120,159,169]

for i in range(0, len(test_features)):
	if i in index:
		print(test_features[i])
	#if refsets[i] != testsets[i]:
	#	print(test_features[i])


print(refsets)
print(testsets)
accuracy = accuracy_score(refsets, testsets)
print('SKLearn Accuracy')
print(accuracy)
print()
coefficients = matthews_corrcoef(refsets, testsets)
print(coefficients)
print()

cm = nltk.ConfusionMatrix(refsets, testsets)
print(cm.pretty_format(sort_by_count=True, show_percents=False, truncate=9))
print()
print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))

precision, recall, _ = precision_recall_curve(refsets, testsets, pos_label=1)
pr_auc = auc(recall, precision)
print('Precision')
print(precision)
print('Recall')
print(recall)
print('PR AUC')
print(pr_auc)

fpr, tpr, _ = roc_curve(refsets, testsets, pos_label=1)
roc_auc = auc(fpr, tpr)
print('False Positive Rate')
print(fpr)
print('True Positive Rate')
print(tpr)
print('ROC AUC')
print(roc_auc)

print('F-Score')
print(f1_score(refsets, testsets,  average='macro'))

#Save classifier bc this shit takes forever yo
save_classifier = open("spanglish_naivebayes_800_new_process.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()


