# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    title = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()

class MaoyanMovieItem(scrapy.Item):
    movie_title = scrapy.Field()
    movie_type = scrapy.Field()
    movie_release = scrapy.Field()

