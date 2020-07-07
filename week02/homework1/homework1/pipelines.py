# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Homework1Pipeline:
    def open_spider(self, spider):
        print("连接数据库")
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        user = spider.settings.get('MYSQL_USER', 'scrapy')
        passwd = spider.settings.get('MYSQL_PASSWD', '5j0878ok')
        dbname = spider.settings.get('MYSQL_DBNAME', 'bookstore')
        try:
            self.cli = pymysql.connect(host, user=user, password=passwd, db=dbname)
            self.cursor = self.cli.cursor()
        except Exception as err:
            raise Exception(f"数据库连接异常{err}")

    def close_spider(self, spider):
        print("断开数据库")
        self.cli.close()

    def process_item(self, item, spider):
        print("插入数据")
        self._intert_data("books", item)
        return item

    def _intert_data(self, table_name, item):
        data_dict = {k:v for k, v in item.items()}
        data_dict["table_name"] = table_name
        sql = 'insert into {table_name} (book_name, book_price, book_stars) values("{title}", "{price}", "{stars}")'
        try:
            self.cursor.execute(sql.format(**data_dict))
            self.cli.commit()
        except Exception as err:
            raise Exception(f"数据库写入失败{err}")
