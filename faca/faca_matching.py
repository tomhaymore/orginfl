from decimal import *
import csv
import re
import sys
import os
import os.path
import argparse
import datetime
import glob
import time
import tempfile
from _sqlscript import *

"""
Loads all rows, skipping the header row, from CSV file.
"""
def loadRawData(fileName):

    tempScript = tempfile.mktemp('.sql')
    f = open( tempScript, 'w' )
    f.write(
    """
    TRUNCATE TABLE raw_faca;
    LOAD DATA CONCURRENT
    INFILE '%s'
    IGNORE
    INTO TABLE raw_faca
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r'
	IGNORE 1 LINES
    (
        AgencyAbbr,
        CommitteeName,
        CNo,
        FY,
        Prefix,
        FirstName,
        MiddleName,
        LastName,
        Suffix,
        MemberDesignation,
        RepresentedGroup,
        Chairperson,
        OccupationOrAffiliation,
        StartDate,
        EndDate,
        @dummy, -- CreatedAt,
        @dummy, -- CreatedBy,
        @dummy, -- ChangedAt,
        @dummy, -- ChangedBy,
        @dummy, -- IncludeinAnnualReport,
        AppointmentType,
        AppointmentTerm,
        PayPlan,
        PaySource,
        @dummy -- LastLogonDate
        );

    """ % fileName.replace('\\','\\\\') )
	#http://dev.mysql.com/doc/refman/5.0/en/user-variables.html about @
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

"""
Loads matching map
"""
def loadRawMatching():
    fileName = '/Users/kevinshin92/Research/Database/faca/CSV Files/org_matching_master.csv'
	#'/Users/kevinshin92/Research/orginfl/faca/CSV Files/test.csv'
	#'/Users/kevinshin92/Research/FACAMemberLists/new/FACAMemberList1997_new'
    tempScript = tempfile.mktemp('.sql')
    f = open(tempScript, 'w') # Creates temporary MySQL Script
    f.write(
    """
    TRUNCATE TABLE raw_faca_match;

    LOAD DATA CONCURRENT
    INFILE '%s'
    INTO TABLE raw_faca_match
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r'
	IGNORE 1 LINES
    (
        data,
        matchorg,
        id
        );
    
    """ % fileName.replace('\\','\\\\') )
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

"""
Through set properties, matches maps together
NOTE: There was an error from the git file and was corrected (I think it was a regular expression problem)
"""  
def intersectAndMatch(value, tokenOrgDict, orgsToNormDict):
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
				finalSet = tokenOrgDict[token].intersection(finalSet)
		else: #Not 100% Match, Empty the Set
			finalSet = set([])
			break
	for org in finalSet:
		if org in orgsToNormDict:
			if len(value) > len(orgsToNormDict[org]): #Always take the longer string
				orgsToNormDict[org] = value
		else:
			orgsToNormDict[org] = value	

"""
Returns Dictionary of a set map of actual data
Key: tokenized words
Value: normalized/regular expressioned data
"""
def createTokenMap(): 
	tokenToStringDict = {}
	for i in range(14): #14
		date = 1997 + i
		fileName = '/Users/kevinshin92/Research/datafeeds/FACAMemberLists/new/FACAMemberList%(date)d_new' % {'date':date}
		r = csv.DictReader(open(fileName +'.csv', 'rU'))		
		for row in r:
			v = row["OccupationOrAffiliation"]
			v = v.upper()
			tokenSet = set(v.split(" "))
			for token in tokenSet:
				if token not in tokenToStringDict:
					newSet = set([])
					tokenToStringDict[token] = newSet
				tokenToStringDict[token].add(v) #Add the normalized organized name				
	return tokenToStringDict

""" 
Creates master map of data to actual organizations and outputs to .csv file
"""
def createOrgMap(): 
	f = open('CSV Files/org_matching_master.csv','wb')
	w = csv.writer(f)
	w.writerow(['data', 'match', 'id'])
	orgsToNormDict = {}
	orgsToIDDict = {}
	tokenOrgDict = createTokenMap()
	r = csv.DictReader(open('CSV Files/org_id_list_new.csv', 'rU'))
	for row in r:
		orgID = row["org_id"] # Note: org_id may be different each time the script is run for preprocess because it iterates through a dictionary
		value = row["org_name"]
		value = value.upper()
		if value != "":
			intersectAndMatch(value, tokenOrgDict, orgsToNormDict)
			orgsToIDDict[value] = orgID
	print len(orgsToNormDict)
	for data,norm in orgsToNormDict.items():
		orgid = orgsToIDDict[norm]
		w.writerow([data, norm, orgid])
	f.close()

if __name__ == "__main__":
    #createOrgMap() # Only run if preprocess.py is run
	setMySqlCommand(getArgs());
	runSQLCommand('_cr_raw_match_table.sql');
	loadRawMatching() 
	runSQLCommand('_cr_raw_faca_table.sql');
	for i in range(14): #14
		date = 1997 + i
		fileName = '/Users/kevinshin92/Research/datafeeds/FACAMemberLists/new/FACAMemberList%(date)d_new.csv' % {'date':date}
		loadRawData(fileName)
		runSQLCommand('_process_faca_rows.sql')