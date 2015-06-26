import re,os,sys,glob
from bag_of_words import Bag,filter_text

# Definitions
#MAX_FEATURES = 500
#MAX_REVIEWS = 500


def dbg(thing):
	print thing,type(thing),len(thing)

def generate_arff(bag,reviews,filename):
	f = open(filename,'w')
	f.write("@relation imdbreviewclassifier\n")
	for i in range(bag.num_features):
		f.write("@attribute "+str(i)+" {0,1}\n")
	f.write("@attribute class {p,n}\n")
	f.write("@data")
	for j in range(bag.size):		
		rev_data = "{"
		if j%1000 == 0:
			print j*bag.num_features
		for i in range(bag.num_features):
			if bag.features[j][i] != 0:
				rev_data = rev_data + str(i) +" 1, "
		rev_data+= "class "+bag.num_features+"}\n"
		reviews[j] = None
		f.write(rev_data)
	f.close()
		
				


class Review:
	def __init__(self,rev_file,classification):
		"rev_file: path to .txt review. classification:'p'/'n'"
		self.name = re.sub("(.*\/)","",rev_file)
		self.name = self.name.strip(".txt")
		self.classification = classification
		f = open(rev_file,'r')
		raw = f.read()
		self.filtered = filter_text(raw)
		f.close() 	

if __name__== "__main__":
	if len(sys.argv) != 2:
		print """Usage: $main.py /reviews/folder/\n """	
		sys.exit("Wrong number of parameters")
	else:
		working_folder = sys.argv[1]
		if working_folder[-1] != '/':
			working_folder = working_folder + '/'
			#windows=\

	neg_reviews_path = song_files = glob.glob(working_folder+"part1/neg/*.txt")
	pos_reviews_path = song_files = glob.glob(working_folder+"part1/pos/*.txt")
	reviews = []	
	num_neg_reviews = len(neg_reviews_path)
	for i in range(num_neg_reviews):
		if i%1000 == 0:
			print i
		reviews.append(Review(neg_reviews_path[i],'n'))
	num_pos_reviews = len(pos_reviews_path)
	for j in range(num_pos_reviews):
		if (i+j)%1000 == 0:
			print i+j
		reviews.append(Review(pos_reviews_path[j],'p'))
	neg_reviews_path = pos_reviews_path = None
	bag_of_reviews = []
	for review in reviews:
		bag_of_reviews.append(review.filtered)
		del review
	print "creating bag of words...\n"
	bag_of_reviews = Bag(bag_of_reviews) 
	print "...bag of words created\n"
	generate_arff(bag_of_reviews,reviews,"imdb.arff")	
			

