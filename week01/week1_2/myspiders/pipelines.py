# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
headers = ["movie_title", "movie_type", "movie_release"]

class MyspidersPipeline:
    def process_item(self, item, spider):
        with open('./question2.csv', "a+", encoding="utf-8") as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writerow(item)
        return item
