from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from regulations.items import RegulationItem

class RegulationSpider(BaseSpider):
    name = 'regulations'
    allowed_domains = ['regulations.gov']

    #
    # setup the initial request to begin the spidering process
    #
    def start_requests(self):
        regulationsRequest = Request("http://www.regulations.gov/#!searchResults;rpp=100;po=0",callback=self.parseRegulations)


        #return [regulationsRequest]

    #
    # scrape, parse all regulations
    # also catch any dockets
    #
    def parseRegulations(self,response):
        hxs = HtmlXPathSelector(response)

        regulationsList = hxs.select('/div[@class="x-grid3-body"]/div/table/tr/td/div/div/div/a[@href]').extract()

        for i in range(len(regulationsList)):

            yield Request('http://www.regulations.gov/#!documentDetail;D='+regulationsList[i],callback=self.parseRegulation)


    def parseRegulation(self,response):
        hxs = HtmlXPathSelector(response)

        id = hxs.select('/div[@id="mainContentTop"/span[@class="gwt-InlineLabel"/text()')

        docket = hxs.select('/div[@id="mainContentTop"]/span[text() = "Docket ID:"]/following-sibling::div/a/text()').extract()

        item = RegulationItem()
        item['documentID'] = id
        item['docketID'] = docket

        fields = {'Document Title:':'documentTitle','Document Type:':'documentType','Document Sub-Type:':'documentSubType','Start/End Page:':'pages','Author Date:':'authorDate','Receipt Date:':'receiptDate','FR Publish Date:':'frDate','Comment Start Date:':'commentStart','Comment End Date:':'commentEnd','Postmark Date:': 'postmarkDate','Media:':'media','Page Count:':'pageCount'}

        for k,v in fields.iteritems():
            item[v] = hxs.select('/div[@id="mainContentBottom"]/table/tr/td/div/table/tr/td[text() = "'+k+'"/following-sibling::td/text()').extract()

        yield item

        



SPIDER = RegulationSpider()