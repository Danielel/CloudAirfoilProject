import json
import os

def readJsonDataFile():
    strCheckList = ["han", "hon", "den", "det", "denna", "denne", "hen"]

    try:
        FileNotFoundError
    except NameError:
        #py2
        FileNotFoundError = IOError
    
    #try:
    #    with open("tweetData.json", "r" ) as file:
    #        strCountDict = json.loads(file.read())
    #except FileNotFoundError:
    #    strCountDict = {"uniqueTweets" : 0, "han" : 0, "hon" : 0, "den" : 0, "det" : 0, "denna" : 0, "denne" : 0, "hen" : 0}
    strCountDict = {"uniqueTweets" : 0, "han" : 0, "hon" : 0, "den" : 0, "det" : 0, "denna" : 0, "denne" : 0, "hen" : 0}

    for fileName in os.listdir(os.getcwd() + "/../data"):
        with open("../data/" + fileName, "r" ) as file:
            for line in file:
                try:
                    jsonObject = json.loads(line)
                except ValueError:
                    continue
                if('retweeted_status' not in jsonObject):
                    strCountDict['uniqueTweets'] += 1
                    stringToSearch = jsonObject['text'].split()
                    for str in strCheckList:
                        strCountDict[str] += stringToSearch.count(str)
        #break

    jsonDump = json.dumps(strCountDict, sort_keys=True, indent=4)

    #print(jsonDump)
    #with open("tweetData.json", "w") as jsonFile:
    #    jsonFile.write(jsonDump)
        
    return jsonDump