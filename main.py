import re,os,sys,glob
from bag_of_words import Bag,filter_text

class Review:
	def __init__(self,rev_file):
		self.name = re.sub("(.*\/)","",rev_file)
		self.name = self.name.strip(".txt")
		f = open(rev_file,'r')
		self.raw = f.read()
		self.filtered = filter_text(self.raw)
		f.close() 	

if __name__== "__main__":
	if len(sys.argv) != 3:
		print """Usage: $main.py /reviews/folder/ ALGORITHM\n """	
		sys.exit("Wrong number of parameters")
	else:
		working_folder = sys.argv[1]
		if working_folder[-1] != '/':
			working_folder = working_folder + '/'
			#windows=\

	neg_reviews_path = song_files = glob.glob(working_folder+"part1/neg/*.txt")
	pos_reviews = song_files = glob.glob(working_folder+"part1/pos/*.txt")
	neg_reviews = []	
	num_reviews = len(neg_reviews_path)
	for i in range(num_reviews):
		if i%1000 == 0:
			print i
		neg_reviews.append(Review(neg_reviews_path[i]))

	bag_of_reviews = []
	for review in neg_reviews:
		bag_of_reviews.append(review.filtered)
	bag_of_reviews = Bag(bag_of_reviews) 
		

	
		
