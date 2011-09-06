import sys
import os
import os.path
import argparse
import datetime
import glob
import time
import tempfile
from _sqlscript import *

args = getArgs()
setMySqlCommand( args)
if not os.path.exists( args.input ):
    raise Exception("File or directory %s doesn't exist!" % args.input)
runSQLCommand('_mastertables.sql')

fileName = "/Users/kevinshin92/Research/Database/faca/CSV Files/org_id_list_new.csv"
tempScript = tempfile.mktemp('.sql')
f = open( tempScript, 'w' )
f.write(
"""
TRUNCATE TABLE orgs;
LOAD DATA CONCURRENT
INFILE '%s'
IGNORE
INTO TABLE orgs
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 LINES
(
name,
id
);

 """ % fileName.replace('\\','\\\\') )
f.close()
cmd = getMySqlCommand()+"<\""+tempScript+"\""
os.system( cmd  )

fileName = "/Users/kevinshin92/Research/Database/initialization/agency_abbr.csv"
tempScript = tempfile.mktemp('.sql')
f = open( tempScript, 'w' )
f.write(
"""
TRUNCATE TABLE agencies;
LOAD DATA CONCURRENT
INFILE '%s'
IGNORE
INTO TABLE agencies
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r'
IGNORE 1 LINES
(
abbr,
agency_name
);

 """ % fileName.replace('\\','\\\\') )
f.close()
cmd = getMySqlCommand()+"<\""+tempScript+"\""
os.system( cmd  )


