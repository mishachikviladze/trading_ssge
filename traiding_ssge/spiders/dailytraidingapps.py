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
        # yield {'მისამართი': response.url}
        print('მიღებული მისამართია'+'=====================================================================================>'+response.url)
        yield {
        'მდგომარეობა': response.xpath("normalize-space(//div[@class='condition']/text())").get(),
        'მდებარეობა': response.xpath("normalize-space(//div[@class='location-time']/div[2]/p/span/text())").get(),
        'ბოლო განახლების თარიღი': response.xpath("normalize-space(//div[@class='location-time']/div[2]/descendant::span[2]/text())").get(),
        'პროდუქტის დასახელება': response.xpath("normalize-space(//h2[@class='main-title']/text())").get(),
        'ფასი': response.xpath("normalize-space(//div[@class='market-item-price ']/text())").get(),
        'ვალუტის სიმბოლო': response.xpath("normalize-space(//div[@class='market-item-price ']/span/text())").get(),
        'განმცხადებელი': response.xpath("normalize-space(//div[@class='author_type']/text())").get(),
        'მიმდინარე განცხადების ლინკი': response.url,
        'ყველა განცხადების ლინკი': "https://www.ss.ge"+response.xpath("normalize-space(//div[@class='author_type']/descendant::span/a/@href)").get(),
        'აგენტი თუ კერძო პირი': response.xpath("normalize-space((//div[@class='author_type'])[1]/span/a/text())").get(),
        'სულ განცხადებათა რაოდენობა': response.xpath("normalize-space(//div[@class='author_type']/descendant::span[2]/text())").get(),
        'პროდუქტის აღწერილობა': response.xpath("normalize-space(//span[@class='details_text']/text())").get(),
        'პროდუქტის სპეციფიკაცია': response.xpath("normalize-space(//div[@class='jobs_details']/span/text())").get(),
        'პროდუქტის მდგომარეობის აღწერილობა': response.xpath("normalize-space(//div[@class='jobs_details'][2]/span[2]/text())").get(),
        'დათვალიერებათა რაოდენობა': response.xpath("normalize-space(//div[@class='article_views']/span/text())").get(),
        'განცხადების ნომერი': response.xpath("normalize-space(//div[@class='market-item-id']/span/text())").get(),
        'ტელეფონი': response.xpath("normalize-space(//div[@class='numbers-wrap']/a/@href)").get(),
        }

        # 'text': response.xpath("").get()


