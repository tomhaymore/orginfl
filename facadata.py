from decimal import *
import csv
import database
import re
from prefixSuffixClass import *
from orgmatching import createOrgMap
from orgmatching import createPreprocessMap

#OH NO! GLOBAL VARIABLES!
suffixSet = set(returnSuffixList())
prefixSet = set(returnPrefixList())
orgNormalizationDict = createOrgMap() #Normalize organizations
preprocessDict = createPreprocessMap() #Correct misspellings

matchCounter = 0
overallCounter = 0
unmatchedList = []
matchedDict = {}

def matchOrganizations(eachDict, key, value):
    global matchCounter
    global overallCounter
    global unmatchedList
    global matchedDict
    if value in preprocessDict:
        value = preprocessDict[value] #Preprocesses string
    value = value.upper()
    if value in orgNormalizationDict:
        newValue = orgNormalizationDict[value]
        if newValue in matchedDict:
            matchedDict[newValue]+=1
        else:
            matchedDict[newValue] = 1
        eachDict[key] = orgNormalizationDict[value]
        matchCounter += 1
    else:
        unmatchedList.append(value)
    overallCounter +=1
	
def organizeNames(eachDict):
	fullName = eachDict["LastName"]
	nameList = fullName.split(" ")
	if len(nameList) > 1:
		eachDict["LastName"] = ""
		count = 0
		for eachName in nameList:
			if (eachName in prefixSet and count == 0):
				eachDict["Prefix"] = eachName
				count+=1
			elif (eachName in suffixSet and count == 1):
				eachDict["Suffix"] = eachName
				count+=1
			elif (count <= 2):
				eachName = eachName.replace(",", "")
				eachDict["LastName"] = eachName
				count=3
			elif (count <= 3):
				eachDict["FirstName"] = eachName
				count=4
			elif (count == 4):
				eachDict["MiddleName"] = eachName
				count+=1
	else:
		fullName = fullName.replace(",", "")
		eachDict["LastName"] = fullName

if __name__ == "__main__": #~4.5 Minutes without organization matching, 10 Minutes with 30% Match
	db = database.DataBase(host='127.0.0.1', user='root', passwd='', db = "FACADATA")
	for i in range(14): #14
		date = 1997 + i
		csvName = 'FACAMemberList%(date)d' % {'date':date}
		db.dropTable(csvName)
		db.createTable(csvName, 
		"""
		entry_no int not null auto_increment,
		ChangedBy varchar(80),
		CreatedAt varchar(40),
		ChangedAt varchar(40),
		CreatedBy varchar(80),
		IncludeinAnnualReport varchar(10),
		Prefix varchar(10),
		FirstName varchar(40),
		MiddleName varchar(40),
		LastName varchar(40),
		Suffix varchar(10),
		FY varchar(40),
		StartDate varchar(30),
		EndDate varchar(30),
		PayPlan varchar(60),
		PaySource varchar(20),
		OccupationOrAffiliation varchar(300),
		AgencyAbbr varchar(10),
		AppointmentType varchar(30),
		CommitteeName varchar(200),
		RepresentedGroup varchar(300),
		MemberDesignation varchar(80),
		Chairperson varchar(5),
		AppointmentTerm varchar (60),
		CNo varchar(10),
		LastLogonDate varchar(100),
		primary key(entry_no)
		""")
		facaDictReader = csv.DictReader(open(csvName +'.csv', 'rU'))		
		for eachDict in facaDictReader:
			for k,v in eachDict.items():
				if k == "FirstName" and v == "":
					organizeNames(eachDict)
				if k == "OccupationOrAffiliation":
					matchOrganizations(eachDict, k, v)
			db.insert(csvName, "", eachDict)
		print "Match Count: %(match)d" % {"match":matchCounter}
		print "Overall Count: %(overall)d" % {"overall" :overallCounter}
		print "Match Percentage: %(percent)f Percent" % {"percent": Decimal(matchCounter)/Decimal(overallCounter)*100}
		
		print len(matchedDict)
		for k,v in matchedDict.items():
		    if v > 0.0005*matchCounter:
				print "Title: " + k + " | Count: %f" % (100*Decimal(v)/Decimal(matchCounter)) +"%"
		
		"""unmatchCountDict = {}
		sum = 0
		for elem in unmatchedList:
			if elem in unmatchCountDict:
				unmatchCountDict[elem] += 1
			else:
				unmatchCountDict[elem] = 1
		for k,v in unmatchCountDict.items():
			if v < (.0005)*overallCounter and v > (.0001)*overallCounter: #.0001
				print "Title: " + k + " | Count: %f" % (100*Decimal(v)/Decimal(overallCounter)) +"%"
				sum += v
		print sum
        """
