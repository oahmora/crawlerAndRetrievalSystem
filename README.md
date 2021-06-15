## Team member 1 - Steven Joseph
## Team member 2 - Omar Hernandez 
## Team member 3 - Hridya Antony

- Python was used for this project.
- To deploy the crawler, enter: python3 main.py crawl
- The crawler can also run on additional command line arguments: python3 main.py crawl <name of seed file> <number of pages to crawl> < number of hops>
- To index the documents, enter: python3 main.py index
- To retrieve information about a term, enter: python3 main.py retrieve <word>


Example commands:
```bash python3 main.py crawl seed.txt 50 10```
```bash python3 main.py index```
```bash python3 main.py retrieve music```

## Contributions
- Steven Joseph: Part 2 bugfix, part 3 code
- Omar Hernandez: Part 1 code, part 2 code, part 3 bugfix
- Hridya Antony: Video demonstration, troubleshooting

## Project Details
- Part a - Architecture, Data Collection, and Data Strucutures.
- This crawler follows the basic architecture of a web crawler. The program begins by accessing the seed file (seed.txt) to grab the URL of the website we want to crawl.
The program then adds the URL to a queue and checks whether it has visited the URL and whether it is allowed or not based on robots.txt. If the URL is new, the program proceeds to extract the HTML and writes it to a file (under the html folder).
It then proceeds to parse the HTML document to extract all of the website's links, adding them to the queue. If the URL has been visited before, they are removed from the queue and then the program proceeds to the next element of the queue.
- Part b - Limitations
- The only big limitation is that the program isn't able to address website depth. There's also possibilities that some links are filtered out from the measures taken to avoid spider traps and other crawling pitfalls. Another limitation seems to be that duplicate results are in the ranking: it might be an issue with the indexing.

## Extended Details
- Our code is designed by a crawler that makes use of beautifulsoup, and crawls and parses multiple sites as it goes over the specifications.
- The program indexes the documents and loads them into files, and stores them in an  html folder.
- A search can also be done to look up words from within the documents, and see what documents contain which word.
- It also displays how many documents hold that word.
- For example, at 20 documents, if you type in University, I recieveced 10 responses.
- To run this program, make sure that ther is no html folder already  present in the directory, open cmd prompt, preferably on windows(unsure  if it will work elsewhere.), and navigate to the file path for this project.
- The crawler can also take additional arguments: python3 <name-of-the-file> <seed-file> <number-of-pages> <number-of-hops>
- Let the program crawl and scrape the data from 20 sites, starting from the seedFile.
- Upon completion, enter a word to search in the elasticsearch indexed files, and watch as it searches and returns the files with that word, if any exist,and rates them accoding to elasticsearch. 
- The program ends on it's own as this finishes.
