# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RegulationItem(Item):

    documentID = Field()
    docketID = Field()
    documentTitle = Field()
    documentType = Field()
    documentSubType = Field()
    pages = Field()
    authorDate = Field()
    receiptDate = Field()
    frDate = Field()
    commentStart = Field()
    commentEnd = Field()
    postmarkDate = Field()
    media = Field()
    pageCount = Field()

    pass
