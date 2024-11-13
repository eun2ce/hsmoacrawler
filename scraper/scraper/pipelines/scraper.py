# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os

from scrapy.utils.project import get_project_settings


class ScraperPipeline(object):
    def __init__(self):
        data_dir = get_project_settings().get("DATA_DIR")
        file_name = get_project_settings().get("PRODUCT_NAME")

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        self.file = codecs.open(os.path.join(data_dir, f"{file_name}"), "w", encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
