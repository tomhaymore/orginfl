# Scrapy settings for regulations project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'regulations'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['regulations.spiders']
NEWSPIDER_MODULE = 'regulations.spiders'
DEFAULT_ITEM_CLASS = 'regulations.items.RegulationsItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

