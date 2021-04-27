# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

from scrapy.exporters import CsvItemExporter
class TraidingSsgePipeline:

    def __init__(self): 
        self.file = open(f"data/trading_ssge/{yesterday}-data_export.csv", 'wb') 
        self.exporter = CsvItemExporter(self.file) 
        # self.exporter.fields_to_export = ['APP_ID','statement_date', 'owner', 'owner_type', 'phone', 'owner_statements','statements_count','current_staytement_url','address', 'amount_GEL', 'amount_USD', 'square','rooms', 'badrooms', 'floor', 'other_characteristics']
        self.exporter.start_exporting()
    
    def close_spider(self, spider): 
        self.exporter.finish_exporting() 
        self.file.close()

    def process_item(self, item, spider): 
        self.exporter.export_item(item) 
        return item