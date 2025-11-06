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