import csv

dataPath = "/Users/thaymore/Documents/Research/CDRG/Data/regulations/regulations.csv"

f = open(dataPath, 'r')
i = 0

lines = f.readlines(1024)

print lines[0]

#for line in f:
#	i += 1
	
#print i