import re,os,sys,glob,operator
import numpy as np
from parse_text import filter_text

def generate_reviews(folder,classification):
    files = glob.glob(folder+"/*.txt")
    reviews = []
    i=0
    for review in files:
        reviews.append(Review(review,classification))
        i+=1
        if i%1000 == 0:
            print i
    return reviews


class Review:
    word_index = {}
    word_count = {}
    curr_index = 0
    def __init__(self,rev_file,classification):
        "rev_file: path to .txt review. classification:'p'/'n'"
        self.name = re.sub("(.*\/)","",rev_file)
        self.name = self.name.strip(".txt")
        self.classification = classification
        f = open(rev_file,'r')
        raw = f.read()
        self.filtered = filter_text(raw)
        f.close() 	

        words = self.filtered.split()
        self.feature_frequency = {}
        for word in words:
            try:
                self.feature_frequency[word] += 1
            except KeyError:
                self.feature_frequency[word] = 1
            try:
                rpnse = Review.word_index[word]
                Review.word_count[word] += 1	 
            except KeyError:
                Review.word_index[word] = Review.curr_index
                Review.word_count[word] = 1
                Review.curr_index += 1
    
   
    def most_frequent_words(num_words):
        features = sorted(Review.word_count, key=Review.word_count.get, reverse=True)[:num_words]
        features_index = {}
        i=0
        for feature in features:
            features_index[feature] = i
            i+=1
        return features_index
    most_frequent_words = staticmethod(most_frequent_words)
    
    



def generate_arff(reviews,filename,features=None):
	f = open(filename,'w')
	f.write("@relation imdbreviewclassifier\n")
	num_reviews = len(reviews)
	if not features:
		features = Review.most_frequent_words(1000)
	num_features = len(features)
	for feature in features:
		f.write("@attribute "+feature+" NUMERIC\n")
	f.write("@attribute class {p,n}\n")
	f.write("@data\n")
	i = 0
	for review in reviews:	
            i+=1
	    if i%1000 == 0:
		print i
            rev_data = "{"
            for word in review.feature_frequency.keys():
                try:
                    rev_data += str(features[word]) +" "+str(review.feature_frequency[word])+","
                except KeyError:
                    continue
            rev_data += str(num_features)+" "+review.classification+"}\n"
            del review
            f.write(rev_data)
	f.close()
	return features	

def generate_vector(reviews,features=None):
    vect = []
    if not features:
        features = Review.most_frequent_words(1000)
    num_features = len(features)
    print len(features)
    i = 0
    for review in reviews:
        if i%1000 == 0:
            print i
        i+=1
        freqs = [0]*num_features
        for word in review.feature_frequency.keys():
            try:
                freqs[features[word]] = review.feature_frequency[word]
            except KeyError:
                continue
        if review.classification == 'p':
            freqs.append(1)
        else:
            freqs.append(0)
        vect.append(freqs)
    return vect,features


    
    
def toWeka():
    working_folder = os.getcwd()+"/movie_review_dataset/"
    train_reviews = generate_reviews(working_folder+"part1/neg",'n')
    train_reviews += generate_reviews(working_folder+"part1/pos",'p')
    
    features_used = generate_arff(train_reviews,"train.arff")	
    train_reviews = None
    validation_reviews = generate_reviews(working_folder+"part2/neg",'n')
    validation_reviews += generate_reviews(working_folder+"part2/pos",'p')
	
    generate_arff(validation_reviews,"validation.arff",features_used)
    
    
def toScikitSVM(gen_train=True,gen_valid=True):
    working_folder = os.getcwd()+"/movie_review_dataset/"
    
    if gen_train:
        train_reviews = generate_reviews(working_folder+"part1/neg",'n')
        train_reviews += generate_reviews(working_folder+"part1/pos",'p')
        print("generated train reviews")
        train,features_used = generate_vector(train_reviews)	
        train_reviews = None
        print train
    if gen_valid:
        validation_reviews = generate_reviews(working_folder+"part2/neg",'n')
        tmp = generate_reviews(working_folder+"part2/pos",'p')
        validation_reviews += tmp
    
        validation,features_used = generate_vector(validation_reviews,features_used)
        print "validation:",validation
    
    if gen_train:
        tf = open("train_bag",'w')
        train = np.array(train)
        np.save(tf,train)
        np.save(tf,train)
    if gen_valid:
        vf = open("validation_bag",'w')
        validation = np.array(validation)
        np.save(vf,validation)
        vf.close()
    
    return train,validation
    
    
#a,b = toScikitSVM()
#print a,b

if __name__ == "__main__":
    toScikitSVM()
    
   
		
