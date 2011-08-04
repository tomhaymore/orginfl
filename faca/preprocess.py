import csv
import re
import database

db = database.Database()

def normalizeOrgs(v):
    """
    Remember to Always run Prepare for both cached dictionaries in orgmatching.py after adding/removing any regexes
    """
	#Character Removal/Clean Up
    v = re.sub(r'[\.\?\'\"!\$\*\+\)\(,;#]',"",v) # combined previous regex into one
    # v = re.sub(r"\?", "", v)
    # v = re.sub(r'\'', "", v)
    # v = re.sub(r'\"', "", v)
    # v = re.sub(r'!', "", v)
    # v = re.sub(r'\$', "", v)
    # v = re.sub(r'\*', "", v)
    # v = re.sub(r'\+', "", v)
    # v = re.sub(r'\(', "", v)
    # v = re.sub(r'\)', "", v)
    # v = re.sub(r'\-', " ", v)
    # v = re.sub(r"\.", "", v)
    # v = re.sub(r",", "", v)
    # v = re.sub(r";", "", v)
    # v = re.sub(r"#", "", v)	
    v = re.sub(r'\w&\w'," and ",v) # need to distinguish if ampersand has spaces around it or not
    v = re.sub(r"\s&\s", "and", v)
    v = re.sub(r'\s\s+', " ", v)
	
	#Typoes/Normalize Abbreviations
    v = re.sub(r'(?i)\bU\sS\b', 'US', v)
    v = re.sub(r'(?i)\bU\b', 'University', v)
    v = re.sub(r'(?i)\bSch\b', 'School', v)	
    v = re.sub(r'(?i)\bMed\b', 'Medical', v)
    v = re.sub(r'(?i)\b(Tec|Tech)\b', 'Technology', v)
    v = re.sub(r'(?i)\bMus\b', 'Museum', v)
    v = re.sub(r'(?i)\bEduc\b', 'Education', v)	
    v = re.sub(r'(?i)\bBus\b', 'Business', v)	
    # v = re.sub(r'(?i)\bPub\b', 'Public', v)	
    v = re.sub(r'(?i)\bHist\b', 'History', v)	
    v = re.sub(r'(?i)\bAssoc\b', 'Association', v)	
    v = re.sub(r'(?i)\bAsst\b', 'Assistant', v)
    v = re.sub(r'(?i)\bAsstistant\b', 'Assistant', v)
    v = re.sub(r'(?i)\bUniv\b', 'University', v)
    v = re.sub(r'(?i)\bbUniveristy\b', 'University', v)	
    v = re.sub(r'(?i)\bUnivesity\b', 'University', v)	
    v = re.sub(r'(?i)\bCorp\b', 'Corporation', v)	
    v = re.sub(r'(?i)\bAssn\b', 'Association', v)	
    v = re.sub(r'(?i)\bInst\b', 'Institution', v)	
    v = re.sub(r'(?i)\b(Gov|Govt)\b', 'Government', v)	
    v = re.sub(r'(?i)\bIntl\b', 'International', v)	
    v = re.sub(r'(?i)\bNatl\b', 'National', v)
    v = re.sub(r'(?i)\bLLC\b', '', v)
    v = re.sub(r'(?i)\bCo\b', 'Company', v)	
    v = re.sub(r'(?i)\bDept\b', 'Department', v)	
    v = re.sub(r'(?i)\bOrg\b', 'Organization', v)	
    v = re.sub(r'(?i)^[T]he\s', '', v)	
    v = re.sub(r'(?i)\bAuth\b', 'Authority', v)
    v = re.sub(r'(?i)\bTechnol\w?\b','Technology',v)
	
    #States and Cities
    v = re.sub(r'(?i)\bFlordia\b', 'Florida', v)
    v = re.sub(r'(?i)\bPenn\b', 'Pennsylvania', v)	
    v = re.sub(r'(?i)\b(Cal|Cali|Calif|Califronia)\b', 'California', v)	
    v = re.sub(r'(?i)\bLA\b', 'Los Angeles', v)
    v = re.sub(r'(?i)\bSD\b', 'San Diego', v)
    v = re.sub(r'(?i)\bSF\b', 'San Francisco', v)
    v = re.sub(r'(?i)\bIrv\b', 'Irvine', v)
    v = re.sub(r'(?i)\bBerk\b', 'Berkeley', v)

    #University Normalizations	
    v = re.sub(r'(?i)\bUPenn\b', 'University Of Pennsylvania', v)	
    v = re.sub(r'(?i)\bMIT\b', 'Massachusetts Institute Of Technology', v)	
    v = re.sub(r'(?i)\b(Cal\bTech|CalTech)\b', 'California Institute Of Technology', v)	
    v = re.sub(r'(?i)\bJohn(s)?\bHopkin(s)?\b', 'Johns Hopkins', v)	
    v = re.sub(r'(?i)\bJHU\b', 'Johns Hopkins University', v)
    v = re.sub(r'(?i)\bCMU\b', 'Carnegie Mellon University', v)	
    v = re.sub(r'(?i)\bUC\b', 'University Of California', v)	
    v = re.sub(r'(?i)\bUSC\b', 'University Southern California', v)	
    v = re.sub(r'(?i)\bUVirginia\b', 'University Of Virginia', v)	
    v = re.sub(r'(?i)\bUoV\b', 'University Of Virginia', v)	
    v = re.sub(r'(?i)\bUMich\b', 'University Of Michigan', v)	
    v = re.sub(r'(?i)\bUCLA\b', 'University Of California Los Angeles', v)	
    v = re.sub(r'(?i)\bUCSD\b', 'Universaity Of California San Diego', v)	
    v = re.sub(r'(?i)\bUCI\b', 'University Of California Irvine', v)	
    v = re.sub(r'(?i)\bUCD\b', 'University Of California Davis', v)
    v = re.sub(r'(?i)\bUCSB\b', 'University Of California Santa Barbara', v)	
    v = re.sub(r'(?i)\bUNC\b', 'University Of North Carolina', v)	
    v = re.sub(r'(?i)\bBC\b', 'Boston College', v)	
    v = re.sub(r'(?i)\bNYU\b', 'New York University', v)	
    v = re.sub(r'(?i)\bGeorgiaTech\b', 'Georgia Institute of Technology', v)	
    v = re.sub(r'(?i)\bRPI\b', 'Rensselaer Polytechnic Institute', v)	
    v = re.sub(r'(?i)\bWashU\b', 'University Of Washington', v)	
    v = re.sub(r'(?i)\bUT\b', 'University Of Texas', v)	
    v = re.sub(r'(?i)\bUIUC\b', 'University Of Illinois Urbana Champaign', v)	
    v = re.sub(r'(?i)\bUMiami\b', 'University Of Miami', v)	
    v = re.sub(r'(?i)\b(SUNY|State\sUniversity\sof\sNew\sYork)(\s|,|-|--)(ESF|College\sof\sEnvironmental\sScience\sand\sForestry)\b', 'SUNY College of Environmental Science & Forestry', v)
    v = re.sub(r'(?i)\bUniv\w+\sof\sMaryland(\s|,|-|--)College\sPark\b','University of Maryland College Park',v)
    v = re.sub(r'(?i)\bUniv\w+\sof\sMinnesota(\s|,|-|--)Twin\sCities\b','University of Minnesota Twin Cities',v)
    v = re.sub(r'(?i)\bUniv\w+\sof\sCali\w+(\s|,|-|--)Santa\sCruz\b','University of California Santa Cruz',v)
    v = re.sub(r'(?i)\bUniv\w+\sof\sColorado(\s|,|-|--)Boulder\b','University of Colorado Boulder',v)
    v = re.sub(r'(?i)\bUniv\w+\sof\sCali\w+(\s|,|-|--)Riverside\b','University of California Riverside',v)
    v = re.sub(r'(?i)\bOhio\sState\sUniv\w+(\s|,|-|--)Columbus\b','Ohio State University Columbus',v)
    v = re.sub(r'(?i)\bTexas\sA\s?\&\s?M\sUniv\w+\b','Texas A and M University',v)
    v = re.sub(r'(?i)\bIndiana\sUniv\w+(\s|,|-|--)Bloomington\b','Indiana University Bloomington',v)
    v = re.sub(r'(?i)\bMiami\sUniv\w+(\s|,|-|--)Oxford\b','Miami University Oxford',v)
    v = re.sub(r'(?i)\bBinghamton\sUniv\w+(SUNY|State\sUniversity\sof\sNew\sYork)?\b','Binghamton University SUNY',v)
    v = re.sub(r'(?i)\b(Virginia\sTech\b|Virginia\sPolytechnic(al)?\sInstitute\sand\sState\sUniv\w+)\b','Virginia Tech',v)
	
    #Corporations and Organizations
    v = re.sub(r'(?i)\w*Boeing\w*','Boeing Corporation',v)
    v = re.sub(r'(?i)\bWal(\s)Mart\b', 'WalMart', v)
    v = re.sub(r'(?i)\bExxonMobil\b', 'Exxon Mobil', v)
    v = re.sub(r'(?i)\bConocoPhillips\b', 'Conoco Phillips', v)		
    v = re.sub(r'(?i)\bFannieMae\b', 'Fannie Mae', v)	
    v = re.sub(r'(?i)\bGeneralElectric\b', 'General Electric', v)
    v = re.sub(r'(?i)\bGeneral(\s)?Motors\b', 'General Motors', v)
    v = re.sub(r'(?i)\bBOA\b', 'Bank of America Corp', v)
    v = re.sub(r'(?i)\bHewlet(t)?(\s)?Packard\b', 'Hewlett Packard', v)
    v = re.sub(r'(?i)\bHP\b', 'Hewlett Packard', v)
    v = re.sub(r'(?i)\b(AIG|American\s(International|Int(\')?l)\sGroup)\b', 'American International Group', v)
    v = re.sub(r'(?i)\b(IBM|(Int\'?l|International)\sBusiness\sMachines)\b', 'International Business Machines', v)								
    v = re.sub(r'(?i)\bCDC\b','Centers for Disease Control',v)
    v = re.sub(r'(?i)\bFCC\b','Federal Communications Commission',v)
    v = re.sub(r'(?i)\bNTIA\b','National Telecommunications and Infrastructure Administration',v)
    v = re.sub(r'(?i)\bJet\sPropulsion\sLaboratory\b','National Aeronautics and Space Administration',v)
    v = re.sub(r'(?i)\bNIST\b','National Institute of Standards and Technology',v)
    
    
    #Regular Expressions for General Titles.
    return v

