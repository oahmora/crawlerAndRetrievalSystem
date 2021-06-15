from retrievalSystem import parseHTMLfiles, retrievalMain
from newCrawler import crawlerMain
import sys

#####################################
#  Main
#####################################
if __name__ == "__main__":
	#input: crawl <seed-file> <number-of-pages> <number-of-hops>
	#number of hops is distance from main page. Check how many '/' the link has for an indication of number of hops.
	if(len(sys.argv) >= 2):
		if(sys.argv[1] == 'crawl'):
			if(len(sys.argv) == 4 or len(sys.argv) == 5):
				seedFile = sys.argv[2]
				numPages = int(sys.argv[3])
				numHops = int(sys.argv[4])
				
				print("Running crawler on provided arguments...")
				crawlerMain(seedFile, numPages, numHops)
				parseHTMLfiles()	#create index
				
			else:	#run on default arguments 
				print("Running crawler on default arguments...")
				crawlerMain()
				parseHTMLfiles()	#create index
				
		if(sys.argv[1] == 'index'):
			parseHTMLfiles()
				
		if(sys.argv[1] == 'retrieve'):
			if (len(sys.argv) == 2):
				term = 'medicine'
				retrievalMain(term)
			else:
				term = sys.argv[2]
				retrievalMain(term)
	else:
		print("Please provide additional arguments.")