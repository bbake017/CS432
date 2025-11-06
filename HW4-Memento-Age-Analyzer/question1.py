import tarfile
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

def mapHashUrl(hashUrlDict):
    with open("..\\HW3\\HashURL-Mappings.txt") as inFile:
        for line in inFile:
            tempEntry = []
            for word in line.split():
                tempEntry.append(word)
            tempKey = tempEntry[0]
            tempValue = tempEntry[1]
            hashUrlDict.update({tempKey: tempValue})

def countMementos(hashUrlDict, urlMementoDict, mementoEarliest):
    
    for key, value in hashUrlDict.items():
        tar = tarfile.open(f"..\\HW3\\mementos\\{key}.tar")
        for member in tar.getmembers():
            try:
                inJSON = tar.extractfile(member)
                currentMemento = json.load(inJSON)
                urlMementoDict.update({currentMemento["original_uri"] : len(currentMemento["mementos"]["list"])})

                earliest = currentMemento["mementos"]["first"]["datetime"]
                earliestDateTime = datetime.datetime(int(earliest[0:4]), int(earliest[5:7]), int(earliest[8:10]), int(earliest[11:13]), int(earliest[14:16]), int(earliest[17:19]))

                mementoEarliest.update({currentMemento["original_uri"] : earliestDateTime})
            except Exception as e:
                continue
        tar.close()

def plotMementoDate(urlMementoDict, sortedMementos):
    collectionDate = datetime.datetime(2025, 10, 17, 14)
    x = []
    y = []
    lessThanWeekOld = 0
    for key, value in sortedMementos.items():
        age = collectionDate - value
        if age.days < 7: 
            lessThanWeekOld += 1
        x.append(age.days)
        y.append(urlMementoDict[key])
    
    print(f"The URI-R that has the oldest memento of the {len(urlMementoDict)} collected is '{list(sortedMementos)[0]}'")
    print(f"Out of {len(urlMementoDict)} URI-Rs, {lessThanWeekOld} had an age of less than a week old from the day of collection.")

    plt.scatter(x, y)
    plt.show()

def main():
    hashUrlDict = dict()
    urlMementoDict = dict()
    mementoEarliest = dict()
    mapHashUrl(hashUrlDict)
    countMementos(hashUrlDict, urlMementoDict, mementoEarliest)

    sortedMementos = dict(sorted(mementoEarliest.items(), key=lambda item: item[1]))

    plotMementoDate(urlMementoDict, sortedMementos)

if __name__ == '__main__':
    main()