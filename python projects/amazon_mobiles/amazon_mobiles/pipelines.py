# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class AmazonMobilesPipeline:
    def createconnection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'scrapy'
        )
    def create_table(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS amobiles")
        self.cursor.execute("CREATE TABLE amobiles( id int  AUTO_INCREMENT PRIMARY KEY,title text,price varchar(20))")
    
    def __init__(self):
        self.createconnection()
        self.create_table()
    def store_db(self,item):      
        self.cursor.execute("INSERT INTO amobiles VALUES (NULL,%s,%s)",(item['title'],item['price']))
        self.conn.commit()
    def process_item(self, item, spider):
        # print(item['title'],end='')
        self.store_db(item)
        return item
