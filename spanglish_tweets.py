#!/bin/python

import sys
import re
import json

import enchant
from nltk.corpus import stopwords
import nltk 

import string


#spanglishRegex = r'(#|@)*(S|s)panglish*'
spanglish_tweets_file = open('/home/ubuntu/data/us_mx_spanglish_tweets_jan06.2.txt', 'w')
exclusion_list_en_es = open('/home/ubuntu/data/exclusion_list.txt', 'w+')

english_dictionary = enchant.Dict("en_US")
spanish_dictionary = enchant.Dict("es")
#create Spanglish dictionary
spanglish_dictionary = [
	'spanglish',
	'troca',
	'mopear',
	'checke',
	'renta',
	'billes',
	'pusha',
	'lunche',
	'puerco',
	'trinche'
	]

english_word = False
spanish_word = False

spanglish_tweets = []

tweet_count = 0
spanglish_tweet_count = 0

punctuation = list(string.punctuation)

emoji_re = re.compile(u'['
	u'\U0001F300-\U0001F64F'
	u'\U0001F680-\U0001F6FF'
	u'\U0001F910-\U0001F940'
	u'\u2600-\u26FF\u2700-\u27BF]+'
	, re.UNICODE)
	
hashtag_re = re.compile(r"((@|#)+[\w_]+[\w\'_\-]*[\w_]+)")


emoticons_str = r"""
	(?:
		[:=;] #eyes
		[oO\-]? #nose (optional)
		[D\)\]\(\]/\\OpP] #mouth
	)"""

regex_str = [
	emoticons_str,
	r'<[^>]+>', #HTML tags
	r'(?:@[\w_]+)', #@mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", #hashtag
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', #URLs
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', #numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", #words with - and '
	r'(?:[\w_]+)', #other words
	r'(?:\S)' #anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens



def clean_english_dictionary():
	#manual cleanse of words in English dictionary that are used in Spanish language
	english_dictionary.remove("Eu")
	english_dictionary.remove("um")
	english_dictionary.remove("to")
	
def extract_entity_names(t):
	entity_names = []
	
	if hasattr(t, 'node') and t.node:
		if t.node == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return entity_names


clean_english_dictionary()


#json file of tweets passed as parameter
line_generator = open(sys.argv[1])

for line in line_generator:
	line_object = json.loads(line)
	if spanglish_tweet_count == 12000:
		break
	tweet_count += 1

	if "text" in line_object:
		tweet = line_object["text"]
		tweet_words = preprocess(tweet)
		#spanglish_tweets_file.write(tweet + "\n")
		

		#determine if the tweet is Spanglish
		for word in tweet_words:
			hashtag = hashtag_re.search(word)
			if hashtag:
				temp = word[1:]
				#spanglish_tweets_file.write("WORD " + word + "\n")
				temp = re.sub("([a-z])([A-Z])","\g<1> \g<2>",temp)
				temp = temp.split()
				#spanglish_tweets_file.write("TEMP " + str(temp) + "\n")
				if len(temp)>1:
					for hastag_word in temp:
						tweet_words.append(hastag_word)
				else:
					tweet_words.append(temp[0])	
				tweet_words.remove(word)
				#spanglish_tweets_file.write("New Tweet Words  " + str(tweet_words) + '\n')

			if word.lower() in spanglish_dictionary:
				#spanglish_tweets_file.write("Spanglish Word!  " + word + '\n')
				english_word = True
				spanish_word = True
				break
			#not a number or an emoji
			if not (bool(re.search(r'\d', word)) or emoji_re.search(word) or len(word)<2 or word=="\n" or word.endswith("...")):
				if word not in punctuation:
					if not (english_dictionary.check(word) and spanish_dictionary.check(word)):
						if english_dictionary.check(word):
							english_word = True
							#spanglish_tweets_file.write("English Word!  " + word + '\n')
						if spanish_dictionary.check(word):
							spanish_word = True
							#spanglish_tweets_file.write("Spanish Word!  " + word + '\n')
					else:
						exclusion_list_en_es.write(word + '\n')
		if english_word and spanish_word:
			#print("Spanglish Tweet!  " + tweet)
			spanglish_tweets_file.write(tweet + '\n')
			spanglish_tweet_count += 1
		english_word = False
		spanish_word = False


spanglish_tweets_file.write('\n')
spanglish_tweets_file.write('\n')
spanglish_tweets_file.write('\n')
spanglish_tweets_file.write('Total Original Tweets Streamed: ' + str(tweet_count) + '\n')
spanglish_tweets_file.write('Total Spanglish Tweets : ' + str(spanglish_tweet_count) + '\n')
spanglish_tweets_file.write('Percentage of Streamed Tweets determined to be Spanglish : ' + str((spanglish_tweet_count/tweet_count)*100) + '\n')
spanglish_tweets_file.close()
exclusion_list_en_es.close()

