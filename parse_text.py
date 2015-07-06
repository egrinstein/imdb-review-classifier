import collections,re
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

import sys

def _slugify(text):
	"Removes html tags,punctuation and puts everything in lowercase"
	slug = BeautifulSoup(text,"html5lib").get_text()
	slug = re.sub("[^a-zA-Z]", " ", slug )  
	slug = slug.lower()
	return slug

def _get_meaningful_words(text):
    
	words = text.split()	

	stopwords_set = set(nltk.corpus.stopwords.words("english"))
	filtered = ""
	#words = [w for w in words if not w in stopwords_set]
	for word in words:
            if word not in stopwords_set:
                try:
                    if word[-1] == 's':
                        filtered += word[0:-1]
                    else:
                        filtered += word
                    filtered += ' '
                except IndexError:
                    continue
	return filtered



def filter_text(text):
	filtered = _slugify(text)
	filtered = _get_meaningful_words(filtered)
	return filtered




