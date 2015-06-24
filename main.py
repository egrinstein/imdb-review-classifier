import re,os,sys,glob
from bag_of_words import Bag

class Review:
	def __init__(self,rev_file):
		self.name = re.sub("(.*\/)","",rev_file)
		self.name = self.name.strip(".txt")
		f = open(rev_file,'r')
		self.raw = f.read()
		self.bag = Bag(self.raw)
		f.close() 	

if __name__== "__main__":
	if len(sys.argv) != 3:
		print """Usage: $main.py /reviews/folder/ ALGORITHM\n """	
		sys.exit("Wrong number of parameters")
	else:
		working_folder = sys.argv[1]
	
	neg_reviews = song_files = glob.glob(working_folder+"part1/neg/*.txt")
	pos_reviews = song_files = glob.glob(working_folder+"part1/pos")

	a = Review(neg_reviews[0])	

	print a.raw 
	
		
