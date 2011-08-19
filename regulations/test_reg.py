import csv

dataPath = "/Users/thaymore/Documents/Research/CDRG/Data/regulations/regulations.csv"

f = open(dataPath, 'r')
i = 0

lines = f.readlines(10024)

for line in lines[0:100]:
	line = line.split(',')
	print line[7]

#for line in f:
#	i += 1
	
#print i