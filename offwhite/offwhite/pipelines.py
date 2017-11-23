# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .tasks import add_product, add_price
from .items import Price, Product


class OffwhitePipeline(object):
    def process_item(self, item, spider):
        if type(item) is Product:
            add_product.delay(dict(item))
        if type(item) is Price:
            add_price.delay(dict(item))
        return item
