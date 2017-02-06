import re



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




positive_emoticon_re = re.compile(u'['
	u'\U0001F601-\U0001F60D'
	u'\U0001F618'
	u'\U0001F61A]+'
	, re.UNICODE)
	
negative_emoticon_re = re.compile(u'['
	u'\U0001F61E-\U0001F637]+'
	, re.UNICODE)
	
emoji_re = re.compile(u'['
    u'\U0001F300-\U0001F64F'
	u'\U0001F680-\U0001F6FF'
	u'\U0001F910-\U0001F940'
	u'\u2600-\u26FF\u2700-\u27BF]+'
	, re.UNICODE)

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
hashtag_or_mention_re = re.compile(r"((@|#)+[\w_]+[\w\'_\-]*[\w_]+)")



def tokenize(s):
	return tokens_re.findall(s)
