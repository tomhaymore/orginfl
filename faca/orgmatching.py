from decimal import *
import csv
import database
import re
import sys
import os
import os.path
import argparse
import datetime
import glob
import time
import tempfile

orgsToNormDict = {}
tokenOrgDict = {}

def getArgs():
    """
    Command argument parser

    Returns structure:
        args.server
        args.port
        args.db
        args.user
        args.password
        args.input

    """
    parser = argparse.ArgumentParser(description='FACA Data Import')
    parser.add_argument( '-s', '--server', help='Server', default='localhost')
    parser.add_argument( '-P', '--port', help='Server communication port', default=3306)
    parser.add_argument( '-d', '--db', help='Database, e.g., cdrg', default='cdrg')
    parser.add_argument( '-u', '--user', help='DB User', default='root')
    parser.add_argument( '-p', '--password', help='User password', default='')
    parser.add_argument( 'input', help='CSV file or directory containing CSV files')

    args = parser.parse_args()
    return args

def getScriptAbsPath( scriptName ):
    return os.path.join( os.path.dirname( __file__ ), scriptName );

def setMySqlCommand( args):
    """
    Create mysql command with parameters for executing a script file
    """
    global sqlCmd
    sqlCmd = "mysql -u%(user)s -h%(host)s -P%(port)s -D%(db)s -v -v -v -f " % {
        'host': args.server,
        'user': args.user,
        'db'  : args.db,
        'port': args.port
    }
    if args.password!= None and args.password!='':
        sqlCmd += " -p%s " % args.password
    return sqlCmd

def getMySqlCommand():
    """
    a gloal variable wrapper
    """
    global sqlCmd
    return sqlCmd

def showMsg( message):
    """
    Displays a message printing it to the standart streem STDERR
    """
    sys.stderr.write( message+'\n' )

def loadRawData( fileName):
    """
    Loads all rows, skipping the header row, from CSV file.
    """

    tempScript = tempfile.mktemp('.sql')
    f = open( tempScript, 'w' )
    f.write(
    """
    TRUNCATE TABLE raw_faca;
    ALTER TABLE raw_faca DROP INDEX raw_faca_org_id_idx;
    ALTER TABLE raw_faca DROP INDEX raw_faca_maj_agency_cat_idx;
    ALTER TABLE raw_faca DROP INDEX raw_faca_agency_org_id_idx;
    ALTER TABLE raw_faca DISABLE KEYS;

    LOAD DATA CONCURRENT
    INFILE '%s'
    IGNORE
    INTO TABLE raw_faca
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '\\"'
    LINES TERMINATED BY '\\n'
     
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
        @StartDate,
        @EndDate,
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
        )

        ALTER TABLE raw_faca ENABLE KEYS;
    """ % fileName.replace('\\','\\\\') )
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

def loadRawMatching():
    """
    Loads matching map
    """

    tempScript = tempfile.mktemp('.sql')
    f = open( tempScript, 'w' )
    f.write(
    """
    TRUNCATE TABLE raw_faca_match;
    ALTER TABLE raw_faca_match DROP INDEX raw_faca_id_idx;
    ALTER TABLE raw_faca_match DROP INDEX raw_faca_data_idx;
    ALTER TABLE raw_faca_match DISABLE KEYS;

    LOAD DATA CONCURRENT
    INFILE '%s'
    IGNORE
    INTO TABLE raw_faca_match
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '\\"'
    LINES TERMINATED BY '\\n'
     
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
        @StartDate,
        @EndDate,
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
        )

        ALTER TABLE raw_faca ENABLE KEYS;
    """ % fileName.replace('\\','\\\\') )
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

def processRows():
    """
    Invokes process_faca_rows.sql to process loaded rows from the CSV file
    """
    cmd = getMySqlCommand()+"<\""+ getScriptAbsPath('process_faca_rows.sql') +"\""
    os.system( cmd  )

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
    createOrgMap() # Keys are all Upper-Case
    loadRawMatching()
    for i in range(14):
    	date = 1997 + i
        fileName = '/Users/thaymore/Documents/Research/CDRG/Data/FACA/FACAMemberList%(date)d' % {'date':date}
        loadRawData(filename)
        processRows()
    # print rawDict
    # need to load org_matching_master.csv into database, then use it as part of process_faca to fold over into db
