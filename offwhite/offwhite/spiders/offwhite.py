import scrapy
from ..items import ProductLoader, PriceLoader, PriceParamsLoader
from urllib.parse   import quote
from scrapy.selector import Selector

my_h = {
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64;"
        + "rv:57.0) Gecko/20100101 Firefox/57.0"
        }

base_url = 'https://www.off---white.com'

class OffSpider(scrapy.Spider):
    name = 'offwhite'

    def __init__(self, url):
        super(OffSpider, self).__init__()
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url,
                             headers=my_h,
                             callback=self.parse)

    def parse(self, response):
        categories = response.xpath('//h3[contains(text(), "Categories")]/'
                              + 'following-sibling::ul//label/text()').extract()
        numbas = response.xpath('//h3[contains(text(), "Categories")]/'
                              + 'following-sibling::ul//label/preceding-sibling::input/@value').extract()
#        for item in numbas:
#            yield scrapy.Request(url=self.url+"?utf8=%E2%9C%93&f%5Bcategories%5D%5B%5D="+item,
#            callback=self.parse_category, headers=my_h)
        yield scrapy.Request(url=self.url+"?utf8=%E2%9C%93&f%5Bcategories%5D%5B%5D="+numbas[5], callback=self.parse_category,
                             headers=my_h)

    def parse_category(self, response):
        items = response.xpath('//section[@class="products"]/article/a/@href').extract()

        for item in items:
            yield scrapy.Request(url=base_url+item, headers=my_h, callback=self.parse_shmotka)
#        yield scrapy.Request(url=base_url+items[0], headers=my_h, callback=self.parse_shmotka)

    def parse_shmotka(self, response):
        productloader = ProductLoader(selector=Selector(response))
        priceloader = PriceLoader(selector=Selector(response))

        productloader.add_xpath('name', '//header/span[@class="prod-title"]/text()')
#        cheto['brand'] = response.xpath('//div[@class="product-description"]/p[@itemprop="brand"]/text()').extract()
        productloader.add_xpath('categories', '//header/span[@class="prod-subtitle"]/text()')
        productloader.add_xpath('description', '//p[@id="details"]/@content')
        productloader.add_xpath('material', '//div[@class="product-description"]/ul/li[contains(text(), "Material")]/text()')
        productloader.add_value('url', response.url)
        productloader.add_xpath('images', '//nav[contains(@class, "thumbnails")]//img/@src')
        productloader.add_value('site', base_url)
        productloader.add_xpath('site_product_id', '//section[@id="content"]/article/@id')
        priceloader.add_xpath('site_product_id', '//section[@id="content"]/article/@id')
        params = self.get_price_params(response)
        priceloader.add_value('params', params)

#        priceloader.add_xpath('stock_level', '//form[contains(@class, "product-cart-form")]/p[@class="available-items"]/text()')
        stock = response.xpath('//form[contains(@class, "product-cart-form")]/p[@class="available-items"]/text()').extract() or \
             response.xpath('//div[contains(@class, "availability")]/text()').extract()
        priceloader.add_value('stock_level', stock)

        priceloader.add_xpath('currency', '//div[@class="price"]/span[@itemprop="priceCurrency"]/@content')
        priceloader.add_value('date', 'today')

        yield productloader.load_item()
        yield priceloader.load_item()

    def get_price_params(self, response):
        paramsloader = PriceParamsLoader(selector=Selector(response))
        paramsloader.add_xpath('size','//div[@class="styled-radio"][not(@hidden)]/label/text()')
        color = response.xpath('//div[@class="product-description"]//li[contains(text(), "Color")]/text()').extract_first()
        if color:
            color = color.split(":")[1]
        paramsloader.add_value('color', color)
        paramsloader.add_xpath('price','//div[@class="price"]/span[@itemprop="price"]/@content')
        return paramsloader.load_item()

    def okkie(self, response):
        yield {"ok":"done"}
