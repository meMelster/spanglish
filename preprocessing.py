import sys
import re
import string
from labeled_tweets import labeled_tweets_csv_to_list

from nltk.corpus import stopwords

#English and Spanish stemmer available
from nltk.stem import SnowballStemmer



#This file to be passed spanglish_tweets.txt

punctuation = list(string.punctuation)

stop_words_list = []
flat_stop_words_list = []
exclusion_list_en_es = []

cleansed_tweet = []

cleansed_spanglish_tweets_file = open('/home/ubuntu/data/cleansed_spanglish_tweets.txt', 'w')


def make_stop_words_list():
	#exclude words which are in both dictionaries
	#bc they will be counted toward both languages and
	#stop_words_list.append(list(set(eng_dict) & set(spn_dict)))
	#because Dict is not iterable we collected a list in our filtering of Spanglish tweets
	with open('/home/ubuntu/data/exclusion_list.txt') as f:
		for word in f:
			stop_words_list.append(word)
	
	stop_words_list.append(punctuation)
	stop_words_list.append('...')

	#use nltk stopwords list
	stop_words_list.append(stopwords.words('english'))
	stop_words_list.append(stopwords.words('spanish'))

hashtag_re = re.compile(r"((@|#)+[\w_]+[\w\'_\-]*[\w_]+)")

emoji_re = re.compile(u'['
	u'\U0001F300-\U0001F64F'
	u'\U0001F680-\U0001F6FF'
	u'\U0001F910-\U0001F940'
	u'\u2600-\u26FF\u2700-\u27BF]+'
	, re.UNICODE)


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


make_stop_words_list()
flat_stop_words_list = [item for sublist in stop_words_list for item in sublist]
print(flat_stop_words_list)

with open(sys.argv[1]) as f:
	for tweet in f:
		#cleansed_spanglish_tweets_file.write(tweet + '\n')
		#parse tweets
		tweet_words = preprocess(tweet)
		#cleansed_spanglish_tweets_file.write(str(tweet_words) + '\n')
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
			else:
				if word not in flat_stop_words_list:
					print(word)
					cleansed_tweet.append(word)
					#cleansed_spanglish_tweets_file.write(str(cleansed_tweet) + '\n')
		cleansed_spanglish_tweets_file.write(str(cleansed_tweet) + '\n')
		cleansed_tweet[:] = []

	
				
cleansed_spanglish_tweets_file.close()
				

