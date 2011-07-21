import database
import csv

db = database.Database()

orgs = db.get('orgs')

# print orgs

data = {}


dir = '/Users/thaymore/Documents/Research/CDRG/Data/USASpending/'
files = ['2002_All_Contracts_Full_20110401.csv']

# files = ['2010_All_Grants_Full_20110701.csv']
# files = ['2002_All_Contracts_Full_20110401.csv','2009_All_Contracts_Full_20110701.csv']

for f in files:

	f = open(dir+f,'rU')
	c = csv.DictReader(f)
	
	names = []
	namesDict = {}
	count = 0
	for row in c:
		
		if row['vendorname'].find('\\') >= 0:
			print row['vendorname']

# db.insert('orgs',data)

# print db.insertId 
# print db.lastQuery