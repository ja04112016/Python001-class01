import scrapy
from scrapy.selector import Selector
from myspiders.items import MaoyanMovieItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com']
    def start_requests(self):
        url = f'{self.start_urls[0]}/films?showType=3'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath("//div[@class='movie-hover-info']")[:10]
        items = []
        for movie in movies:
            movie_title = movie.xpath('div[1]/@title').extract_first()
            movie_type = movie.xpath('div[2]/text()').extract()[-1].strip()
            movie_release = movie.xpath('div[4]/text()').extract()[-1].strip()
            item = MaoyanMovieItem()
            item["movie_title"] = movie_title
            item["movie_type"] = movie_type
            item["movie_release"] = movie_release
            items.append(item)
            print()
        return items
