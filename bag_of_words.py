import collections,re
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

#definitions
MAX_WORDS = 5000


def _slugify(text):
	"Removes html tags,punctuation and puts everything in lowercase"
	slug = BeautifulSoup(text).get_text()
	slug = re.sub("[^a-zA-Z]", " ", slug )  
	slug = slug.lower()
	return slug

def _remove_stopwords(text):
	"Removes stopwords from slugified text"
	stops = set(stopwords.words("english"))
	meaningful_words = [w for w in text if not w in stops] 
	return( " ".join( meaningful_words )) 

def _create_features(text):
	vectorizer = CountVectorizer(analyzer = "word",
			                 tokenizer = None,   
                             preprocessor = None,
                             stop_words = None,  
                             max_features = MAX_WORDS)  
	
	features = vectorizer.fit_transform(clean_train_reviews)
	features = train_data_features.toarray()
	return features 

class Bag(object):
	def __init__(self,text):
		self.raw = text
		slug = _slugify(text)
		self.features = _remove_stopwords(slug)
		self.features = _create_features(self.features)

	def features(self):
		return self.features


		
