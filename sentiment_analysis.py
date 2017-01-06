#TF-IDF feature extraction with scikit-learn
# vectorizer = TfidfVectorizer(min_df=2,
#                              max_df = 0.8,
#                              sublinear_tf=True,
#                              use_idf=True)

# train_vectors = vectorizer.fit_transform(train_data)
# test_vectors = vectorizer.transform(train_data)


pos.words = scan(file.path('opinion-lexicon-English', 'positive-words.txt'), what='character', comment.char=';') 
neg.words = scan(file.path('opinion-lexicon-English', 'negative-words.txt'), what='character', comment.char=';') 

score.sentiment = function(sentences, pos.words, neg.words, .progress='none') { 

    # we got a vector of sentences. plyr will handle a list or a vector as an "l" for us 
    scores = laply(sentences, function(sentence, pos.words, neg.words) { 
        # clean up sentences with R's regex-driven global substitute, gsub(): 
        sentence = gsub('[[:punct:]]', '', sentence) 
        sentence = gsub('[[:cntrl:]]', '', sentence) 
        sentence = gsub('\\d+', '', sentence) 
        # and convert to lower case: 
        sentence = tolower(sentence) 
        
        # split into words 
        word.list = str_split(sentence, '\\s+') 
        # sometimes a list() is one level of hierarchy too much 
        words = unlist(word.list) 
        
        # compare our words to the dictionaries of positive & negative lexicons 
        pos.matches = match(words, pos.words) 
        neg.matches = match(words, neg.words) 
        
        # we just want a TRUE/FALSE: 
        pos.matches = !is.na(pos.matches) 
        neg.matches = !is.na(neg.matches) 
        # TRUE/FALSE will be treated as 1/0 by sum(): 
        score = sum(pos.matches) - sum(neg.matches)
         
        return(score) 
    }, pos.words, neg.words, .progress=.progress ) 
    
    scores.df = data.frame(score=scores, text=sentences) 
    return(scores.df) 
} 
