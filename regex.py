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
	u'\U0001F617-\U0001F619'
	u'\u263A'
	u'\U0001F642'
	u'\U0001F917'
	u'\U0001F61A'
	u'\U0001F48B-\U0001F49C'
	u'\u2764]+'
	, re.UNICODE)
	
negative_emoticon_re = re.compile(u'['
	u'\U0001F641'
	u'\U0001F616'
	u'\u2639'
	u'\U0001F61E-\U0001F622'
	u'\U0001F624'
	u'\U0001F626-\U0001F629'
	u'\U0001F62C-\U0001F62D'
	u'\U0001F630-\U0001F631'
	u'\U0001F633'
	u'\U0001F635]+'
	, re.UNICODE)

#puñeta	
spanish_n_re = re.compile(u'['
	u'U0070U0075U00F1U0065U0074U0061]+'
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
urls_re = re.compile(r'(http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+)')



def tokenize(s):
	return tokens_re.findall(s)
