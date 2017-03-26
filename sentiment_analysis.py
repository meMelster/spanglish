import nltk
from pprint import pprint
from nltk.corpus import sentiwordnet as swn
from nltk.internals import find_jars_within_path
#English and Spanish POS-tagger available
from nltk.tag import StanfordPOSTagger
import string
import regex
import re
from spanish_preprocessing import has_hashtag_or_mention

#tagger = StanfordPOSTagger('/home/ubuntu/spanglish/tools/english-bidirectional-distsim.tagger', '/home/ubuntu/spanglish/tools/stanford-postagger.jar')

#stanford_dir = tagger._stanford_jar[0].rpartition('/')[0]
#stanford_jars = find_jars_within_path(stanford_dir)
#tagger._stanford_jar = ':'.join(stanford_jars)

#has_hashtag_or_mention = [False] * 800

wordlist = []

negation = ['no', 'not', 'nil', 'nope', 'nah', 'naw', 'non', 'nan']

punctuation = list(string.punctuation)

def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(tweets):
	print(has_hashtag_or_mention)
	word_features = []
	print(tweets)
	wordlist = get_words_in_tweets(tweets)
	print('WORD LIST')
	wordlist = nltk.FreqDist(wordlist)
	pprint(wordlist)
	print()
	
	tagged_tweets = []
	scored_tweets = []
	count = 0
	for (words, sentiment) in tweets:
		try:
			pos = nltk.pos_tag(words)
			print(pos)
			print()
			tagged_tweets.append((pos, sentiment))
		except:
			print("Error getting POS for " + str(words))
			print("Moving on to next tweet")
		count = count + 1
	print('LENGTH')
	print(len(tagged_tweets))
	result = []
	count = 0
	for (words, sentiment) in tagged_tweets:
		#print(words)
		scored_words = []
		
		tweet_score = 0
		contains_negation = False
		contains_all_caps_word = False
		all_caps_word_count = 0
		contains_special_characters = False
		special_character_count = 0
		noun_count = 0
		adjective_count = 0
		verb_count = 0
		adverb_count = 0
		emoji_count = 0
		pos_emoji = False
		neg_emoji = False
		pos_wods = []
		print('WORDS')
		for word, tag in words:
			print(words)
			if regex.emoji_re.search(word):
				emoji_count = emoji_count + 1
			if regex.positive_emoticon_re.search(word):
				pos_emoji = True
			if regex.negative_emoticon_re.search(word):
				neg_emoji = True
			if word in negation:
				contains_negation = True
			if word.isupper():
				contains_all_caps_word = True
				all_caps_word_count = all_caps_word_count + 1
			if word in punctuation:
				contains_special_characters = True
				special_character_count = special_character_count + 1
			else:
				newtag=''
				if tag.startswith('NN'):
					newtag = 'n'
					noun_count = noun_count + 1
				elif tag.startswith('JJ'):
					newtag = 'a'
					adjective_count = adjective_count + 1
				elif tag.startswith('V'):
					newtag = 'v'
					verb_count = verb_count + 1
				elif tag.startswith('R'):
					newtag = 'r'
					adverb_count = adverb_count + 1
				else:
					newtag=''
				if(newtag!=''):
					synsets = list(swn.senti_synsets(word, newtag))
					print(synsets)
					#Getting average of all possible sentiments
					score=0
					if(len(synsets)>0):
						for syn in synsets:
							print(syn)
							print(syn.pos_score())
							print(syn.neg_score())
							score+=syn.pos_score()-syn.neg_score()
						scored_words.append((word, score/len(synsets)))
						tweet_score = (score/len(synsets)) + tweet_score
					else:
						scored_words.append((word, 0))
				else:
					scored_words.append((word, 0))
		#print(scored_words)
		print(tweet_score)
		#if len(scored_words)>0:
		if len(words) > 0:
			t = (((scored_words, tweet_score/len(words), contains_negation, contains_all_caps_word, all_caps_word_count/len(words), contains_special_characters, special_character_count/len(words), noun_count/len(words), adjective_count/len(words), verb_count/len(words), adverb_count/len(words), emoji_count/len(words), has_hashtag_or_mention[count], pos_emoji, neg_emoji)), sentiment)
			scored_tweets.append(t)
		else:
			print('EMPTY')
			print(words)
			t = (((scored_words, tweet_score, contains_negation, contains_all_caps_word, all_caps_word_count, contains_special_characters, special_character_count, noun_count, adjective_count, verb_count, adverb_count, emoji_count, has_hashtag_or_mention[count], pos_emoji, neg_emoji)), sentiment)
			scored_tweets.append(t)
		#print(t)
		
		count = count + 1
	return scored_tweets
	
	
def extract_features(tweet):
	features = {}

	if(tweet[1] > 0):
		features['has_positive_tweet_score'] = True
		features['has_negative_tweet_score'] = False
	elif(tweet[1] < 0):
		features['has_negative_tweet_score'] = True
		features['has_positive_tweet_score'] = False
	else:
		features['has_positive_tweet_score'] = False
		features['has_negative_tweet_score'] = False
	
	if(len(tweet[0]) > 6):
		features['word_count_greater_than_six'] = True
	else:
		features['word_count_greater_than_six'] = False
		
	if(tweet[8] > 0):
		features['has_adjective'] = True
	else:
		features['has_adjective'] = False

		
	features['hash_hashtag_or_mention'] = tweet[12]
	features['has_positive_emoji'] = tweet[13]
	features['has_negative_emoji'] = tweet[14]

	
	return features
 
def build_features(tweets):
	scored_tweets = get_word_features(tweets)
	return scored_tweets
	 
def build_feature_set(tweets):
	#print()
	#print(tweets)
	featuresets = [(dict(extract_features(tweet)), sentiment) for (tweet, sentiment) in tweets]
	return featuresets
	
def cleanse_mention_and_hashtag_words(tweet_words, hash_hashtag_or_mention, count):
	cleansed_tweet = []
	for word in tweet_words:
			hashtag = regex.hashtag_or_mention_re.search(word)
			if hashtag:
				has_hashtag_or_mention[count] = True
				temp = word[1:]
				#print("WORD " + word + "\n")
				temp = re.sub("([a-z])([A-Z])","\g<1> \g<2>",temp)
				temp = temp.split()
				#print("TEMP " + str(temp) + "\n")
				if len(temp)>1:
					for hastag_word in temp:
						tweet_words.append(hastag_word)
				else:
					tweet_words.append(temp[0])	
				tweet_words.remove(word)
			else:
				cleansed_tweet.append(word)
	return list(cleansed_tweet)
