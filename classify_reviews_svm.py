import numpy as np
from time import time
from sklearn import svm
from parse_reviews import toScikitSVM
import parse_text as parse_text


def firsts(arr):
    return arr[:-1]
def last(arr):
    return arr[-1]
def compare(val1,val2):
    return val1 == val2

def main():
    try:
        tf,vf = open("train_bag",'r'),open("validation_bag",'r')
        train,validation = np.load(tf),np.load(vf)
        tf.close()
        vf.close()
    except IOError:
        train,validation = toScikitSVM()
    #print validation
    
    #pega a classificacao (ultimo elemento de cada vetor)
    train_class,valid_class = map(last,train),map(last,validation)
    train_feats,valid_feats = map(firsts,train),map(firsts,validation)
    
    t0 = time()
    print "Started fitting SVM... "
    
    classifier = svm.SVC()
    classifier.fit(train_feats,train_class)
    
    #print valid_class
    
    result = classifier.predict(valid_feats)
    #print "oi mae"
    matches = np.sum(result == valid_class) 
    
    #print result,matches
    print "Accuracy:"+str(100*matches/len(result))+"%"
    
    duration = time() - t0
    print "Time for fitting: "+str(duration)

    strReview = "This movie is very good. I like it."
    #Quando for fazer o while mudar a linha acima para strReview = ""
    #while strReview != '0':
    
    strParsed = parse_text.filter_text(strReview)

    vectFeats = []
    #for feat in strParsed:
        #fazer o match de palavras com as features

    result = classifier.predict(vectFeats)
    if result == valid_class:
        print 'Review positivo'
    else:
        print 'Review negativo'



if __name__ == "__main__":
    main()
