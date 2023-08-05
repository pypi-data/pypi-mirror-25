import string

import nltk

stopwords = frozenset(nltk.corpus.stopwords.words('english'))
stopchars = frozenset(string.punctuation)


def tokenize(document):
    # use PorterStemmer for stemming
    stemmer = nltk.PorterStemmer()
    return (
        ''.join(c for c in stemmer.stem(word) if c not in stopchars)
        for word in document.lower().split() if word not in stopwords)
