#-------------------------------------------------------------------------------
# Name:        usaspending_grants
# Purpose:     USA Spending Grants Data load and processing
#
# Author:      Thomas Haymore, based on usaspending_auto.py by Radomirs Cirskis
#
# Created:     07/25/11
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import os
import os.path
import argparse
import datetime
import glob
import time
import tempfile

def getArgs():
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
    parser = argparse.ArgumentParser(description='USA Spending Grants Data Import')
    parser.add_argument( '-s', '--server', help='Server', default='localhost')
    parser.add_argument( '-P', '--port', help='Server communication port', default=3306)
    parser.add_argument( '-d', '--db', help='Database, e.g., cdrg', default='cdrg')
    parser.add_argument( '-u', '--user', help='DB User', default='root')
    parser.add_argument( '-p', '--password', help='User password', default='')
    parser.add_argument( 'input', help='CSV file or directory containing CSV files')

    args = parser.parse_args()
    return args

def getScriptAbsPath( scriptName ):
    return os.path.join( os.path.dirname( __file__ ), scriptName );

def setMySqlCommand( args):
    """
    Create mysql command with parameters for executing a script file
    """
    global sqlCmd
    sqlCmd = "mysql -u%(user)s -h%(host)s -P%(port)s -D%(db)s -v -v -v -f " % {
        'host': args.server,
        'user': args.user,
        'db'  : args.db,
        'port': args.port
    }
    if args.password!= None and args.password!='':
        sqlCmd += " -p%s " % args.password
    return sqlCmd

def getMySqlCommand():
    """
    a gloal variable wrapper
    """
    global sqlCmd
    return sqlCmd

def showMsg( message):
    """
    Displays a message printing it to the standard streem STDERR
    """
    sys.stderr.write( message+'\n' )

def loadRawData( fileName):
    """
    Loads all rows, skipping the header row, from CSV file.
    """
	
    tempScript = tempfile.mktemp('.sql')
    f = open( tempScript, 'w' )
    f.write(
    """
    TRUNCATE TABLE raw_grants;
    ALTER TABLE raw_grants DROP INDEX raw_grants_org_id_idx;
    ALTER TABLE raw_grants DROP INDEX raw_grants_maj_agency_cat_idx;
    ALTER TABLE raw_grants DROP INDEX raw_grants_agency_org_id_idx;
    ALTER TABLE raw_grants DISABLE KEYS;

    LOAD DATA CONCURRENT
    INFILE '%s'
    IGNORE
    INTO TABLE raw_grants
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '\\"'
    LINES TERMINATED BY '\\n'
     
    (
            @unique_transaction_id,
            @dummy, -- transaction_status,
            @dummy, -- fyq
            @dummy, -- cfda_program_num
            @dummy, -- sai_number
            account_title,
            recipient_name,
            @dummy, -- recipient_city_code
            recipient_city_name,
            @dummy, -- recipient_county_code
            recipient_county_name,
            recipient_zip,
            recipient_type,
            action_type,
            agency_code,
            federal_award_id,
            @dummy, -- federal_award_mod
            fed_funding_amount,
            non_fed_funding_amount,
            total_funding_amount,
            @dummy, -- obligation_action_date
            starting_date,
            ending_date,
            assistance_type,
            @dummy, -- record_type
            @dummy, -- correction_late_ind
            @dummy, -- fyq_correction
            @dummy, -- principal_place_code
            principal_place_state,
            principal_place_cc,
            principal_place_zip,
            principal_place_cd,
            cfda_program_title,
            agency_name,
            project_description,
            duns_no,
            @dummy, -- duns_conf_code
            progsrc_agen_code,
            @dummy, -- progsrc_acnt_code
            @dummy, -- progsrc_subacnt_code
            receip_addr1,
            receip_addr2,
            receip_addr3,
            @dummy, -- face_loan_guran
            @dummy, -- orig_sub_guran
            fiscal_year,
            @dummy, -- principal_place_state_code
            recip_cat_type,
            asst_cat_type,
            recipient_cd,
            maj_agency_cat,
            @dummy, -- rec_flag
            @dummy, -- recipient_country_code
            uri,
            @dummy, -- recipient_state_code )
        SET unique_transaction_id = UNHEX(@unique_transaction_id);

        ALTER TABLE raw_grants ENABLE KEYS;
    """ % fileName.replace('\\','\\\\') )
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

def processRows():
    """
    Invokes process_grants_rows.sql to process loaded rows from the CSV file
    """
    cmd = getMySqlCommand()+"<\""+ getScriptAbsPath('process_contracts_rows.sql') +"\""
    os.system( cmd  )

def main():
    """
    1. parse parameters;
    2. loops through the file list (one file or all in the directory);
    3. loads file and prcesses it;
    """
    time_start = time.time()
    args = getArgs()
    setMySqlCommand( args)
    if not os.path.exists( args.input ):
        raise Exception("File or directory %s doesn't exist!" % args.input)

    # data source:
    source = os.path.abspath( args.input)
    # List of CSV files:
    source = [source] if os.path.isfile( source) else glob.glob( os.path.join( source, '*.csv') )

    totalRowCount = 0
    for f in source:
        loadRawData(f)
        processRows()

    showMsg( "Data processing completed in %.5f sec."
        % (time.time()-time_start))

if __name__ == '__main__':
    main()
