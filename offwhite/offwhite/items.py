# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

class Product(scrapy.Item):
    site_product_id = scrapy.Field()
    name = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    material = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    site = scrapy.Field()

class Price(scrapy.Item):
    site_product_id = scrapy.Field()
    params = scrapy.Field()
    stock_level = scrapy.Field()
    currency = scrapy.Field()
    date = scrapy.Field()

