import scrapy
from datetime import datetime, timedelta
from itemloaders import ItemLoader
from ..items import TraidingSsgeItem


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
            # print("---------------------------------------------------------------------------------------------------Semdegi gverdi moiZebna", next_page_url, self.page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_application(self, response):
        loader = ItemLoader(item = TraidingSsgeItem(), selector=response)
        loader._add_value('statement_date', response.request.meta['appdate'])
        loader.add_xpath('new_or_used', "normalize-space(//div[@class='condition']/text())")
        loader.add_xpath('location', "//div[@class='location-time']/div[2]/p/span/text()")
        loader.add_xpath('last_updated', 'normalize-space(//div[@class="location-time"]/div[2]/descendant::span[2]/text())')
        loader.add_xpath('product', "normalize-space(//h2[@class='main-title']/text())")
        loader.add_xpath('price', "normalize-space(//div[@class='market-item-price ']/text())")
        loader.add_xpath('currency_symbol', "normalize-space(//div[@class='market-item-price ']/span/text())")
        loader.add_xpath('applicant', "normalize-space(//div[@class='author_type']/text())")
        loader.add_value('current_app_url', response.url)
        loader.add_xpath('all_apps_url', "//div[@class='author_type']/descendant::span/a/@href")
        loader.add_xpath('agent_or_person', "normalize-space((//div[@class='author_type'])[1]/span/a/text())")
        loader.add_xpath('number_of_apps', "normalize-space(//div[@class='author_type']/descendant::span[2]/text())")
        loader.add_xpath('product_description', "normalize-space(//span[@class='details_text']/text())")
        loader.add_xpath('product_specification', "normalize-space(//div[@class='jobs_details']/span/text())")
        loader.add_xpath('product_condition_description', "normalize-space(//div[@class='jobs_details'][2]/span[2]/text())")
        loader.add_xpath('seen', "normalize-space(//div[@class='article_views']/span/text())")
        loader.add_xpath('app_id', "normalize-space(//div[@class='market-item-id']/span/text())")
        loader.add_xpath('phone', "normalize-space(//div[@class='numbers-wrap']/a/@href)")
        print(loader.item)
        yield loader.load_item()


