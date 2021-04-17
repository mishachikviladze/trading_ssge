import scrapy
from datetime import datetime, timedelta


class DailytraidingappsSpider(scrapy.Spider):
    name = 'dailytraidingapps'
    allowed_domains = ['www.ss.ge']
    start_urls = ['https://www.ss.ge/ka/sales/list?Page=1']
    page=1
    irrelevantpages=0
    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    def parse(self, response):
        links = response.xpath("//div[@class='latest_desc']/div/a/@href")
        URLS = []
        for i in links:
            URLS.append("https://www.ss.ge"+i.get())

        daystrings = response.xpath("//div[@class='rubrucsPostTime']/div/span[2]/text()")
        days = []
        for i in daystrings:
            days.append(i.get())
        
        for url, day in zip(URLS, days):
            if "გუშინ" in day:
                # print(url +'--------------------------------------------------------------------------------------------->' + day)
                self.irrelevantpages=0
                yield scrapy.Request(url=url, callback=self.parse_application, meta={'appdate':self.yesterday})

        self.page = self.page + 1
        self.irrelevantpages+=1
        next_page_url = f'https://www.ss.ge/ka/sales/list?Page={self.page}'
        next_page = scrapy.Request(url=next_page_url)
        if (next_page and self.irrelevantpages<7):  
            print("---------------------------------------------------------------------------------------------------Semdegi gverdi moiZebna", next_page_url, self.page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_application(self, response):
        pass
        # print('მიღებული მისამართია'+'=====================================================================================>'+response.url)