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

def _create_bag(text):
	vectorizer = CountVectorizer(analyzer = "word",   
				 tokenizer = None,    
				 preprocessor = None,
				 stop_words = None,  
				 max_features = 5000) 
	train_data_features = vectorizer.fit_transform(text)
	train_data_features = train_data_features.toarray()
	return train_data_features
class Bag(object):
	def __init__(self,text):
		slug = _slugify(text)
		slug = _get_meaningful_words(slug)		
		self.features = _create_bag(slug)
