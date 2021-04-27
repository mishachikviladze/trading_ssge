# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags

def remove_whitespaces(field):
        return field.replace('\n',' ').replace('\t','').strip()

def make_full_URL(partialurt):
    return "https://www.ss.ge"+partialurt


def extract_numbers(field):
    return ''.join(char for char in field if char.isdigit())



class TraidingSsgeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    statement_date=scrapy.Field()
    new_or_used=scrapy.Field(output_processor = TakeFirst())
    location=scrapy.Field(input_processor=MapCompose(remove_whitespaces), output_processor = TakeFirst())
    last_updated=scrapy.Field(output_processor = TakeFirst())
    product=scrapy.Field(output_processor = TakeFirst())
    price=scrapy.Field(input_processor=MapCompose(extract_numbers), output_processor = TakeFirst())
    currency_symbol=scrapy.Field(output_processor = TakeFirst())
    applicant=scrapy.Field(output_processor = TakeFirst())
    current_app_url=scrapy.Field(output_processor = TakeFirst())
    all_apps_url=scrapy.Field(input_processor=MapCompose(make_full_URL), output_processor = TakeFirst())
    agent_or_person=scrapy.Field(output_processor = TakeFirst())
    number_of_apps=scrapy.Field(input_processor=MapCompose(extract_numbers), output_processor = TakeFirst())
    product_description=scrapy.Field(output_processor = TakeFirst())
    product_specification=scrapy.Field(output_processor = TakeFirst())
    product_condition_description=scrapy.Field(output_processor = TakeFirst())
    seen=scrapy.Field(output_processor = TakeFirst())
    app_id=scrapy.Field(output_processor = TakeFirst())
    phone=scrapy.Field(input_processor=MapCompose(extract_numbers), output_processor = TakeFirst())



  