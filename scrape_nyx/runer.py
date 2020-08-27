import scrapy
import os
import sys


from  scrape_nyx.spiders import nyx_spider
from scrapy.crawler import CrawlerProcess

import os
def start_scrape():

    path = os.path.abspath('') + '\data.json'
    if os.path.exists(path):
        os.remove(path)



    process = CrawlerProcess(settings={
    "FEEDS": {
        "data.json": {"format": "json"},
    },
})

    process.crawl(nyx_spider.PricesSpider)
    process.start()