def preprocessFACA():
	for i in range(14): #14
		date = 1997 + i
        dir = '/Users/thaymore/Documents/Research/CDRG/Data/FACA/'
        baseName = 'FACAMemberList%(date)d' % {'date':date}
        r = csv.DictReader(open(dir + baseName +'.csv', 'rU'))
        w = csv.DictWriter(open(dir + baseName + '_new.csv', 'wb'),fieldnames = r.fieldnames)
        w.writerow(dict((fn,fn) for fn in r.fieldnames))
        for row in r:
            old = row["OccupationOrAffiliation"]

            row["OccupationOrAffiliation"] = normalizeOrgs(row["OccupationOrAffiliation"])
            # test to see if first and middle name fields are empty
            if (row["Prefix"] == '' and row["FirstName"] == '' and row["MiddleName"] == ''):
            	names = row["LastName"].replace(",","")
            	names = names.split(" ")
            	# test again to make sure that there is more than one name in LastName field
            	if len(names) > 1:
            		count = 0
            		for name in names:
            			if count == 0:
            				row["LastName"] = name
            				count += 1
            			elif count == 1:
            				row["FirstName"] = name
            				count += 1
            			elif count == 2:
            				row["MiddleName"] = name
            				count += 1
            			else:
            				# what do we do here?
            				pass
            # for k,v in row.items():
            #    if k == "OccupationOrAffiliation":
            #        v = normalizeOrgs(v) #Regular Expressions
            #        row["OccupationOrAffiliation"] = v
            new = row["OccupationOrAffiliation"]
            #if old != new:
            #	print old + " | " + new
            w.writerow(row)

def preprocessOrgs():
	header = {'org_name':'org_name','org_id':'org_id'}
	# header = ['org_name','org_id']
	f = open('orgs_list.csv','wb')
	w = csv.DictWriter(f,fieldnames = header)
	w.writerow(header)
	orgs = db.get('orgs')
	for o in orgs:
		org = {}
		org['org_name'] = str(o[1])
		org['org_id'] = str(o[0])
		w.writerow(org)
		

          
if __name__ == '__main__':
	preprocessFACA()
	preprocessOrgs()