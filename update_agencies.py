import csv
import database

db = database.Database()

f = open('agency_abbr.csv','rU')
c = csv.DictReader(f)

for row in c:
	data = {'agency':row['agency'],'abbr':row['abbr'],'code':row['code']}
	db.insert('orgs_agencies',data)
	
	