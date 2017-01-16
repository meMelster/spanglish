import nltk
from pprint import pprint
from nltk.corpus import sentiwordnet as swn
from nltk.internals import find_jars_within_path
#English and Spanish POS-tagger available
from nltk.tag import StanfordPOSTagger

tagger = StanfordPOSTagger('/home/ubuntu/spanglish/tools/english-bidirectional-distsim.tagger', '/home/ubuntu/spanglish/tools/stanford-postagger.jar')

stanford_dir = tagger._stanford_jar[0].rpartition('/')[0]
stanford_jars = find_jars_within_path(stanford_dir)
tagger._stanford_jar = ':'.join(stanford_jars)

wordlist = []

def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(tweets):
	word_features = []
	wordlist = get_words_in_tweets(tweets)
	wordlist = nltk.FreqDist(wordlist[0])
	
	tagged_tweets = []
	scored_tweets = []
	for (words, sentiment) in tweets:
		pos = tagger.tag(words)
		tagged_tweets.append((pos, sentiment))
	
	result = []
	for (words, sentiment) in tagged_tweets:
		scored_words = []
		tweet_score = 0
		for word, tag in words:
			newtag=''
			if tag.startswith('NN'):
				newtag='n'
			elif tag.startswith('JJ'):
				newtag='a'
			elif tag.startswith('V'):
				newtag='v'
			elif tag.startswith('R'):
				newtag='r'
			else:
				newtag=''
			if(newtag!=''):
				synsets = list(swn.senti_synsets(word, newtag))
				#Getting average of all possible sentiments
				score=0
				if(len(synsets)>0):
					for syn in synsets:
						score+=syn.pos_score()-syn.neg_score()
					scored_words.append((word, score/len(synsets)))
					tweet_score = (score/len(synsets)) + tweet_score
				else:
					scored_words.append((word, 0))
		#print(scored_words)
		#print(tweet_score)
		if len(scored_words)>0:
			scored_tweets.append((((scored_words, tweet_score)), sentiment))
	return scored_tweets
	
	
def extract_features(tweet):
	features = {}
	print("Tweet: " + str(tweet))
	print("\n")
	#features['sentiment'] = sentiment
	features['tweet_score'] = tweet[1]
	features['word_count'] = len(tweet[0])
	return features
 
def build_features(tweets):
	scored_tweets = get_word_features(tweets)
	return scored_tweets
	 
def build_training_set(tweets):
	featuresets = [(extract_features(tweet), sentiment) for (tweet, sentiment) in tweets]
	train_set = []
	train_set = featuresets
	return train_set
