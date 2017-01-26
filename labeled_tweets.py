import sys
import csv

list = []

#convert labeled tweets in tsv to list of tuples
def labeled_tweets_tsv_to_list(tsv_file):
	with open(tsv_file) as f:
		for line in f:
			t = tuple(line.strip().split('\t'))
			if len(t)>1:
				#print(t)
				list.append(t)
	return list

#lines = list(line for line in (l.strip() for l in f) if line)
