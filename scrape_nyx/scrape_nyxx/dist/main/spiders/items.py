# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeNyxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    old_cost = scrapy.Field()
    new_price = scrapy.Field()
    link = scrapy.Field()
    picture = scrapy.Field()
