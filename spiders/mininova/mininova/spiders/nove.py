from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from mininova.items import TorrentItem

from scrapy.contrib.spiders import *
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class MininovaSpider(BaseSpider):

    name = 'nova'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse(self, response):
        x = HtmlXPathSelector(response)

        torrent = TorrentItem()
        torrent['url'] = response.url
        torrent['name'] = x.select("//h1/text()").extract()
        torrent['description'] = x.select("//div[@id='description']").extract()
        torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
        return torrent
