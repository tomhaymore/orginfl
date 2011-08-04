# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import csv
import items

class RegulationsPipeline(object):

    def __init__(self):
        self.regFile = csv.writer(open('regulations.csv','wb'))
        self.regFile.writerow(['documentID','docketID','documentTitle','documentType','documentSubType','pages','authorDate','receiptDate','frDate','commentStart','commentEnd','postmarkDate','media','pageCount'])

    def process_item(self, item, spider):
        self.regFile.writerow(item['documentID'],item['docketID'],item['documentTitle'],item['documentType'],item['documentSubType'],item['pages'],item['authorDate'],item['receiptDate'],item['frDate'],item['commentStart'],item['commentEnd'],item['postmarkDate'],item['media'],item['pageCount'])
        return item
