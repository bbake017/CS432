import tarfile
import json

def mapHashUrl(hashUrlDict):
    with open("HashURL-Mappings.txt") as inFile:
        for line in inFile:
            tempEntry = []
            for word in line.split():
                tempEntry.append(word)
            tempKey = tempEntry[0]
            tempValue = tempEntry[1]
            hashUrlDict.update({tempKey: tempValue})

def countMementos(hashUrlDict, urlMementoDict, NAMementoUrls):
    
    for key, value in hashUrlDict.items():
        tar = tarfile.open(f".\\mementos\\{key}.tar")
        for member in tar.getmembers():
            try:
                inJSON = tar.extractfile(member)
                currentMemento = json.load(inJSON)
                urlMementoDict.update({currentMemento["original_uri"] : len(currentMemento["mementos"]["list"])})
            except Exception as e:
                NAMementoUrls.update({value : "N/A"})
                #print(e)
        tar.close()

def groupAndPrintAmounts (urlMememntoDict, NAMementoUrls):
    amounts = { ">= 20000": 0,
                "19999 - 10000" : 0,
                "9999 - 5000" : 0,
                "4999 - 2500" : 0,
                "2499 - 1000" : 0,
                "999 - 500" : 0,
                "499 - 250" : 0,
                "249 - 100" : 0,
                "99 - 50" : 0,
                "49 - 25" : 0,
                "24 - 10" : 0,
                "< 10" : 0,
                "N/A": len(NAMementoUrls)}
    for key, value in urlMememntoDict.items():
        if value >= 20000:
            amounts[">= 20000"] += 1
        elif 20000 > value >= 10000:
            amounts["19999 - 10000"] += 1
        elif 10000 > value >= 5000:
            amounts["9999 - 5000"] += 1
        elif 5000 > value >= 2500:
            amounts["4999 - 2500"] += 1
        elif 2500 > value >= 1000:
            amounts["2499 - 1000"] += 1
        elif 1000 > value >= 500:
            amounts["999 - 500"] += 1
        elif 500 > value >= 250:
            amounts["499 - 250"] += 1
        elif 250 > value >= 100:
            amounts["249 - 100"] += 1
        elif 100 > value >= 50:
            amounts["99 - 50"] += 1
        elif 50 > value >= 25:
            amounts["49 - 25"] += 1
        elif 25 > value >= 10:
            amounts["24 - 10"] += 1
        elif 10 > value:
            amounts["< 10"] += 1
    

    for key, value in amounts.items():
        print(key, value)

    print("The URLs that have are 20000 or greater are: ")
    for key, value in urlMememntoDict.items():
        if value >= 20000:
            print(key)
    

def main():
    hashUrlDict = dict()
    urlMementoDict = dict()
    NAMementoUrls = dict()
    mapHashUrl(hashUrlDict)
    countMementos(hashUrlDict, urlMementoDict, NAMementoUrls)
    groupAndPrintAmounts(urlMementoDict, NAMementoUrls)

    #sortedMementos = dict(sorted(urlMementoDict.items(), key=lambda item: item[1]))

    #for key, value in sortedMementos.items():
    #    print(key, value)
    #for key, value in NAMementoUrls.items():
    #    print(key, value)

    

if __name__ == '__main__':
    main()