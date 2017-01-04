#!/bin/python

import sys
import re
import enchant
import json


#spanglishRegex = r'(#|@)*(S|s)panglish*'
spanglish_tweets_file = open('data/spanglish_tweets.txt', 'w')

english_dictionary = enchant.Dict("en_US")
spanish_dictionary = enchant.Dict("es_US")

english_word = False
spanish_word = False

spanglish_tweets = []

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

    if "text" in line_object:
        tweet = line_object["text"]
        tweet_words = preprocess(tweet)

        # if re.search(r'spanglishRegex', tweet) != None:
        #     spanglish_tweets_file.write(*fields, sep='\t')
        #     spanglish_tweets_file.write('\n')

        # #we should check for Spanglish words as well

        for word in tweet_words:
            if english_dictionary.check(word):
                english_word = True
                spanglish_tweets_file.write("English Word!  " + word + '\n')
            if spanish_dictionary.check(word):
                spanish_word = True
                spanglish_tweets_file.write("Spanish Word!  " + word + '\n')
        if english_word and spanish_word:
            #print("Spanglish Tweet!  " + tweet)
            spanglish_tweets_file.write(tweet + '\n')

spanglish_tweets_file.close()



#TF-IDF feature extraction with scikit-learn
# vectorizer = TfidfVectorizer(min_df=5,
#                              max_df = 0.8,
#                              sublinear_tf=True,
#                              use_idf=True)
# train_vectors = vectorizer.fit_transform(train_data)
# test_vectors = vectorizer.transform(train_data)