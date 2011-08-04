import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
from BeautifulSoup import BeautifulSoup


class Crawler( QWebPage ):
	def __init__(self, url, file):
		QWebPage.__init__( self )
		self._url = url
		self._file = file
 
	def crawl( self ):
		signal.signal( signal.SIGINT, signal.SIG_DFL )
		self.connect( self, SIGNAL( 'loadFinished(bool)' ), self._finished_loading )
		self.mainFrame().load( QUrl( self._url ) )
 
	def _finished_loading( self, result ):
		file = open( self._file, 'w' )
		file.write( self.mainFrame().toHtml() )
		file.close()
		sys.exit( 0 )

def main():
	
	baseUrl = 'http://www.regulations.gov'
	url = 'http://www.regulations.gov/#!searchResults;rpp=10;po=0'
	
	app = QApplication( sys.argv )
	
	crawler = Crawler(url)
	crawler.crawl()
	
	r = Render(url)
	html = r.frame.toHtml()
	# use BeautifulSoup to cycle through each regulation
	soup = BeautifulSoup(html)
	
	print soup
	
	regs = soup.find('div',{'class':'x-grid3-body'}).findAll('a')
	
	# cycle through list and call up each page separately
	for reg in regs:
		link = baseUrl + reg['href']
		link = str(link)
		# use Qt to load each regulation page
		r = r.mainFrame().load(QUrl(link))
		r.frame = r.mainFrame()
		
		html = r.frame.toHtml() # get actual rendered web page
		
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

if __name__ == '__main__':
	main()