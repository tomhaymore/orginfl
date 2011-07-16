import csv
from preprocess import returnNormalizedString

funWriter = csv.writer(open('preprocess_prev_org_list.csv', 'wb'))
funWriter.writerow(["", "org_name"])
orgSet = set([])

count = 0

funDictReader = csv.DictReader(open('raw_prev_org_list.csv', 'rU'))
for each in funDictReader:
    print each
    v = each["org_name"]
    v = returnNormalizedString(v)
    orgSet.add(v)
    count+=1

otherCount = 0    
for each in orgSet:
    funWriter.writerow([otherCount, each])
    otherCount += 1
    
print "Set Count: %d" % len(orgSet)
print "Overall Count: %d" % count