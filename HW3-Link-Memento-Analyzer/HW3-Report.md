# HW 3
### Bryan Baker
### CS 432, Fall 2025
### October 19th, 2025

# Q1 - Get TimeMaps for each URI

Obtain the [TimeMaps](http://www.mementoweb.org/guide/quick-intro/) for each of the unique URIs you collected in HW1 using the [MemGator Memento Aggregator](https://github.com/oduwsdl/MemGator).  

*Do **not** use memgator.cs.odu.edu this assignment. You must download and install a local version of MemGator.*

Here's an example:

`./memgator-darwin-amd64 -c "ODU CS432/532 YOUR_EMAIL_ADDRESS" -a https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json -F 2 -f JSON https://www.cs.odu.edu/~mweigle/ > mweigle-tm.json`

If you uncover TimeMaps that are very large (e.g., for popular sites like <https://www.cnn.com/>) and swamp your filesystem, you have two options:
* Manually remove those URI-Rs from your dataset (but note this in your report), or
* Compress each TimeMap file individually (using pipe to `gzip` in the same command when downloading or after the download is completed). These compressed files can be used for further analysis by decompressing on the fly using commands like `zcat` or `zless` (or using gzip libraries in Python).

## Answer

To tackle this section of the homework, I opted to use a windows batch file in order to repeatably call memgator with each different url, and then outputting a JSON file that's zipped in a .tar file to compress to maintain space for the larger files.
It's a simple file:

```
@echo off

for /F "tokens=1-2 delims= " %%A in (.\HashURL-Mappings.txt) do (

.\memgator-windows-amd64.exe -c "ODU CS432/532 bbake017@odu.edu" -a https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json -F 2 -f JSON %%B > .\mementos\%%A.json
tar -c -f .\mementos\%%A.tar .\mementos\%%A.json
del .\mementos\%%A.json
TIMEOUT /T 10 /NOBREAK
)
```

This script has a for loop that iterates through every line in the HashURL-Mappings.txt which gives the program the URL and the hash associated with the URL to name the output. In the loop body, the script calls the
memgator command which downloads the various time maps of each URL that are present in the list of archives that are found in 

`https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json`

After it downloads them, it outputs the data onto a JSON file that is named after the URL's hashed form, which allows all the URLs to be used as unique filenames, and then sends the file to a compressed .tar file, finally
deleting the original file. After this, the program waits 10 seconds before it iterates to the next loop as to prevent potential spam issues. All of the output is kept in a seperate folder 'mementos.'

# Q2 - Analyze Mementos Per URI-R.

Use the TimeMaps you saved in Q1 to analyze how well the URIs you collected in HW1 are archived.

Create a table showing how many URI-Rs have certain number of mementos.  For example

|Mementos | URI-Rs |
|---------:|--------:|
|   0     |  250   |
|   1     |  100   |
|   7     |   50   |
|   12     |   25   |
|   19     |   25   |
|   24     |  20  |
|   30     |   27   |
|  57     |    3   |

*Q: What URI-Rs had the most mementos?  Did that surprise you?*

## Answer

For this question, I wrote this program in python found in `question2.py`

```python
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
```

I originally sorted out the URLs by their total amount of mementos as to find what I feel would be good ranges to use, which has 
been commented out.

This program firstly maps URLs to their hashes in a dict which then uses that to open each tar file in the mementos directory and count each memento according to each URL in another dict. Finally, a last dict is
used to count the amount of URLs that are in specific ranges (20000, 10000, 5000, ...) and print out the tables that show how many URLs are in each range, as well as printing out the URLs that are in the highest range.

Output
```
>= 20000 10
19999 - 10000 36
9999 - 5000 36
4999 - 2500 30
2499 - 1000 25
999 - 500 35
499 - 250 33
249 - 100 71
99 - 50 50
49 - 25 29
24 - 10 46
< 10 19
N/A 81
The URLs that have are 20000 or greater are:
https://www.businessinsider.com/politics
https://adsrvr.org
https://markets.businessinsider.com
https://www.businessinsider.com/privacy-policy
https://www.forbes.com/billionaires
https://www.theguardian.com
https://www.businessinsider.com.pl/?IR=C
https://www.businessinsider.com/terms
https://www.businessinsider.com
https://www.theguardian.com/world
```

Which shows that the URLs that had the most mementos were
* https://www.businessinsider.com/politics
* https://adsrvr.org
* https://markets.businessinsider.com
* https://www.businessinsider.com/privacy-policy
* https://www.forbes.com/billionaires
* https://www.theguardian.com
* https://www.businessinsider.com.pl/?IR=C
* https://www.businessinsider.com/terms
* https://www.businessinsider.com
* https://www.theguardian.com/world

The table below shows the various groupings of each range with the amount of URLs present.

|# of Mementos|# of URLs|
|:---|:---|
|>= 20000|10|
|19999 - 10000|36|
|9999 - 5000|36|
|4999 - 2500|30|
|2499 - 1000|25|
|999 - 500|35|
|499 - 250|33|
|249 - 100|71|
|99 - 50|50|
|49 - 25|29|
|24 - 10|46|
|< 10|19|
|N/A|81|

For the category N/A, I'm unsure whether or not it failed to return anything because of there not being any mementos, or any other kind of jank that may have happened when acquiring the mementos, so I grouped both of them together.


# References

*Every report must list the references that you consulted while completing the assignment. If you consulted a webpage, you must include the URL.  These are just a couple examples.*

* Python - Change Dictionary Items, <https://www.w3schools.com/python/python_dictionaries_change.asp>
* Sorting a Python Dictionary: Values, Keys, and More – Real Python, <https://realpython.com/sort-python-dictionary/>
* How to Get Count of JSON Array elements in Python, <https://likegeeks.com/count-json-array-elements-python/>
* oduwsdl/MemGator: A Memento Aggregator CLI and Server in Go, <https://github.com/oduwsdl/MemGator>
* How do you loop through each line in a text file using a windows batch file? - Stack Overflow, <https://stackoverflow.com/questions/155932/how-do-you-loop-through-each-line-in-a-text-file-using-a-windows-batch-file>
* reading tar file contents without untarring it, in python script - Stack Overflow, <https://stackoverflow.com/questions/2018512/reading-tar-file-contents-without-untarring-it-in-python-script>
* How can I run the "tar -czf" command in Windows? - Super User, <https://superuser.com/questions/244703/how-can-i-run-the-tar-czf-command-in-windows>
