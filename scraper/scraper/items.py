# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoaItem(scrapy.Item):
    """
    e.g.)
        "name": "XX전자 선풍기", 상품명
        "site": "hmall", 쇼핑사 명
        "price": 53000,  가격 정보
        "imageUrl": "https://www.example.com/example.jpg", 대표 이미지 URL
        "imageHashes": [ ... ]
    """
    name = scrapy.Field()
    site = scrapy.Field()
    price = scrapy.Field()
    imageUrl = scrapy.Field()
    imageHashes = scrapy.Field()