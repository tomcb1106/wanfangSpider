# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WanfangItem(scrapy.Item):
    Title = scrapy.Field()
    author = scrapy.Field()
    abstr = scrapy.Field()
    Volume = scrapy.Field()
    keyword = scrapy.Field()
    Source = scrapy.Field()
    maker = scrapy.Field()
    download = scrapy.Field()
    URL = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
