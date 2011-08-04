from decimal import *
import csv
import database
import re

orgsToNormDict = {}
tokenOrgDict = {}

def createOrgMap(): 
    
    """ 
    creates master map of data to actual organizations
    """
    
    global orgsToNormDict
    global tokenOrgDict
    global orgId
    global header
    
    orgsToNormDict = {}
    tokenOrgDict = createTokenMap()
    r = csv.DictReader(open('orgs_list.csv', 'rU')) #preprocess_org_list.csv
    for row in r:
        orgId = row["org_id"]
        v = row["org_name"]
        v = v.upper()
        intersectAndMatch(v)
    # print "Number of Organizations that are Normalizable: %(size)d" % {"size":len(orgsToNormDict)}
    return orgsToNormDict
    

def createTokenMap(): 
    
    """ returns dictionary - set map of actual data
    key: tokenized words
    value: normalized data
    """
    
    tokenToStringDict = {}
    # don't need preprocess anymore because the file is preprocessed
    # preprocessDict = createPreprocessMap()
    count = 0
    for i in range(14): #14
        date = 1997 + i
        fileName = '/Users/thaymore/Documents/Research/CDRG/Data/FACA/FACAMemberList%(date)d' % {'date':date}
        # r = csv.DictReader(open(fileName +'_new.csv', 'rU'))		
        r = csv.reader(open(fileName +'_new.csv', 'rU'))		
        for row in r:
            v = row[12] # row["OccupationOrAffiliation"]
            # value = preprocessDict[v] # Get Preprocessed Value
            v = v.upper()
            tokenSet = set(v.split(" ")) # Tokenize
            for token in tokenSet:
                if token not in tokenToStringDict:
                    newSet = set([])
                    tokenToStringDict[token] = newSet
                tokenToStringDict[token].add(v) #Add the normalized organized name
            count += 1
    print "Size of Token to Org Dict: %(size)d" % {"size":len(tokenToStringDict)}
    print "Num of Total Orgs: %d" % count
    return tokenToStringDict

def intersectAndMatch(value):
    
    """ matches maps together
    """
    
    global orgsToNormDict
    global orgId
    global header
    
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
    # need to check here for empty finalSet and skip next if so; else starts packing into final set
    
    f = open('org_matching_master.csv','a')
    w = csv.DictWriter(f,fieldnames = header)
    
    for org in finalSet:
        # write in matches: org, match, id
        data = {'data':org,'match':value,'id':orgId}
        w.writerow(data)
        if org in orgsToNormDict:
            if len(value) > len(orgsToNormDict[org]): #Always take the longer string
                orgsToNormDict[org] = value
                # write to file -- or later
        else:
            orgsToNormDict[org] = value
            # write to file
    f.close()

if __name__ == "__main__":
    global header
    f = open('org_matching_master.csv','wb')
    header = {'data':'data','match':'match','id':'id'}
    w = csv.DictWriter(f,fieldnames = header)
    w.writerow(header)
    rawSet = set([])
    preprocessSet = set([])
    rawDict = createOrgMap() # Keys are all Upper-Case
    # print rawDict
    # probably should run usa spending first; get the list of organizations
    # at this point, should probably use master map and write another version of the FACA files
    # then put them into the database and start folding over
