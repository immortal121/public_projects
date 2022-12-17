import scrapy
from ..items import *
class amazon_spider(scrapy.Spider):
    # https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&fs=true&page=2&qid=1669625019&ref=sr_pg_2
    # https://www.amazon.in/s?rh=n%3A1389432031&fs=true&ref=lp_1389432031_sar
    name = 'amazon_mobiles'
    start_urls = [
        'https://www.amazon.in/s?rh=n%3A1389432031&fs=true&ref=lp_1389432031_sar'
    ]

    page_no = 2
    def parse(self,response):
        
        items = AmazonMobilesItem()
        title = response.css('.a-size-base-plus::text').extract()
        for i in range(len(title)): 
            items['title'] = response.css('.a-size-base-plus::text')[i].extract()
            items['price'] = response.css('.a-price-whole::text')[i].extract()
            yield items
       
       
        local = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&fs=true&page="+str(amazon_spider.page_no)+"&qid=1669636293&ref=sr_pg_"+str(amazon_spider.page_no)+""  
        if amazon_spider.page_no < 10:
            amazon_spider.page_no +=1
            
            print('------------------------------')
            yield response.follow(local,callback = self.parse)
            
        


        