#-------------------------------------------------------------------------------
# Name:        faca
# Purpose:     FACA Data load and processing
#
# Author:      Radomirs Cirskis, modified by Thomas Haymore
#
# Created:     15/05/2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import os
import os.path
import argparse
import datetime
##import pymysql
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
    parser = argparse.ArgumentParser(description='FACA Data Import')
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
    Displays a message printing it to the standart streem STDERR
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
    TRUNCATE TABLE raw_contracts;
    ALTER TABLE raw_contracts DROP INDEX raw_contracts_org_id_idx;
    ALTER TABLE raw_contracts DROP INDEX raw_contracts_maj_agency_cat_idx;
    ALTER TABLE raw_contracts DROP INDEX raw_contracts_agency_org_id_idx;
    ALTER TABLE raw_contracts DISABLE KEYS;

    LOAD DATA CONCURRENT
    INFILE '%s'
    IGNORE
    INTO TABLE raw_contracts
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '\\"'
    LINES TERMINATED BY '\\n'
     
    (
            @unique_transaction_id,
            @dummy, -- transaction_status,
            obligatedamount,
            @dummy, -- baseandexercisedoptionsvalue,
            @dummy, -- baseandalloptionsvalue,
            maj_agency_cat,
            @dummy, -- mod_agency,
            @dummy, -- maj_fund_agency_cat,
            @dummy, -- contractingofficeagencyid,
            @dummy, -- contractingofficeid,
            @dummy, -- fundingrequestingagencyid,
            @dummy, -- fundingrequestingofficeid,
            @dummy, -- fundedbyforeignentity,
            @dummy, -- signeddate,
            effectivedate,
            @dummy, -- currentcompletiondate,
            ultimatecompletiondate,
            @dummy, -- lastdatetoorder,
            @dummy, -- contractactiontype,
            @dummy, -- reasonformodification,
            @dummy, -- typeofcontractpricing,
            @dummy, -- priceevaluationpercentdifference,
            @dummy, -- subcontractplan,
            @dummy, -- type_of_contract,
            @dummy, -- lettercontract,
            @dummy, -- multiyearcontract,
            @dummy, -- performancebasedservicecontract,
            @dummy, -- majorprogramcode,
            @dummy, -- contingencyhumanitarianpeacekeepingoperation,
            @dummy, -- contractfinancing,
            @dummy, -- costorpricingdata,
            @dummy, -- costaccountingstandardsclause,
            descriptionofcontractrequirement,
            @dummy, -- purchasecardaspaymentmethod,
            @dummy, -- numberofactions,
            @dummy, -- nationalinterestactioncode,
            @dummy, -- progsourceagency,
            @dummy, -- progsourceaccount,
            @dummy, -- progsourcesubacct,
            account_title,
            @dummy, -- rec_flag,
            @dummy, -- typeofidc,
            @dummy, -- multipleorsingleawardidc,
            @dummy, -- programacronym,
            vendorname,
            vendoralternatename,
            vendorlegalorganizationname,
            vendordoingasbusinessname,
            @dummy, -- divisionname,
            @dummy, -- divisionnumberorofficecode,
            @dummy, -- vendorenabled,
            @dummy, -- vendorlocationdisableflag,
            @dummy, -- ccrexception,
            streetaddress,
            streetaddress2,
            streetaddress3,
            city,
            state,
            zipcode,
            vendorcountrycode,
            vendor_state_code,
            vendor_cd,
            @dummy, -- congressionaldistrict,
            @dummy, -- vendorsitecode,
            @dummy, -- vendoralternatesitecode,
            dunsnumber,
            parentdunsnumber,
            phoneno,
            faxno,
            @dummy, -- registrationdate,
            @dummy, -- renewaldate,
            @dummy, -- mod_parent,
            @dummy, -- locationcode,
            @dummy, -- statecode,
            @dummy, -- pop_state_code,
            @dummy, -- placeofperformancecountrycode,
            @dummy, -- placeofperformancezipcode,
            @dummy, -- pop_cd,
            @dummy, -- placeofperformancecongressionaldistrict,
            psc_cat,
            productorservicecode,
            @dummy, -- systemequipmentcode,
            @dummy, -- claimantprogramcode,
            @dummy, -- principalnaicscode,
            @dummy, -- informationtechnologycommercialitemcategory,
            @dummy, -- gfe_gfp,
            @dummy, -- useofepadesignatedproducts,
            @dummy, -- recoveredmaterialclauses,
            @dummy, -- seatransportation,
            @dummy, -- contractbundling,
            @dummy, -- consolidatedcontract,
            @dummy, -- countryoforigin,
            @dummy, -- placeofmanufacture,
            @dummy, -- manufacturingorganizationtype,
            @dummy, -- agencyid,
            @dummy, -- piid,
            @dummy, -- modnumber,
            @dummy, -- transactionnumber,
            fiscal_year,
            @dummy, -- idvagencyid,
            @dummy, -- idvpiid,
            @dummy, -- idvmodificationnumber,
            @dummy, -- solicitationid,
            @dummy, -- extentcompeted,
            @dummy, -- reasonnotcompeted,
            @dummy, -- numberofoffersreceived,
            @dummy, -- commercialitemacquisitionprocedures,
            @dummy, -- commercialitemtestprogram,
            @dummy, -- smallbusinesscompetitivenessdemonstrationprogram,
            @dummy, -- a76action,
            @dummy, -- competitiveprocedures,
            @dummy, -- solicitationprocedures,
            @dummy, -- typeofsetaside,
            @dummy, -- localareasetaside,
            @dummy, -- evaluatedpreference,
            @dummy, -- fedbizopps,
            @dummy, -- research,
            @dummy, -- statutoryexceptiontofairopportunity,
            @dummy, -- organizationaltype,
            numberofemployees,
            annualrevenue )
        SET unique_transaction_id = UNHEX(@unique_transaction_id);

        ALTER TABLE raw_contracts ENABLE KEYS;
    """ % fileName.replace('\\','\\\\') )
    f.close()
    cmd = getMySqlCommand()+"<\""+tempScript+"\""
    os.system( cmd  )

def processRows():
    """
    Invokes process_contrcts_rows.sql to process loaded rows from the CSV file
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
