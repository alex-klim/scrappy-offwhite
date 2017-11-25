import scrapy
from ..items import Product, Price
from ..utils import strippin


base_url = 'https://www.off---white.com'

class OffSpider(scrapy.Spider):
    name = 'offwhite'

    def __init__(self, url):
        super(OffSpider, self).__init__()
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url,
                             callback=self.parse)

    def parse(self, response):
        categories = response.xpath('//h3[contains(text(), "Categories")]/'
                              + 'following-sibling::ul//label/text()').extract()
        numbas = response.xpath('//h3[contains(text(), "Categories")]/'
                              + 'following-sibling::ul//label/preceding-sibling::input/@value').extract()
        for item in numbas:
            yield scrapy.Request(url=self.url+"?utf8=%E2%9C%93&f%5Bcategories%5D%5B%5D="+item,
            callback=self.parse_category)

    def parse_category(self, response):
        items = response.xpath('//section[@class="products"]/article/a/@href').extract()

        for item in items:
            yield scrapy.Request(url=base_url+item, callback=self.parse_shmotka)

    def parse_shmotka(self, response):
        product = Product()
        price = Price()

        name = response.xpath('//header/span[@class="prod-title"]/text()').extract_first()
        product['name'] = strippin(name)
        categories = response.xpath('//header/span[@class="prod-subtitle"]/text()').extract_first()
        product['categories'] = strippin(categories)
        description = response.xpath('//p[@id="details"]/@content').extract_first()
        product['description'] = strippin(description)
        material = response.xpath('//div[@class="product-description"]/ul/li[contains(text(), "Material")]/text()').extract_first()
        product['material'] = strippin(material)
        product['url'] = response.url
        images = response.xpath('//nav[contains(@class, "thumbnails")]//img/@src').extract()
        product['images'] = images
        product['site'] = base_url
        site_product_id = response.xpath('//section[@id="content"]/article/@id').extract_first()
        product['site_product_id'] = strippin(site_product_id)
        price['params'] = {}
        price['site_product_id'] = strippin(site_product_id)
        stock = response.xpath('//form[contains(@class, "product-cart-form")]/p[@class="available-items"]/text()').extract_first() or \
             response.xpath('//div[contains(@class, "availability")]/text()').extract_first()
        price['stock_level'] = strippin(stock)
        currency = response.xpath('//div[@class="price"]/span[@itemprop="priceCurrency"]/@content').extract_first()
        price['currency'] = strippin(currency)
        price['date'] = 'today'

        pprice = response.xpath('//div[@class="price"]/span[@itemprop="price"]/@content').extract_first()
        price['params']['price'] = strippin(pprice)
        psize = response.xpath('//div[@class="styled-radio"][not(@hidden)]/label/text()').extract()
        price['params']['size'] = psize
        color = response.xpath('//div[@class="product-description"]//li[contains(text(), "Color")]/text()').extract_first()
        if color:
            color = color.strip().split(":")[1]

        price['params']['color'] = color

        yield product
        yield price

