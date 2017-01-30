import sys
import csv

list = []

#convert labeled tweets in tsv to list of tuples
def labeled_tweets_tsv_to_list(tsv_file):
	pos = 0
	neg = 0
	with open(tsv_file) as f:
		for line in f:
			t = tuple(line.strip().split('\t'))
			if len(t)>1:
				#print(t)
				if 'neutral' not in t[1]:
					if 'positive' in t[1]:
						pos = pos + 1
					else:
						neg = neg + 1
					list.append(t)
	return list, pos, neg

#lines = list(line for line in (l.strip() for l in f) if line)
