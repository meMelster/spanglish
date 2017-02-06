#English version of preprocessing
#English stopwords
#English SnowballStemmer

import sys
import regex
from nltk.corpus import stopwords

#English and Spanish stemmer available
from nltk.stem import snowball

stemmer = snowball.EnglishStemmer(ignore_stopwords=False)

stop_words_list = []
flat_stop_words_list = []
exclusion_list_en_es = []

def make_stop_words_list():
	#exclude words which are in both dictionaries
	#bc they will be counted toward both languages and
	#because Dict is not iterable we collected a list in our filtering of Spanglish tweets
	with open('/home/ubuntu/data/exclusion_list.txt') as f:
		for word in f:
			stop_words_list.append(word)
	
	stop_words_list.append('...')

	#use nltk stopwords list
	stop_words_list.append(stopwords.words('english'))
	


make_stop_words_list()
flat_stop_words_list = [item for sublist in stop_words_list for item in sublist]

def tokenize(s):
	return tokens_re.findall(s)
	
def cleanse(tweet_words):
	cleansed_tweet = []
	for word in tweet_words:
		word = stemmer.stem(word)
		if word not in flat_stop_words_list:
			cleansed_tweet.append(word)
	return list(cleansed_tweet)



				

