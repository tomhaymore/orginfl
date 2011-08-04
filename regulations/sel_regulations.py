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

    # get actual web page using selenium
    
    sel.open('http://www.regulations.gov/#!searchResults;rpp='+str(args.quota)+';po=0')
    # sel.wait_for_page_to_load('3000')
    
    html = sel.get_html_source() # get actual rendered web page

    print html

    # use BeautifulSoup to cycle through each regulation
    soup = BeautifulSoup(html)

    regs = soup.find('div',{'class':'x-grid3-body'}).findAll('a')

    # cycle through list and call up each page separately
    for reg in regs:
        link = baseUrl + reg['href']
        link = str(link)
        # use Selenium to load each regulation page
        sel.open(link)
        # sel.wait_for_page_to_load('3000')
        html = sel.get_html_source() # get actual rendered web page

        # use BeautifulSoup to assign each value to a variable
        soup = BeautifulSoup(html)
        docid = soup.find('span',id="rrspan1").findNext('span').contents
        docketid = soup.find('span',id='rrspan2').findNext('a').contents
        info = []
        info.append({'name':'DocumentID','value':docid})
        info.append({'name':'DocketID','value':docketid})

        s = soup.find('table',id='rrtable3').find('tr')

        while getattr(s,'name',None) != None:
            name = s.findAll('td')[0].span.contents
            name = str(name[0])
            name = re.sub(r'[\s+\:\\\-\/]','',name)
            value = s.findAll('td')[1].contents
            info.append({'name':name,'value':str(value[0])})
            s = s.nextSibling

        # grab actual text of document

        doclink = str(soup.findAll('iframe')[3]['src'])

        if doclink != None:
            doc = urlopen(doclink).read()

            doclinkid = re.search('(?<=objectId\=)\w*(?=\&)',doclink)

            doclinkid = doclinkid.group(0)

        # write variables to row in csv file

        fields = ['DocumentID','DocketID','RIN','DocumenTitle','OtherIdentifier','CFRCitation','FRDocketNumber','Abstract','DocumentType','DocumentSubtype','Startendpage','PostDate','AuthorDate','AuthorDocumentDate','ReceivedFilingDate','ReceiptDate','FRPublishDate','CommentStartDate','CommentEndDate','CommentsDue','PostmarkDate','DocumentLegacyID','Media','PageCount']

        row = []

        for f in fields:
            for i in info:
                if i['name'] == f:
                    row.append(i['value'])
                else:
                    row.append('')

        if doclinkid != None:
            row.append(doclinkid)
        else:
            row.append('')

        f = open(filename,'wb')
        c = csv.writer(f,delimiter=',')
        c.writerow(row)
        f.close()

        if doc != None:
            f = open(doclinkid,'wb')
            f.write(doc)
            f.close()

    # close down selenium
    sel.stop()

if __name__ == '__main__':
    main()
