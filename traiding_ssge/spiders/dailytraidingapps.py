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
            # print("---------------------------------------------------------------------------------------------------Semdegi gverdi moiZebna", next_page_url, self.page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_application(self, response):
        # yield {'მისამართი': response.url}
        print('მიღებული მისამართია'+'=====================================================================================>'+response.url)
        yield {
        'new_or_used': response.xpath("normalize-space(//div[@class='condition']/text())").get(),
        'location': response.xpath("normalize-space(//div[@class='location-time']/div[2]/p/span/text())").get(),
        'last_updated': response.xpath("normalize-space(//div[@class='location-time']/div[2]/descendant::span[2]/text())").get(),
        'product': response.xpath("normalize-space(//h2[@class='main-title']/text())").get(),
        'price': response.xpath("normalize-space(//div[@class='market-item-price ']/text())").get(),
        'currency symbol': response.xpath("normalize-space(//div[@class='market-item-price ']/span/text())").get(),
        'applicant': response.xpath("normalize-space(//div[@class='author_type']/text())").get(),
        'current_app_url': response.url,
        'all_apps_url': "https://www.ss.ge"+response.xpath("normalize-space(//div[@class='author_type']/descendant::span/a/@href)").get(),
        'agent_or_person': response.xpath("normalize-space((//div[@class='author_type'])[1]/span/a/text())").get(),
        'number_of_apps': response.xpath("normalize-space(//div[@class='author_type']/descendant::span[2]/text())").get(),
        'product_description': response.xpath("normalize-space(//span[@class='details_text']/text())").get(),
        'product_specification': response.xpath("normalize-space(//div[@class='jobs_details']/span/text())").get(),
        'product_condition_description': response.xpath("normalize-space(//div[@class='jobs_details'][2]/span[2]/text())").get(),
        'seen': response.xpath("normalize-space(//div[@class='article_views']/span/text())").get(),
        'app_id': response.xpath("normalize-space(//div[@class='market-item-id']/span/text())").get(),
        'phone': response.xpath("normalize-space(//div[@class='numbers-wrap']/a/@href)").get(),
        }

        # 'text': response.xpath("").get()


