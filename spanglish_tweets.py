#!/bin/python

import sys
import re
import enchant

# parameter should be downloadedTweets.tsv

spanglishRegex = (#|@)*(S|s)panglish*

tweet_file = open(sys.argv[0], 'r')
spanglish_tweets_file = open('spanglish_tweets.tsv', 'w+')

english_dictionary = enchant.Dict("en_US")
spanish_dictionary = enchant.Dict("es_US")

for line in tweet_file:
    fields = line.rstrip('\n').split('\t')
    sid = fields[0]
    uid = fields[1]
    tweet = fields[2]

    if re.search(r'spanglishRegex', tweet) != None:
        spanglish_tweets_file.write(*fields, sep='\t')
        spanglish_tweets_file.write('\n')

    english_word = false
    spanish_word = false
    #not sure if we should check for Spanglish words as well

    tweet_words = tweet.split(' ')
    for word in tweet_words:
        if english_dictionary.check(word):
            english_word = true
        if spanish_dictionary.check(word):
            spanish_word = true
    if english_word && spanish_word:
        spanglish_tweets_file.write(*fields, sep='\t')
        spanglish_tweets_file.write('\n')
