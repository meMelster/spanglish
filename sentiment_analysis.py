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

negation = ['no', 'not', 'nil', 'nope', 'nah', 'naw', 'non', 'nan']

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
		#print(words, sentiment)
		pos = tagger.tag(words)
		print(pos)
		tagged_tweets.append((pos, sentiment))
	
	#print(tagged_tweets)
	result = []
	for (words, sentiment) in tagged_tweets:
		#print(words)
		scored_words = []
		tweet_score = 0
		contains_negation = False
		for word, tag in words:
			if word in negation:
				contains_negation = True
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
			scored_tweets.append((((scored_words, tweet_score, contains_negation)), sentiment))
	return scored_tweets
	
	
def extract_features(tweet):
	features = {}
	features['tweet_score'] = tweet[1]
	features['word_count'] = len(tweet[0])
	features['contains_negation'] = tweet[2]
	return features
 
def build_features(tweets):
	scored_tweets = get_word_features(tweets)
	return scored_tweets
	 
def build_feature_set(tweets):
	featuresets = [(extract_features(tweet), sentiment) for (tweet, sentiment) in tweets]
	return featuresets
