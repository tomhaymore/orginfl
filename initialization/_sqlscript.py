import sys
import os
import os.path
import argparse
import tempfile

"""
Command argument parser

Returns structure:
    args.server
    args.port
    args.db
    args.user
    args.password
    args.input

"""
def getArgs():
    parser = argparse.ArgumentParser(description='USA Spending Grants Data Import')
    parser.add_argument( '-s', '--server', help='Server', default='localhost')
    parser.add_argument( '-P', '--port', help='Server communication port', default=3306)
    parser.add_argument( '-d', '--db', help='Database, e.g., cdrg', default='cdrg')
    parser.add_argument( '-u', '--user', help='DB User', default='root')
    parser.add_argument( '-p', '--password', help='User password', default='')
    parser.add_argument( '-i', '--input', help='CSV file or directory containing CSV files', default = '/Users/kevinshin92/Research/datafeeds/Contracts')

    args = parser.parse_args()
    return args

"""
Returns absolute path of a local scriptName
"""
def getScriptAbsPath( scriptName ):
    return os.path.join( os.path.dirname( __file__ ), scriptName );

"""
Create mysql command with parameters for executing a script file
"""
def setMySqlCommand( args):
    global sqlCmd
    sqlCmd = "mysql5 -u%(user)s -h%(host)s -P%(port)s -D%(db)s -v -v -v -f " % {
        'host': args.server,
        'user': args.user,
        'db'  : args.db,
        'port': args.port
    }
    if args.password!= None and args.password!='':
        sqlCmd += " -p%s " % args.password
    return sqlCmd

"""
Global variable wrapper
"""
def getMySqlCommand():
    global sqlCmd
    return sqlCmd

def showMsg( message):
    """
    Displays a message printing it to the standard streem STDERR
    """
    sys.stderr.write( message+'\n' )

"""
Invokes process_grants_rows.sql to process loaded rows from the CSV file
"""
def runSQLCommand(fileName):
    cmd = getMySqlCommand()+"<\""+ getScriptAbsPath(fileName) +"\""
    os.system(cmd)

if __name__ == '__main__':
	print "Class for script, not meant to be run"