from nltk.corpus import stopwords


punctuation = list(string.punctuation)

stop_words_list = []
flat_stop_words_list = []

def make_stop_words_list():
    #exclude words which are in both dictionaries
    #bc they will be counted toward both languages and
    # without further analysis we would not know which language it was truely in
    #stop_words_list.append(list(set(eng_dict) & set(spn_dict)))

    stop_words_list.append(punctuation)

    #use nltk stopwords list
    stop_words_list.append(stopwords.words('english'))
    stop_words_list.append(stopwords.words('spanish'))



emoji_re = re.compile(u'['
    u'\U0001F300-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\U0001F910-\U0001F940'
    u'\u2600-\u26FF\u2700-\u27BF]+'
    , re.UNICODE)


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

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


make_stop_words_list()
flat_stop_words_list = [item for sublist in stop_words_list for item in sublist]
#print(flat_stop_words_list)