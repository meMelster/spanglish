#!/bin/python

import sys
import re
import enchant
import json


#spanglishRegex = r'(#|@)*(S|s)panglish*'
#spanglish_tweets_file = open('spanglish_tweets.tsv', 'w+')

english_dictionary = enchant.Dict("en_US")
spanish_dictionary = enchant.Dict("es_US")

english_word = False
spanish_word = False

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




#json file of tweets passed as parameter
line_generator = open(sys.argv[1])

for line in line_generator:
    line_object = json.loads(line)

    tweet = line_object["text"]
    tweet_words = preprocess(tweet)

    # if re.search(r'spanglishRegex', tweet) != None:
    #     spanglish_tweets_file.write(*fields, sep='\t')
    #     spanglish_tweets_file.write('\n')

    # #we should check for Spanglish words as well

    for word in tweet_words:
        if english_dictionary.check(word):
            english_word = True
            print("English Word!  " + word)
        if spanish_dictionary.check(word):
            spanish_word = True
            print("Spanish Word!  " + word)
    if english_word and spanish_word:
        print("Spanglish Tweet!  " + tweet)
