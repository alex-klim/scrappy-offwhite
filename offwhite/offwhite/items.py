# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst
clean_text = Compose(MapCompose(lambda v: v.strip()), Join())
to_int = Compose(TakeFirst(), int)
to_dict = lambda k,iterable: iterable[0]

class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site_product_id = scrapy.Field()
    name = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    material = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    site = scrapy.Field()

class ProductLoader(ItemLoader):
    default_item_class = Product

    site_product_id_out = clean_text
    name_out = clean_text
    categories_out = clean_text
    description_out = clean_text
    material_out = clean_text
    url_out = clean_text
    images_out = clean_text
    site_out = clean_text

class PriceParams(scrapy.Item):
    price = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()


class Price(scrapy.Item):
    site_product_id = scrapy.Field()
    params = scrapy.Field(serializer=PriceParams)
    stock_level = scrapy.Field()
    currency = scrapy.Field()
    date = scrapy.Field()

class PriceLoader(ItemLoader):
    default_item_class = Price

    site_product_id_out = clean_text
    stock_level_out = clean_text
    currency_out = clean_text
    date_out = clean_text
    params_out = to_dict

#class PriceParams(scrapy.Item):
#    price = scrapy.Field()
#    color = scrapy.Field()
#    size = scrapy.Field()

class PriceParamsLoader(ItemLoader):
    default_item_class = PriceParams

    color_out = clean_text
    size_out = clean_text
    price_out = clean_text

