import sys
import csv

list = []

#convert labeled tweets in tsv to list of tuples
def labeled_tweets_tsv_to_list(tsv_file):
	with open(tsv_file) as f:
		for line in f:
			list.append(tuple(line.strip().split('\t')))
	return list

