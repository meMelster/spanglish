import sys
import csv
import re

list_of_tuples = []

#convert labeled tweets in tsv to list of tuples
def labeled_tweets_tsv_to_list(tsv_file):
	pos_re = re.compile(r"((p|P)+[\w_]+[\w\'_\-]*[\w_]+)")
	neutral_re = re.compile(r"((neu|nue)+[\w_]+[\w\'_\-]*[\w_]+)")
	pos = 0
	neg = 0
	with open(tsv_file) as f:
		for line in f:
			t = list(line.strip().split('\t'))
			if len(t)>1:
				#print(t)
				if not neutral_re.search(t[1]):
					if pos_re.search(t[1]):
						pos = pos + 1
						t[1] = 'positive'
						print(t[1])
					else:
						neg = neg + 1
						t[1] = 'negative'
						print(t[1])
					list_of_tuples.append(tuple(t))
	#print('POSITIVE: ' + str(pos))
	#print('NEGATIVE: ' + str(neg))
	return list_of_tuples, pos, neg

#lines = list(line for line in (l.strip() for l in f) if line)

#raw_labeled_tweets, pos, neg = labeled_tweets_tsv_to_list('/home/ubuntu/spanglish/data/labeled_tweets.tsv')
