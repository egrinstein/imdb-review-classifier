import collections,re
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

import sys

def _slugify(text):
	"Removes html tags,punctuation and puts everything in lowercase"
	slug = BeautifulSoup(text).get_text()
	slug = re.sub("[^a-zA-Z]", " ", slug )  
	slug = slug.lower()
	return slug

def _get_meaningful_words(text):
	"removes stopwords from a slugged text"
	#stemmer = nltk.stem.PorterStemmer()
	#words = nltk.word_tokenize(text)
	#words = nltk.pos_tag(words)
	words = text.split()	

	stopwords_set = set(nltk.corpus.stopwords.words("english"))
	filtered = ""
	#words = [w for w in words if not w in stopwords_set]
	for word in words:
		if word not in stopwords_set:
			#print word
			try:
				if word[-1] == 's':
					filtered += word[0:-1]
				else:
					filtered += word

				if word == 'not':
					filtered += '_'
				else:
					filtered += ' '
			except IndexError:
				continue
	return filtered

def _create_features(texts):
	vectorizer = CountVectorizer(analyzer = "word",   
				 tokenizer = None,    
				 preprocessor = None,
				 stop_words = None,  
				 max_features = 200) 
	features = vectorizer.fit_transform(texts)
	
	print vectorizer.get_feature_names()
	features = features.toarray()
	
	#feature_names = vectorizer.get_feature_names()
	return features #,feature_names


def filter_text(text):
	filtered = _slugify(text)
	filtered = _get_meaningful_words(filtered)
	return filtered


class Bag(object):
	def __init__(self,texts):
		filtered_texts = map(filter_text,texts)
		self.features = _create_features(filtered_texts) 
		self.num_features = len(self.features[0])
		self.size = len(self.features)
	def __repr__(self):
		return ",".join(self.feature_names)
	def getFeatures(self):
		return self.features	




