# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerindexItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    style = scrapy.Field()

class WineIndexItem(scrapy.Item):
    name = scrapy.Field()
    winetype  = scrapy.Field()
    year = scrapy.Field()
    volume = scrapy.Field()
    grape = scrapy.Field()
    alcohol = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    winery = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
