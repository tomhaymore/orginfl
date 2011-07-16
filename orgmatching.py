from decimal import *
import csv
import database
import re
from preprocess import returnNormalizedString

orgsToNormDict = {}
tokenOrgDict = {}

"""def preparePreprocessOrgList():
    preprocessWriter = csv.writer(open('preprocess_org_list.csv', 'wb'))
    preprocessWriter.writerow(["org_name"])
    orgDictReader = csv.DictReader(open('raw_org_list.csv', 'rU'))
    for eachDict in orgDictReader:
		for k, v in eachDict.items():
			if k == "org_name":
			    value = returnNormalizedString(v)
			    preprocessWriter.writerow([value])"""
			    
def preparePreprocessMap():
    preprocessWriter = csv.writer(open('preprocess_org_dict.csv', 'wb'))
    preprocessWriter.writerow(["previous", "processed"])
    for i in range(14): #14
        date = 1997 + i
        csvName = 'FACAMemberList%(date)d' % {'date':date}
        facaDictReader = csv.DictReader(open(csvName +'.csv', 'rU'))		
        for eachDictToBeMapped in facaDictReader:
            for k,v in eachDictToBeMapped.items():
                oldValue = v
                if k == "OccupationOrAffiliation":
                    newValue=returnNormalizedString(v) #Regular Expressions
                    preprocessWriter.writerow([oldValue, newValue])

def createPreprocessMap(): #Dictionary mapping KEY: Unclean org name | Value: Preprocessed org name
    #Execute after Preparing
    preprocessDict = {}
    preprocessDictReader = csv.DictReader(open('preprocess_org_dict.csv', 'rU'))
    for each in preprocessDictReader:
        preprocessDict[each["previous"]] = each["processed"]
    return preprocessDict
    #Prepare Everytime We Add a RegEx

def createTokenMap(): # Dictionary mapping KEY: Tokenized words | VALUE: Preprocessed, Unnormalized org name
    tokenToOrgDict = {}
    preprocessDict = createPreprocessMap()
    for i in range(14): #14
        date = 1997 + i
        csvName = 'FACAMemberList%(date)d' % {'date':date}
        facaDictReader = csv.DictReader(open(csvName +'.csv', 'rU'))		
        for eachDictToBeMapped in facaDictReader:
            v = eachDictToBeMapped["OccupationOrAffiliation"]
            value = preprocessDict[v] #Get Preprocessed Value
            value = value.upper()
            orgTokenSet = set(value.split(" ")) #Tokenize
            for token in orgTokenSet:
                if token not in tokenToOrgDict:
                    newSet = set([])
                    tokenToOrgDict[token] = newSet
                tokenToOrgDict[token].add(value) #Add the unnormalized organized name
    print "Size of Token to Org Dict: %(size)d" % {"size":len(tokenToOrgDict)}
    print "Num of Total Orgs: %d" % len(preprocessDict)
    return tokenToOrgDict
	
def intersectAndMakeMap(value):
    global orgsToNormDict
    tokenSet = set(value.split(" "))
    finalSet = set([])	
    iterationCount = 0
    for token in tokenSet:        
        if token in tokenOrgDict:
            if len(finalSet) == 0 and iterationCount > 0:
                break
            if iterationCount == 0: #First Match
                finalSet = tokenOrgDict[token]            
                iterationCount+=1
            else: #Find Intersection of all Matches
                finalSet = tokenOrgDict[token].intersection(finalSet) #Copy or actual, looks like actual...?
        else: #Not 100% Match, Empty the Set
            finalSet = set([])
            break
    for org in finalSet:
        if org in orgsToNormDict:
            if len(value) > len(orgsToNormDict[org]): #Always take the longer string
                orgsToNormDict[org] = value
        else:
            orgsToNormDict[org] = value

def createOrgMap(): #Dictionary mapping KEY: Preprocessed, unnormalized org name | Value: Normalized org name
    global orgsToNormDict
    global tokenOrgDict
    
    orgsToNormDict = {}
    tokenOrgDict = createTokenMap()
    orgDictReader = csv.DictReader(open('preprocess_org_list.csv', 'rU')) #preprocess_org_list.csv
    for eachDict in orgDictReader:
        v = eachDict["org_name"]
        v = v.upper()
        intersectAndMakeMap(v)
    print "Number of Organizations that are Normalizable: %(size)d" % {"size":len(orgsToNormDict)}
    return orgsToNormDict

if __name__ == "__main__":
    rawSet = set([])
    preprocessSet = set([])
    rawDict = createOrgMap() # Keys are all Upper-Case

