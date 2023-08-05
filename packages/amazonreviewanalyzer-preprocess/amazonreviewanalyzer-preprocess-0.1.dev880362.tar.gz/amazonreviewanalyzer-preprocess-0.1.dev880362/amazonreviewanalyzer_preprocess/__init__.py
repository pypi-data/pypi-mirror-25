import string

import nltk


# read CSV file at package level so that the data is cached
from amazonreviewanalyzer_preprocess.csvreader import readfile
reviews = readfile('amazon_reviews.csv')


stopwords = frozenset(nltk.corpus.stopwords.words('english'))
stopchars = frozenset(string.punctuation)

def tokenize(document):
    # use PorterStemmer for stemming
    stemmer = nltk.PorterStemmer()
    return (
        ''.join(c for c in stemmer.stem(word) if c not in stopchars)
        for word in document.lower().split() if word not in stopwords)
