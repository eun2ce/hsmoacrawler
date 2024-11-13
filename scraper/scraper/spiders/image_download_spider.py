import json
import os
from typing import Any

import scrapy
from scrapy import Spider
from scrapy.http import Response
from scrapy.utils.project import get_project_settings

from .. import items


class ImageDownloadSpider(Spider):
    name = "image_download_spider"

    custom_settings = {
        "ITEM_PIPELINES": {"scraper.pipelines.image.ImagePipeline": 500},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self.products = self.get_produects()
        self.start_urls = [item["imageUrl"] for _, item in enumerate(self.products)]
        self.image_data_dir = self.settings.get("IMAGE_DATA_DIR")

        if not os.path.exists(self.image_data_dir):
            os.makedirs(self.image_data_dir)

        self.count = 0

    def get_produects(self):
        data_dir = self.settings.get("DATA_DIR")
        product_file_name = self.settings.get("PRODUCT_JSON_FILE")

        # ~/project root/data/products.json
        product_path = os.path.join(data_dir, product_file_name)
        contents = open(product_path, "r", encoding="utf-8").read()
        items = [json.loads(str(item)) for item in contents.strip().split('\n')]

        return items

    def start_requests(self):
        for prod in self.products:
            yield scrapy.Request(prod["imageUrl"], meta={"product": prod})

    def parse(self, response: Response, **kwargs: Any):
        file_name = self.settings.get("IMAGE_FILE_FMT") % self.count

        path = os.path.join(self.image_data_dir, file_name)
        with open(path, 'wb') as f:
            f.write(response.body)
        self.count += 1
        item = items.MoaItem(response.meta.get("product"))
        item["imageHashes"] = [path] # pipeline 에 경로를 전달하고, 값을 구하면 덮어쓴다.
        yield item
