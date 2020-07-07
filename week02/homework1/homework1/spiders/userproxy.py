import scrapy
from ..items import Homework1Item

stars_map = {
    "One": "*",
    "Two": "**",
    "Three": "***",
    "Four": "****",
    "Five": "*****",
}

class UserproxySpider(scrapy.Spider):
    name = 'userproxy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//section/div[2]/ol/li/article')
        for book in books:
            item = Homework1Item()
            title = book.xpath('h3/a/@title').extract_first()
            price = book.xpath('div[@class="product_price"]/p/text()').extract_first()
            stars = book.xpath('p/@class').extract_first().split(' ')[-1]
            item['title'] = title
            item['price'] = price
            item['stars'] = stars_map[stars]
            yield item


