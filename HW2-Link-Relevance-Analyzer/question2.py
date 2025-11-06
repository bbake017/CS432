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