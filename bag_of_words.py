import collections,re
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer


def _slugify(text):
	"Removes html tags,punctuation and puts everything in lowercase"
	slug = BeautifulSoup(text).get_text()
	slug = re.sub("[^a-zA-Z]", " ", slug )  
	slug = slug.lower()
	return slug

def _get_meaningful_words(text):
	"removes stopwords from a slugged text"
	words = text.split()
	stopwords_set = set(nltk.corpus.stopwords.words("english"))
	words = [w for w in words if not w in stopwords_set]
	return( " ".join( words ))

def _create_features(texts):
	vectorizer = CountVectorizer(analyzer = "word",   
				 tokenizer = None,    
				 preprocessor = None,
				 stop_words = None,  
				 max_features = 500) 
	train_data_features = vectorizer.fit_transform(texts)
	train_data_features = train_data_features.toarray()
	return train_data_features


def filter_text(text):
	filtered = _slugify(text)
	filtered = _get_meaningful_words(filtered)
	return filtered


class Bag(object):
	def __init__(self,texts):
		filtered_texts = map(filter_text,texts)
		self.features = _create_features(filtered_texts)
		print self.features	
