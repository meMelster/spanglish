#Spanish version of preprocessing
#Bing translator Spanish->English
#English stopwords
#English SnowballStemmer

import sys
import re
from nltk.corpus import stopwords
from mstranslator import Translator
#English and Spanish stemmer available
from nltk.stem import snowball
import string
import regex 
#English because we translate first
stemmer = snowball.EnglishStemmer(ignore_stopwords=False)

translator = Translator('60864ac93121426d8fbbb1e2581a8c3e')

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
	#in English bc it has been translated already
	stop_words_list.append(stopwords.words('english'))
	


make_stop_words_list()
flat_stop_words_list = [item for sublist in stop_words_list for item in sublist]

def tokenize(s):
	return tokens_re.findall(s)
	
def sp_cleanse(tweet_words, count):
	cleansed_tweet = []
	result_tweet = []
	eng_words = []
	print(tweet_words)
	for word in tweet_words:
		#print(word)
		url = regex.urls_re.search(word)
		#print(url)
		if url:
			tweet_words.remove(word)
		else:
			if word in string.punctuation:
				if word not in punctuation:
					tweet_words.remove(word)
			else:
				hashtag = regex.hashtag_or_mention_re.search(word)
				if hashtag:
					has_hashtag_or_mention[count] = True
					temp = word[1:]
					#print("WORD " + word + "\n")
					temp = re.sub("([a-z])([A-Z])","\g<1> \g<2>",temp)
					temp = temp.split()
					#print("TEMP " + str(temp) + "\n")
					if len(temp)>1:
						for hashtag_word in temp:
							print(hashtag_word)
							tweet_words.append(hashtag_word)
					else:
						tweet_words.append(temp[0])	
					tweet_words.remove(word)
				else:
					cleansed_tweet.append(word)
				
	print(cleansed_tweet)			
	for word in cleansed_tweet:
		translated_word = translator.translate(word, lang_from='es', lang_to='en').split(' ')
		#print(translated_word)
		for w in translated_word:
			eng_words.append(w)
		#print(eng_words)
			
	for word in eng_words:
		word_eng_stemmed = stemmer.stem(word)
		if word_eng_stemmed not in flat_stop_words_list:
			result_tweet.append(word_eng_stemmed)
	print(result_tweet)
	print()
	return list(result_tweet)
