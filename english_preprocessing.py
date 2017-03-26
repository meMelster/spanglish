#English version of preprocessing
#English stopwords
#English SnowballStemmer

import sys
import regex
from nltk.corpus import stopwords
import regex
import string
import re

#English and Spanish stemmer available
from nltk.stem import snowball

stemmer = snowball.EnglishStemmer(ignore_stopwords=False)

stop_words_list = []
flat_stop_words_list = []
exclusion_list_en_es = []
has_hashtag_or_mention = [False] * 800

punctuation = []
punctuation.append(list(string.punctuation[2:6]))
punctuation.append(string.punctuation[9])
punctuation.append(list(string.punctuation[20:22]))

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
	
def cleanse(tweet_words, count):
	cleansed_tweet = []
	result_tweet = []
	print(tweet_words)
	for word in tweet_words:
		print(word)
		url = regex.urls_re.search(word)
		print(url)
		if url:
			tweet_words.remove(word)
		else:
			if word in string.punctuation:
				if word not in punctuation:
					tweet_words.remove(word)
			else:
				print('hashtag')
				hashtag = regex.hashtag_or_mention_re.search(word)
				print(hashtag)
				if hashtag:
					has_hashtag_or_mention[count] = True
					temp = word[1:]
					#print("WORD " + word + "\n")
					temp = re.sub("([a-z])([A-Z])","\g<1> \g<2>",temp)
					temp = temp.split()
					print("TEMP " + str(temp) + "\n")
					if len(temp)>1:
						for hashtag_word in temp:
							print(hashtag_word)
							tweet_words.append(hashtag_word)
					else:
						cleansed_tweet.append(temp[0])
						#tweet_words.append(temp[0])	
					tweet_words.remove(word)
				else:
					cleansed_tweet.append(word)
				
	print()
	print('cleansed tweet')
	print(cleansed_tweet)
	for word in cleansed_tweet:
		print(word)
		stemmed_word = stemmer.stem(word)
		print(stemmed_word)
		if stemmed_word not in flat_stop_words_list:
			result_tweet.append(stemmed_word)
	return list(result_tweet)



				

