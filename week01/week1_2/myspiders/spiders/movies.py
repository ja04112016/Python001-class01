import scrapy
# from bs4 import BeautifulSoup as bs
from scrapy.selector import Selector
from myspiders.items import MyspidersItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']

    def start_requests(self):
        for i in range(10):
            yield scrapy.Request(f"{self.start_urls[0]}top250?start={i*25}&filter=", callback=self.parse)

    def parse(self, response):
        all_movies = Selector(response=response).xpath("//div[@class='hd']")
        for movie in all_movies:
            title = movie.xpath('a/span/text()').extract_first().strip()
            url = movie.xpath('a/@href').extract_first().strip()
        # bs_info = bs(response.text, "html.parser")
        # all_title_url = bs_info.find_all("div", attrs={"class": "hd"})
        # # items = []
        # for b in all_title_url:
        #     title = b.a.find("span").text
        #     url = b.a.get("href")
            item = MyspidersItem()
            item["title"] = title
            item["url"] = url
            yield scrapy.Request(url, callback=self.parse2, meta={"item": item})

    def parse2(self, response):
        item = response.meta["item"]
        movie_detail = Selector(response=response).xpath('//div[@class="related-info"]')
        for md in movie_detail:
            summary_title = md.xpath("h2/i/text()").extract_first()
            summary = [i.strip() for i in md.xpath("div/span[@class='all hidden']/text()").extract()]
            if not summary:
                summary = [i.strip() for i in md.xpath("div/span[@property='v:summary']/text()").extract()]
            item["summary"] = '{}\n{}\n\n\n'.format(summary_title, "".join(summary))
            # print(f'{summary_title}\n{summary}')
    #     bs_info = bs(response.text, 'html.parser')
    #     summary = bs_info.find("div", attrs={"class": "related-info"}).get_text().strip()
    #     item["summary"] = summary
            return item




