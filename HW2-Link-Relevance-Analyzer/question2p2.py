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