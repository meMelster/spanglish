import nltk
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
	
	
	for (words, sentiment) in tagged_tweets:
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
						scored_tweets.append(((word, score/len(synsets)), sentiment))
				else:
					scored_tweets.append(((word, 0), sentiment))
	#print(str(scored_tweets) + "Shows us SentiScore per tweet")
	return scored_tweets
	
	
def extract_features(tweet):
	features = {}
	#print(str(tweet))
	for (words_score, sentiment) in tweet:
		features['sentiment'] = sentiment
		for word_tag_list, score in words_score:
			features['sentiscore'] = score
			for word, tag in word_tag_list:
				features['word_count'] = len(word_tag_list)
	print(features)
	return features
 
def build_features(tweets):
	scored_tweets = get_word_features(tweets)
	return scored_tweets
	 
def build_training_set(tweets):
	return nltk.classify.apply_features(extract_features, tweets)
