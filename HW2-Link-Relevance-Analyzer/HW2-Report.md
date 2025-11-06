# HW 2 
### Bryan Baker
### CS 432, Fall 2025
### September 28th, 2025

## Q1 Data Collection

Download the HTML content of the 500 unique URIs you gathered in HW1 and strip out HTML tags (called "boilerplate") 
so that you are left with the main text content of each webpage. Plan ahead because this will take time to complete.

We just want to save the HTML content. In Python, we can use the requests library to download the webpage.
Once the webpage has been successfully requested, the HTML response content can be accessed using the text property.

You'll need to save the HTML content returned from each URI in a uniquely-named file. The easiest thing is to use the URI itself as the filename,
but your shell will likely not like some of the characters that can occur in URIs (e.g., "?", "&").
My suggestion is to hash the URIs to associate them with their respective filename using a cryptographic hash function, like MD5.

#### Removing HTML Boilerplate

Now use a tool to remove (most) of the HTML markup from your 500 HTML documents. 

The Python boilerpy3 library will do a fair job at this task.  You can use `pip` to install this Python package in your account on the CS Linux machines.  The [main boilerpy3 webpage](https://pypi.org/project/boilerpy3/) has several examples of its usage.

Keep both files for each URI (i.e., raw HTML and processed), and upload both sets of files to your GitHub repo. Put the raw and processed files in separate folders.  Remember that to upload/commit a large number of files to GitHub, [use the command line](https://docs.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository-using-the-command-line).

Sometimes boilerpy3 isn't able to extract any useful information from the downloaded HTML (either it's all boilerplate or it's not actually HTML), so it produces no output, resulting in a 0B size file.  You may also run into HTML files that trigger UnicodeDecode exceptions when using boilerpy3.  You can skip files that have  these types of encoding errors, result in 0B output, or contain inappropriate content (whatever you define as such).  The main goal is to have enough processed files so that you can find 10 documents that contain your query term (for Q2 and later).

*Q: How many of your 500 URIs produced useful text?  If that number was less than 500, did that surprise you?* 


## Answer

To preface, I slightly altered my program in HW1 as to give me a better list of links, and fixed some issues regarding the formatting of links and how it went through each link. 

Noting that, I also used a different seed starting point, being https://en.wikipedia.org/wiki/Donald_Trump, which gave me the list of links found in links.txt in this directory

*question1.py*

```python
import requests 
from bs4 import BeautifulSoup
import sys
from boilerpy3 import extractors
import hashlib

def downloadHTMLContent(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'}
    response = requests.get(url, headers=headers)
    return response

def removeBoilerPlate(response, url, hashUrlDict):

    res = hashlib.md5(url.encode())
    hashedUrl = res.hexdigest()
    extractor = extractors.ArticleExtractor()

    hashUrlDict.update({str(hashedUrl): str(url)})
    soup = BeautifulSoup(response.text, "html.parser")
    #print(res.hexdigest())

    with open(f"./raw-html-files/{hashedUrl}.txt", "a", encoding="utf-8") as outFile:
        outFile.write(str(soup))
        outFile.write('\n')

    with open(f"./processed-html-files/{hashedUrl}.txt", "a", encoding="utf-8") as outFile:
        #print(url)
        content = extractor.get_content(str(soup))
        outFile.write(content)
        outFile.write('\n')
        
    
def mapHashWithURLs(hashUrlDict):
    with open("HashURL-Mappings.txt", "a") as outFile:
        for key, value in hashUrlDict.items():
            outFile.write(f"{key} {value}")
            outFile.write('\n')


def main():
            #url = sys.argv[1]
    hashUrlDict = dict()

    with open("links.txt") as inFile:
        for url in inFile:
            url = url[:-1]
            try:
                response = downloadHTMLContent(url)
                removeBoilerPlate(response, url, hashUrlDict)
            except Exception as e:
                print("oops", e)

    mapHashWithURLs(hashUrlDict)

if __name__ == '__main__':
    main()
```
This program takes in the filename of the text file that HW1 gave as output, being links.txt, downloads the html content of each URL found in the 
links.txt file, then outputs 2 files corresponding to each URL, one file being the raw HTML content of the URL, and the other being the text that were extracted
via the boilerpy3 library. Each kind of file is stored in their own seperate folders, raw-html-files and processed-html-files, as to allow a compressed file name
whiel also avoiding the possibility of an invalid file name being attempted.

The name of each pair of files is the hash of the URL by using the MD5 hash function provided by the hashlib library. The program also outputs
a file which links each URL with their hashed counterpart to allow the the hash to be "unhashed" in a way linking back to the original URL.

Most links produced at least usable text, but there was about 1/5th of files who either produced no text, or a 404 page, and it didn't really surprise me
because of that due to the way that links can lead to content that is either dead or redirected somewhere else.

## Q2 - Rank with TF-IDF

Choose a query term (e.g., "coronavirus") that is not a stop word (e.g, "the"), not super-general (e.g., "web"), and not used in HTML markup (e.g., "http") that is found in at least 10 of your documents.  If the term is present in more than 10 documents, choose any 10 **English-language** documents from *different domains* from the result set.  (Hint: You may want to use the Unix command `grep -c` on the processed files to help identify a good query -- it indicates the number of lines where the query appears.) 

As per the example in the [Searching the Web slides](https://docs.google.com/presentation/d/1xHWYidHcqPljtvqcGsUXgXU7j6KEFDVXrTftHmkv6OA/edit?usp=sharing), compute TF-IDF values for the query term in each of the 10 documents and create a table with the TF, IDF, and TF-IDF values, as well as the corresponding URIs. (If you are using LaTeX, you should create a [LaTeX table](https://www.overleaf.com/learn/latex/tables).  If you are using Markdown, view the raw version of this file for an example of how to generate a table.) Rank the URIs in decreasing order by TF-IDF values.  For example:

Table 1. 10 Hits for the term "shadow", ranked by TF-IDF.

|TF-IDF	|TF	|IDF	|URI
|------:|--:|---:|---
|0.150	|0.014	|10.680	|http://foo.com/
|0.044	|0.008	|10.680	|http://bar.com/

You can use Google or Bing for the DF estimation:
* Google - use **40 billion** as the total size of the corpus
* Bing - use **4 billion** as the total size of the corpus

*These numbers are based on data from <https://www.worldwidewebsize.com>.*

You can use more accurate methods if you'd like, just explain how you did it.  

Don't forget the log base 2 for IDF, and mind your [significant digits](https://en.wikipedia.org/wiki/Significant_figures#Rounding_and_decimal_places).

*You must discuss in your report how you computed the values (especially IDF) and provide the formulas you used for TF, IDF, and TF-IDF.*  

## Answer
I wrote 2 programs to answer this question, one to find out a term that would help in completing this and the next problem, and another to specifically
find the TF-IDF values for each domain of the 10 links that I chose manually from the output of the first program of this question.

*question2.py*
```python
import sys
import string

def mapHashUrl(hashUrlDict):

    with open("HashURL-Mappings.txt") as inFile:
        for line in inFile:
            tempEntry = []
            for word in line.split():
                tempEntry.append(word)
            tempKey = tempEntry[0]
            tempValue = tempEntry[1]

            hashUrlDict.update({tempKey: tempValue})

def countWordsForEachUrl(hashUrlDict, urlWordMatch, wordToFind):

    hits = 0

    with open("findresults.txt", "r", encoding='utf-16') as inFile:
        for line in inFile:
            words = line.split()
            words.insert(1, words[0].split(":")[1])
            words[0] = words[0].split(":")[0][23:-4]

            url = hashUrlDict[words[0]]

            if url not in urlWordMatch:
                urlWordMatch[url] = 0
            
            for word in words:
                if (wordToFind in word.lower()):
                    urlWordMatch[url] += 1
                    hits += 1

    print(f"\nThere were a total of {hits} occurances of the word '{wordToFind}'\n\n")

def main():
    urlWordMatch = dict()
    hashUrlDict = dict()

    mapHashUrl(hashUrlDict)
    countWordsForEachUrl(hashUrlDict, urlWordMatch,sys.argv[1].lower())
    for value, key in urlWordMatch.items():
        print(value, key)
    print('\n')

if __name__ == '__main__':
    main()
```
It's important to note that this program is to be run directly after 

```
findstr /i <targetword> ".\processed-html-files\*.txt" > ".\findresults.txt"
```
meaning the entire execution for this program to work correctly would be
```
findstr /i <targetword> ".\processed-html-files\*.txt" > ".\findresults.txt"; python .\question2.py <targetword>
```
as *question2.py* requires the output that the findstr command gives in order to work correctly.

What this command does is go through each file in the processed-html-files folder and return each line of occurance *targetword* appears in, alongside the
file name from where the line is from. For this problem, *targetword* is "trump"


This program takes in a word for input, and then scans the processed-html-files folder through each file to try to find the total amount of times
that word appears in each file. First, the program uses the HashURL-Mappings.txt to map each hash into the corresponding URL to allow correct
attribution to each hit of the word. It then scans through findresults.txt to count the amount of times the target word appears in each of the documents that
findstr found the occurance of the target word. It does this by splitting each line into a list of words, which are then put lowercase, and then goes through
each word to see if the target word is in the current word. 

It then outputs the total number of occurances the word appeared in the list of processed html files, alongside the source of each hit with the amount of hits in the source.
```
There were a total of 4765 occurances of the word 'trump'


https://www.theguardian.com/info/complaints-and-corrections 1
https://www.theguardian.com/us/technology 1
https://www.businessinsider.com/startups 1
https://cnn.com/2020/09/25/politics/pentagon-election-insurrection-act 26
https://www.npr.org/2024/10/21/nx-s1-5150039/could-trumps-threats-against-news-outlets-carry-weight-if-he-wins-the-presidency 30
https://www.npr.org/2025/03/28/nx-s1-5343474/trump-collective-bargaining-unions-federal-employees 5
https://www.cnn.com/2021/01/06/politics/pro-trump-supporters-dc-protest/index.html 17
...
```
This helped me determine 'trump' is a good target word.


*question2p2.py*
```python
import sys
from urllib.parse import urlparse
import math

def mapHashUrl(hashUrlDict):

    with open("HashURL-Mappings.txt") as inFile:
        for line in inFile:
            tempEntry = []
            for word in line.split():
                tempEntry.append(word)
            tempKey = tempEntry[1]
            tempValue = tempEntry[0]

            hashUrlDict.update({tempKey: tempValue})

def calculateTFIDF(hashUrlDict, wordToFind):
        
        with open("chosenUrls.txt") as inFile:
            for url in inFile:
                wordCount = 0
                hitCount = 0

                if '\n' in url:
                    url = url[:-1]

                with open(f".\\processed-html-files\\{hashUrlDict[url]}.txt", "r", encoding="utf8") as inHtml:
                    for line in inHtml:
                        for word in line.split():
                            wordCount += 1
                            if (wordToFind in word.lower()):
                                hitCount += 1
                
                termFrequency = round(hitCount / wordCount, 3)
                inverseDocFrequency = round(math.log(40000000000/1980000000,2), 3)
                tfidf = round(termFrequency * inverseDocFrequency, 3)
                
                print(f"From the domain {urlparse(url).netloc} | Total Word Count: {wordCount} |  Total Hits: {hitCount} | TF: {termFrequency} | IDF: {inverseDocFrequency} | TF-IDF {tfidf}")

def main():
    hashUrlDict = dict()

    mapHashUrl(hashUrlDict)
    calculateTFIDF(hashUrlDict, sys.argv[1])
    
    print('\n')

if __name__ == '__main__':
    main()
```
To preface this part, I manually picked out the chosen 10 URLs to be used in this part of the question and the next question, and the list is

```
https://www.npr.org/2023/01/25/1146961818/trump-meta-facebook-instagram-ban-ends
https://cnn.com/2020/09/25/politics/pentagon-election-insurrection-act
https://www.nytimes.com/politics/first-draft/2016/05/11/donald-trump-breaks-with-recent-history-by-not-releasing-tax-returns
https://www.bbc.com/news/articles/c62l5zdv7zko
https://usatoday.com/story/tech/2020/10/05/trump-covid-19-coronavirus-disinformation-facebook-twitter-election/3632194001
https://www.theguardian.com/us-news/2023/nov/22/trump-revenge-game-plan-alarm
https://www.forbes.com/sites/andrewsolender/2021/05/03/trump-says-hell-appropriate-the-big-lie-to-refer-to-his-election-loss
https://www.businessinsider.com/timeline-what-trump-was-doing-as-his-mob-attacked-the-capitol-on-jan-6-2022-7
https://www.notus.org/whitehouse/donald-trump-faith-office
https://palmbeachpost.com/story/news/trump/2025/02/20/pastor-paula-white-facts-trumps-head-white-house-faith-office/78604425007
```
This program starts similarly with the previous program, which maps each URL to its hash, to find the file in processed-html-files.
It then goes through each URL in the chosenUrls.txt file to determine which file to go to, and then goes line by line in the file to
analyze each word, maintaining a total word count alongside a total amount of times the target word is present in the document.

I then calculate the term frequency variable with

```termFrequency = round(hitCount / wordCount, 3)``` 

which will round to the 3rd decimal, which will be consistent for the 3 values.

I then calculate the inverse document frequency with

```inverseDocFrequency = round(math.log(40000000000/1980000000,2), 3)```

based on this web search

![\label{fig:Total-Google-Hits}](HW2/donald-trump-query.png)

which gave me the 1,980,000,000 number. Since I used Google, I used 40,000,000,000 as the size of the total corpus as directed by the assignment, which
gave me the IDF number I used in my TF-IDF value, being 

```tfidf = round(termFrequency * inverseDocFrequency, 3)```

The program then takes the domain of the URL provided for each iteration, and then outputs the following

```
From the domain www.npr.org | Total Word Count: 1175 |  Total Hits: 33 | TF: 0.028 | IDF: 4.336 | TF-IDF 0.121
From the domain cnn.com | Total Word Count: 1396 |  Total Hits: 26 | TF: 0.019 | IDF: 4.336 | TF-IDF 0.082
From the domain www.nytimes.com | Total Word Count: 443 |  Total Hits: 10 | TF: 0.023 | IDF: 4.336 | TF-IDF 0.1
From the domain www.bbc.com | Total Word Count: 1003 |  Total Hits: 16 | TF: 0.016 | IDF: 4.336 | TF-IDF 0.069
From the domain usatoday.com | Total Word Count: 377 |  Total Hits: 6 | TF: 0.016 | IDF: 4.336 | TF-IDF 0.069
From the domain www.theguardian.com | Total Word Count: 1699 |  Total Hits: 50 | TF: 0.029 | IDF: 4.336 | TF-IDF 0.126
From the domain www.forbes.com | Total Word Count: 516 |  Total Hits: 10 | TF: 0.019 | IDF: 4.336 | TF-IDF 0.082
From the domain www.businessinsider.com | Total Word Count: 1086 |  Total Hits: 32 | TF: 0.029 | IDF: 4.336 | TF-IDF 0.126
From the domain www.notus.org | Total Word Count: 1717 |  Total Hits: 11 | TF: 0.006 | IDF: 4.336 | TF-IDF 0.026
From the domain palmbeachpost.com | Total Word Count: 630 |  Total Hits: 8 | TF: 0.013 | IDF: 4.336 | TF-IDF 0.056
```

This isn't the table the question asked of, but it helps me to make this table

Table 1. 10 Hits for the term "trump", ranked by TF-IDF.
|TF-IDF	|TF	|IDF	|URI
|------:|--:|---:|---
|0.126	|0.029	|4.336	|www.businessinsider.com
|0.126	|0.029	|4.336	|www.theguardian.com
|0.121	|0.028	|4.336	|www.npr.org
|0.100	|0.023	|4.336	|www.nytimes.com
|0.082	|0.019	|4.336	|www.cnn.com
|0.082	|0.019	|4.336	|www.forbes.com
|0.069	|0.016	|4.336	|www.bbc.com
|0.069	|0.016	|4.336	|www.usatoday.com
|0.056	|0.013	|4.336	|www.palmbeachpost.com
|0.026	|0.006	|4.336	|www.notus.org

# Q3
Now rank the domains of those 10 URIs from Q2 by their PageRank. Use any of the free PR estimators on the web, such as:

  * https://searchenginereports.net/google-pagerank-checker
  * https://dnschecker.org/pagerank.php
  * https://smallseotools.com/google-pagerank-checker/
  * https://www.duplichecker.com/page-rank-checker.php

Note that these work best on domains, not full URIs, so, for example, submit things https://www.cnn.com/ rather than https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21.

If you use these tools, you'll have to do so by hand (most have anti-bot captchas), but there are only 10 to do.

Normalize the values they give you to be from 0 to 1.0. Use the same tool on all 10 (again, consistency is more important than accuracy).

Create a table similar to Table 1:

Table 2. 10 hits for the term "shadow", ranked by PageRank of domain.
|PageRank 	|URI
|----------:|---------:
|0.9 	|http://bar.com/
|0.5 	|http://foo.com/

*Q: Briefly compare and contrast the rankings produced in Q2 and Q3.*

## Answer

I'll be using https://searchenginereports.net/google-pagerank-checker to accomplish this question.

Table 2. 10 Hits for the term "trump", ranked by PageRank.
|PageRank 	|URI
|----------:|---------:
|0.9	|www.nytimes.com
|0.9  |www.cnn.com
|0.9	|www.forbes.com
|0.9	|www.bbc.com
|0.8	|www.businessinsider.com
|0.8	|www.theguardian.com
|0.8	|www.npr.org
|0.8  |www.usatoday.com
|0.6  |www.palmbeachpost.com
|0.5	|www.notus.org

For some reason, my chosen page rank website broke on notus.org, so I opted to use https://dnschecker.org/pagerank.php for that one specifically.

The ranking for these aren't that different from the previous question, however there is a lot more ties in this one compared to the previous one, leading to 4 domains tieing the first spot, with 3 tieing for the second. 
This goes to show that PageRanks has a 'rich-get-richer' phenomenon where the top spots are all selected by big legacy media outlets, ones which have a great influence on their PageRank.

# References

* PageRank Checker, <https://searchenginereports.net/google-pagerank-checker>
* Page Ranking <https://searchenginereports.net/google-pagerank-checker>
* Module-04 Searching, <https://docs.google.com/presentation/d/1xHWYidHcqPljtvqcGsUXgXU7j6KEFDVXrTftHmkv6OA/edit?slide=id.p71#slide=id.p71>
* Extract domain from URL in python - Stack Overflow, <https://stackoverflow.com/questions/44113335/extract-domain-from-url-in-python>
* Python math.log() Method, <https://www.w3schools.com/python/ref_math_log.asp>
* findstr | Microsoft Learn, <https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/findstr>
* Python Dictionaries, <https://www.w3schools.com/python/python_dictionaries.asp>
* python - Convert a list with strings all to lowercase or uppercase - Stack Overflow, <https://stackoverflow.com/questions/1801668/convert-a-list-with-strings-all-to-lowercase-or-uppercase>
* Python open() Function, <https://www.w3schools.com/python/ref_func_open.asp>
* Python String split() Method, <https://www.w3schools.com/python/ref_string_split.asp>
* Python Dictionary update() Method, <https://www.w3schools.com/python/ref_dictionary_update.asp>
* Python program to read file word by word - GeeksforGeeks, <https://www.geeksforgeeks.org/python/python-program-to-read-file-word-by-word/>
* MD5 hash in Python - GeeksforGeeks, <https://www.geeksforgeeks.org/python/md5-hash-python/>
* boilerpy3 · PyPI, <https://pypi.org/project/boilerpy3/>
* Quickstart — Requests 2.32.5 documentation, <https://requests.readthedocs.io/en/latest/user/quickstart/#response-content>
* about_Character_Encoding - PowerShell | Microsoft Learn, <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.5&viewFallbackFrom=powershell-7.1>
