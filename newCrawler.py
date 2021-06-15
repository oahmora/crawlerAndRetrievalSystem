import requests
import re
import os
import json


from urllib.parse import urlparse
from urllib import parse
#https://stackoverflow.com/questions/43085744/parsing-robots-txt-in-python
import urllib.robotparser as urobot

import requests 
import urllib.request as urllib2
#https://stackoverflow.com/questions/42441211/python-urllib-error-httperror-http-error-404-not-found
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer

visitedLinks = []
urlQueue = []
pagesCrawled = 0
uniquePagesCrawled = 0
docURLMap = {}		#to map url to document name

####################################
#	Another requirement for the project. Checks urls robot.txt .
####################################
def robot(url):
	#catch 404 errors (perhaps a bit out of place here?). Timeout is there to get around 403 errors
	#update: what, error 999? 403, 404, and 999 errors encountered when set to 100 pages to crawl with ucr.edu as seed
	#!!!In the write up, talk about the errors listed here for the part asking about crawler obstacles
	try:
		#urlopen(url, timeout=10)	#doesn't work for 403
		source = urllib.request.urlopen(url).read()	#this is specifically for error 999
		response = requests.get(url)
		response.raise_for_status()
	except Exception:
		return False
	
	#robots = requests.get(url + '/robots.txt').text
	try:
		robots = urobot.RobotFileParser()
		robots.set_url(url + "/robots.txt")
		robots.read()
		return robots.can_fetch("*", url)
	except Exception:
		return False

####################################		
#	Creates a queue from the seed file. Since urlQueue is global now, will probably merge it somehow
####################################
def createQueue(seedFile):
	inFile = open(seedFile, 'r')
	temp = inFile.read().splitlines()
	queue = []

	for line in temp:
		queue.append(line)
		
	try:
		os.mkdir('html')
		print('Created html folder to store html files.')
	except FileExistsError:
		print('An html folder already exists. Continuing.')
		
	return queue
	
####################################		
#	Crawler Main
####################################
def crawlerMain(seedFile = 'seed.txt', numPages = 10, numHops = 10):
	global urlQueue, pagesCrawled, docURLMap
	urlQueue = createQueue(seedFile)	#urlQueue is a global variable
	print("Crawler will run through " + seedFile + " limited to " + str(numPages) + " pages and " + str(numHops) + " hops.")
	crawler(numPages, numHops)
	
	with open('docURLMap.txt', 'w') as convert_file:
		convert_file.write(json.dumps(docURLMap))
	
####################################
#	crawlNum is the number of pages to crawl, defaults to 10 if not passed to the funciton
#	For testing purposes, just play around with the default. Remaining considations: implicit politeness with time.sleep?
####################################
def crawler(crawlNum, numHops):
	global urlQueue, pagesCrawled, docURLMap, uniquePagesCrawled
	
	if len(urlQueue) <= 0 or crawlNum == 0:
		return
	
	pagesCrawled += 1
	
	url = urlQueue[0]
	if url not in visitedLinks and robot(url):
		visitedLinks.append(url)
	else:
		urlQueue.pop(0)
		crawler(crawlNum, numHops)
		return
		
	#https://realpython.com/python-requests/
	#write the url  so that we can store it as an html file
	#try/exception because of some random error when set to 10 pages
	try:
		r = requests.get(url)
	except Exception:
		urlQueue.pop(0)
		#print('Exception occurred.  Ignore it.')
		crawler(crawlNum, numHops)
		return
	
	#store html file to html file folder (specific project requirement)
	uniquePagesCrawled += 1
	docName = str(uniquePagesCrawled + 10000)
	
	htmltext = requests.get(url).text
	htmlfile = open("./html/" + docName + '.html', "w", encoding="utf-8")
	htmlfile.write(htmltext)
	htmlfile.close()
	
	#create correspondence between document name and url
	docURLMap[docName] = url
	
	#good source: https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
	#crawl the web page to scrape all of the (good) links
	document = urllib2.urlopen(url).read()
	soup = BeautifulSoup(document, 'lxml')
	for line in soup.find_all('a', href=True):
		text = line.get('href')
		text= text.replace("\n", "").replace("\t", "").replace("\r", "")
		#filters out bad links (what seem to be false positives; perhaps just weird links that would need to be inspected more carefullly)
		if (text.startswith("http") or text.startswith("www")) == True:
			if text not in urlQueue:
				urlQueue.append(text)
	
	urlQueue.pop(0)
	crawler(crawlNum - 1, numHops)

	