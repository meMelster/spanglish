#Spanglish version of preprocessing
#English stopwords
#Both English and Spanish SnowballStemmer
#English POS-Tagging
#English Senitment Lexicon (SentiWordNet)

import sys
import re
import string
from nltk.corpus import stopwords
import regex

from mstranslator import Translator 

#English and Spanish stemmer available
from nltk.stem import snowball

eng_stemmer = snowball.EnglishStemmer(ignore_stopwords=False)
spn_stemmer = snowball.SpanishStemmer(ignore_stopwords=False)

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
	stop_words_list.append(stopwords.words('english'))
	 

make_stop_words_list()
flat_stop_words_list = [item for sublist in stop_words_list for item in sublist]

def tokenize(s):
	return tokens_re.findall(s)
	
def spanglish_cleanse(tweet_words, count):
	chente = False
	if 'Chente' in tweet_words:
		print(tweet_words)
		chente = True
	cleansed_tweet = []
	result_tweet = []
	eng_words = []
	print('SPANGLISH CLEANSE')
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
				print(hashtag)
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
	#print(has_hashtag_or_mention[count])	
	
	for word in cleansed_tweet:
		#print(word)
		if word.lower().startswith('ching'):
			word = 'stupid'
			print('ching')
		if word.lower().startswith('pendej'):
			word = 'stupid'
			print('pendej')
		if word.lower().startswith('pinche'):
			word = 'stupid'
			print('pinche')
		if word.lower().startswith('puto'):
			word = 'stupid'
			print('puto')
		if word.lower().startswith('puta'):
			word = 'bad'
			print('puta')
		if 'jaja' in word.lower():
			word = 'happy'
			print('jaja')
		if 'jeje' in word.lower():
			word = 'happy'
			print('jeje')
		if 'chido' in word.lower():
			word = 'happy'
			print('chido')
		puneta = regex.spanish_n_re.search(word)
		if puneta:
			word = 'stupid'
			print('puñeta')
		if word.lower().startswith('verga'):
			word = 'stupid'
			print('verga')
		if word.lower().startswith('culec'):
			word = 'stupid'
			print('culec')
		if word.lower().startswith('choch'):
			word = 'stupid'
			print('choch')
		if word.lower().startswith('cojer'):
			word = 'stupid'
			print('cojer')
		if word.lower().startswith('pena'):
			word = 'embarrass'
			print('pena')
		translated_word = translator.translate(word, lang_from='es', lang_to='en').split(' ')
		print(translated_word)
		print(word)
		for word in translated_word:
			eng_words.append(word)
	
	print(eng_words)
			
	for w in eng_words:	
		word_eng_stemmed = eng_stemmer.stem(w)
		#catch any Spanglish words that may not have been stemmed
		spanglish_stemmed_word = spn_stemmer.stem(word_eng_stemmed)
		print(spanglish_stemmed_word)
		if spanglish_stemmed_word not in flat_stop_words_list:
			result_tweet.append(spanglish_stemmed_word)
	if chente:
		print('RESULT TWEET')
		print(result_tweet)
	print()
	return list(result_tweet)

