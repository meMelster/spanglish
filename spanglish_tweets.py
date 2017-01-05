#!/bin/python

import sys
import re
import json

import enchant
from nltk.corpus import stopwords

import string


#spanglishRegex = r'(#|@)*(S|s)panglish*'
spanglish_tweets_file = open('/home/ubuntu/data/spanglish_tweets.txt', 'w')

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

punctuation = list(string.punctuation)

emoji_re = re.compile(u'['
	u'\U0001F300-\U0001F64F'
	u'\U0001F680-\U0001F6FF'
	u'\U0001F910-\U0001F940'
	u'\u2600-\u26FF\u2700-\u27BF]+'
	, re.UNICODE)
	
hashtag_re = re.compile(r"(#+[\w_]+[\w\'_\-]*[\w_]+)")


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


clean_english_dictionary()

#json file of tweets passed as parameter
line_generator = open(sys.argv[1])

for line in line_generator:
	line_object = json.loads(line)

	if "text" in line_object:
		tweet = line_object["text"]
		tweet_words = preprocess(tweet)
		spanglish_tweets_file.write(tweet+ '\n')
		# if re.search(r'spanglishRegex', tweet) != None:
		#     spanglish_tweets_file.write(*fields, sep='\t')
		#     spanglish_tweets_file.write('\n')

		# #we should check for Spanglish words as well

		#determine if the tweet is Spanglish
		for word in tweet_words:
			#spanglish_tweets_file.write("WORD " + word + "\n")
			#spanglish_tweets_file.write(str(re.findall(r"#(\w+)", word)) + "\n")
			hashtag = hashtag_re.search(word)
			#spanglish_tweets_file.write("HASHTAG " + str(hashtag) + "\n")
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
			#not a number or an emoji
			if word.lower() in spanglish_dictionary:
				#spanglish_tweets_file.write("Spanglish Word!  " + word + '\n')
				english_word = True
				spanish_word = True
				break
			if not (bool(re.search(r'\d', word)) or emoji_re.search(word) or len(word)<2 or word=="\n" or word.endswith("...")):
				if word not in punctuation:
					if not (english_dictionary.check(word) and spanish_dictionary.check(word)):
						if english_dictionary.check(word):
							english_word = True
							#spanglish_tweets_file.write("English Word!  " + word + '\n')
						if spanish_dictionary.check(word):
							spanish_word = True
							#spanglish_tweets_file.write("Spanish Word!  " + word + '\n')
		if english_word and spanish_word:
			#print("Spanglish Tweet!  " + tweet)
			spanglish_tweets_file.write(tweet + '\n')
		english_word = False
		spanish_word = False

spanglish_tweets_file.close()



#TF-IDF feature extraction with scikit-learn
# vectorizer = TfidfVectorizer(min_df=2,
#                              max_df = 0.8,
#                              sublinear_tf=True,
#                              use_idf=True)

# train_vectors = vectorizer.fit_transform(train_data)
# test_vectors = vectorizer.transform(train_data)

