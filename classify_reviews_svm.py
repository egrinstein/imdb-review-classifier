import numpy as np
from time import time
from sklearn import svm
from sklearn.externals import joblib
from parse_reviews import toScikitSVM
import pickle
from parse_reviews import Review

def firsts(arr):
    return arr[:-1]
def last(arr):
    return arr[-1]
def compare(val1,val2):
    return val1 == val2

def classify(review,features,classifier):
    freqs = [0]*len(features)
    for word in review.feature_frequency.keys():
        try:
            freqs[features[word]] = review.feature_frequency[word]
        except KeyError:
            continue
    return classifier.predict([freqs])


def main():
    try:
        tf,vf = open("train_bag",'r'),open("validation_bag",'r')
        train,validation = np.load(tf),np.load(vf)
        tf.close()
        vf.close()
    except IOError:
        train,validation = toScikitSVM()
    print validation
    
    
    train_class,valid_class = map(last,train),map(last,validation)
    train_feats,valid_feats = map(firsts,train),map(firsts,validation)
    
    t0 = time()
    print "Started fitting SVM... "
    
    try:
        classifier = joblib.load('svm_model.pickle') 
    except IOError:
        classifier = svm.SVC()
        classifier.fit(train_feats,train_class)
        duration = time() - t0
        print "Time for fitting: "+str(duration)
        t1 = time()
    
        result = classifier.predict(valid_feats)
        duration = time() - t1
        print "Time for predicting: "+str(duration)
        
        matches = np.sum(result == valid_class) 
        
        #print result,matches
        print "Accuracy:"+str(100*matches/len(result))+"%"
        
        duration = time() - t0
        print "Time for fitting: "+str(duration)
        joblib.dump(classifier,"svm_model.pickle")
        
    with open('features.pickle', 'rb') as handle:
        features = pickle.load(handle)
  
    review = Review("review.txt")
    while review:
        cl = classify(review,features,classifier)
        print cl
        if cl[0]:
            print "This is positively positive!!!"
        else:
            print "This is undeniably negative!!!"
        prompt = raw_input("continue?(y/n)")
        if prompt == 'n':
            break
        review = Review("review.txt")

if __name__ == "__main__":
    main()
