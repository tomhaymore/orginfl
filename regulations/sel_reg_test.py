# import modules
from selenium import selenium
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import argparse
import time, re, csv

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
    parser = argparse.ArgumentParser(description='Regulations Data Import')
    parser.add_argument( '-q', '--quota', help='Quota', default=50)

    args = parser.parse_args()
    return args

def main():
    args = getArgs()
    filename = 'regulations.csv'
    baseUrl = 'http://www.regulations.gov/'

    # initialize selenium
    sel = selenium("localhost", 4444, "*firefox", "http://www.regulations.gov/")
    sel.start()

    sel.open("http://www.regulations.gov/#!documentDetail;D=NOAA-2005-0001-0001")

    html = sel.get_body_text()

    print html

    # close down selenium
    sel.stop()

if __name__ == '__main__':
    main()
