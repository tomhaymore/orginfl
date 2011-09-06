import csv
from _regexstring import normalizeOrgs
from _prefixsuffix import *

suffixSet = frozenset(returnSuffixList())
prefixSet = frozenset(returnPrefixList())

"""
ONLY RUN THIS SCRIPT IF
1) The master organization reference list has been altered to add/remove organizations
2) _regexstring has been altered

Does not insert anything to database, just creates new .csv files for stylistic reasons
FACAMemberLists get regular expressioned while the raw_org_list gets a new id field and is regexed
"""

"""
Organizes names by looking at prefix, suffix, last, first, middle
"""
def organizeNames(eachDict):
	fullName = eachDict["LastName"]
	fullName = fullName.replace(",", "")
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
				eachDict["LastName"] = eachName
				count=3
			elif (count <= 3):
				eachDict["FirstName"] = eachName
				count=4
			elif (count == 4):
				eachDict["MiddleName"] = eachName
				count+=1
	else:
		eachDict["LastName"] = fullName

"""
Organizes dates to MySQL Format for FACA
"""
def organizeDates(eachDict, dateValue):
	formatDate = eachDict[dateValue]
	tempList = formatDate.split(" ")
	formatDate = tempList[0]
	tempList = formatDate.split("/")
	if len(tempList) > 1:
		if len(tempList[2]) == 2:
			if int(tempList[2]) > 12: #12 is arbitrary cutoff point where it could be 1900s or 2000s
				tempList[2] = "19" + tempList[2]
			else:
				tempList[2] = "20" + tempList[2]
		if len(tempList[1]) == 1:
			tempList[1] = "0" + tempList[1]
		if len(tempList[0]) == 1:
			tempList[0] = "0" + tempList[0]
		formatDate = tempList[2] + "-" +  tempList[0] + "-" + tempList[1]
	eachDict[dateValue] = formatDate


"""
For each FACAMemberList, modifies the name if necessary and runs regular expressions on occupation or affiliation
and outputs new csv file
"""
def preprocessFACA():
	for i in range(1): #14
		date = 1997 + i
		oldDir = '/Users/kevinshin92/Research/datafeeds/FACAMemberLists/old/'
		newDir = '/Users/kevinshin92/Research/datafeeds/FACAMemberLists/new/'
		baseName = 'FACAMemberList%(date)d' % {'date':date}
		readFile = open(oldDir + baseName +'.csv', 'rU')
		writeFile = open(newDir + baseName + '_new.csv', 'wb')
		r = csv.DictReader(readFile)
		w = csv.DictWriter(writeFile, r.fieldnames)
		w.writerow(dict((fn,fn) for fn in r.fieldnames))
		for row in r:
			old = row["OccupationOrAffiliation"]
			# Run regular expressions on occupations
			row["OccupationOrAffiliation"] = normalizeOrgs(old)
			# Test to see if prefix, first, middle, and suffix fields are empty
			organizeDates(row, "StartDate")
			organizeDates(row, "EndDate")
			if (row["FirstName"] == '' and row["MiddleName"] == ''): #Prefix/Suffix can be filled
				organizeNames(row)
			w.writerow(row)
		readFile.close()
		writeFile.close()

"""
For the master organization list, runs regular expressions on occupation or affiliation and outputs new csv file
"""
def preprocessOrgs():
	orgs = csv.DictReader(open('CSV Files/reference/raw_org_list.csv','rU'))
	w = csv.writer(open('CSV Files/org_id_list_new.csv', 'wb'))
	w.writerow(['org_name', 'org_id'])
	count = 1;
	for o in orgs:
		old = o["org_name"]
		new = normalizeOrgs(old)
		w.writerow([new, count])
		count += 1

"""
Cleans up the FACA and the organization list data
"""
if __name__ == '__main__':
	preprocessFACA()
	#preprocessOrgs()