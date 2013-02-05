# Scrapy settings for mininova project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

#BOT_NAME = 'mininova'

SPIDER_MODULES = ['mininova.spiders']
NEWSPIDER_MODULE = 'mininova.spiders'
DEFAULT_ITEM_CLASS = 'mininova.items.TorrentItem'
ITEM_PIPELINES = ['mininova.pipelines.FilterWordsPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mininova (+http://www.yourdomain.com)'
