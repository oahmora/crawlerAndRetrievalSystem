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

###################################
#  Parse stored HTML files and add info from tags using BeautifulSoup
#  (Retrieves title for now for testing purposes)
#  Only prints out list of retrieved info for now.
###################################
from datetime import datetime
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

elastic_pass = "30eR6drsZhFpZPWMLOFC6JMW"
elastic_endpoint = "i-o-optimized-deployment-eb5ff4.es.eastus2.azure.elastic-cloud.com:9243"
cloudID = "i-o-optimized-deployment:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvJDUxZWQzMWJlNzhjZjQ3ZjBhNGU3YjFiODYyZTlmNWVhJDgxMzk1NWM4ZTM5MzRhMmViYTc2YTBkNTVjYzY2MzBj"
connection_string = "https://elastic:" + elastic_pass + "@" + elastic_endpoint
#curl -u elastic:30eR6drsZhFpZPWMLOFC6JMW
indexName = "cs172-index"
esConn = Elasticsearch(cloud_id = cloudID, http_auth=("elastic", "30eR6drsZhFpZPWMLOFC6JMW"))
response = esConn.indices.create(index=indexName, ignore=400) #create index

#####################################
#	Retrieval Main
#####################################
def retrievalMain(term):
	global response
	response = readDictFile('docIndex.txt')
	
	retrieveTerm(response, term)

#####################################
#	Parse HTML files in folder.
#####################################
def parseHTMLfiles():
	global response
	
	# Retrieve the names of all files to be indexed in folder
	for dir_path, dir_names, file_names in os.walk("html"):
		allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

	docURLMap = readDictFile('docURLMap.txt')
	
	existingURLs = []
	for file in allfiles:
		inFile = open(file, 'r', encoding='utf-8')
		
		soup = BeautifulSoup(inFile,'html.parser')
		inFile.close()
		
		docName = re.sub("[^0-9]", "", file)
		if docName not in docURLMap:
			continue
		
		url = docURLMap[docName]
		#print(url)
		parsedURL = re.sub(r'[^\w]', ' ', url)
		if parsedURL in existingURLs:
			continue
		existingURLs.append(parsedURL)
		
		tag = soup.title
		tag2 = soup.body
		
		doc = {
			'url': url, # url
			'page_title': tagFind(tag), # extract webpage name
			'text': tagFind(tag2), # html body text
			'timestamp': datetime.now(), # date
		}
		
		response = esConn.index(index="cs172-index", id=id, body=doc) # add doc to index
	print("Documents indexed.")
	
	with open('docIndex.txt', 'w') as convert_file:
		convert_file.write(json.dumps(response))

#####################################
#	Retrieve term from response
#####################################
def retrieveTerm(response, term):
	#search for the word 'medicine'
	val = term
	search = {
		'query':{
			'match':{
				"text":val
				}
			}
		}
	response = esConn.search(index=indexName, body={"query": {"match_all": {}}})
	response = esConn.search(index=indexName, body = search)
	#response = esConn.search(index="cs172-index", body=search)
	response_h = response["hits"]["hits"]
	#print(response_h)
	#for num, doc in enumerate(response_h):
		
		#doc['url'] = docURLMap[docName]
	#print("Instances of '" + term + "' in document corpus: " + str(len(response_h)))
		#print('\n', num, '--', doc)
	if(len(response_h)==0):
		print("No results have been found.")
		return
		
	print("Top " + str(len(response_h)) + " results for term '" + term + "':")
	
	urlList = []	#so that we can check if top search is in same url
	for i in range(len(response_h)):
		print('\nDocument Rank ' + str(i + 1))
		print('Title: ' + str(response_h[i]['_source']['page_title']))
		print('ID: ' + response_h[i]['_id'])
		print('Score: ' + str(response_h[i]['_score']))
		print('URL: ' + response_h[i]['_source']['url'])
		print('Date Accessed: ' + response_h[i]['_source']['timestamp'])
	
	
#####################################
#	Read docURLMap from file
#####################################
def readDictFile(file):
	with open(file) as inFile:
		data = inFile.read()
	
	dict = json.loads(data)
	return dict
	
#####################################
#  Find all corresponding tags
#####################################
def tagFind(tag):
	list = []
	if tag is None:
		return
	else:
		for string in tag.stripped_strings:
			if not string.isspace():
				list.append(string)	
		
		string = ''
		for element in list: 
			string = string + ' ' + element  
		
		return string
