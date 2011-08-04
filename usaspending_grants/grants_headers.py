import csv

file = '/Users/thaymore/Documents/Research/CDRG/Data/USASpending/2010_All_Grants_Full_20110701.csv'

f = open(file,'rU')
r = csv.reader(f)

header = []

i = 0
for row in r:
	if i <= 1:
		for item in row:
			header.append(item)
		i += 1
	else:
		break


print header