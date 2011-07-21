import database
import csv
from normalize import normalizeOrgs

db = database.Database()

dir = '/Users/thaymore/Documents/Research/CDRG/Data/USASpending/'
files = ['2002_All_Contracts_Full_20110401.csv']
# files = ['2002_All_Contracts_Full_20110401.csv','2009_All_Contracts_Full_20110701.csv']

for f in files:

	f = open(dir+f,'rU')
	c = csv.DictReader(f)
	
	names = []
	namesDict = {}
	count = 0
	for row in c:
		if row['vendorname'] != '':
			names.append(row['vendorname'])
			namesDict[row['vendorname']] = []
			for item in [row['vendoralternatename'],row['vendorlegalorganizationname'],row['vendordoingasbusinessname']]:
				if item != '':
					if item not in namesDict[row['vendorname']]:
						namesDict[row['vendorname']].append(item)
		else:
			i = 0
			for item in [row['vendoralternatename'],row['vendorlegalorganizationname'],row['vendordoingasbusinessname']]:
				if item != '':
					if i == 0:
						names.append(item)
						primary = item
						namesDict[primary] = []
					else:
						namesDict[primary].append(item)
				i +=1		
		count +=1
	
	f.close()
	print "Number of entries in %(filename)s: %(entries)d" % {'filename':f,'entries':count}

file = '2010_All_Grants_Full_20110701.csv'

f = open(dir+file,'rU')
c = csv.DictReader(f)

count = 0
for row in c:
	names.append(row['recipient_name'])
	count +=1
	
print "Number of entries in %(filename)s: %(entries)d" % {'filename':file,'entries':count}
	
f.close()

nameSet = set(names)

data = {}

print "Number of orgs in set: %(number)d" % {'number':len(nameSet)}

for org in nameSet:
	print org
	data['name'] = normalizeOrgs(org)
	db.insert('orgs',data)
	orgId = db.insertId
	if org in namesDict:
		for alias in namesDict[org]:
			aliasData = {'org_id':orgId,'name':normalizeOrgs(alias)}
			db.insert('orgs_aliases',aliasData)

# need to add each org to table, then go through dict and add each alternate name