from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from scrapy import Spider

from .. import items


class MoaSpider(Spider):
    name = "moa_spider"
    allowed_domains = ["hsmoa.com"]

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {"scraper.middlewares.SeleniumMiddleware": 543},
        "ITEM_PIPELINES": {"scraper.pipelines.scraper.ScraperPipeline": 300},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.start_urls:
            today = datetime.now()
            start = today - timedelta(days=5)
            end = today + timedelta(days=7)

            dates, base_hour_dates = [], []
            for x in range(((end + timedelta(days=1)) - start).days):
                date = (start + timedelta(days=x))
                dates.append(date.strftime("%Y-%m-%d"))
                yesterday = date - timedelta(days=1)
                base_hour_dates.append(yesterday.strftime("%Y-%m-%d"))

            # self.start_urls = [
            #     "https://hsmoa.com/?time=2024-11-13&time_size=2&direction=down&base_hour_datetime=2024-11-12T23%3A59%3A00%2B09%3A00"]
            self.start_urls = [
                f"https://hsmoa.com/?time={date}&time_size=2&direction=down&base_hour_datetime={base_hour_date}T23%3A59%3A00%2B09%3A00"
                for date, base_hour_date in zip(dates, base_hour_dates)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        names, img_urls, sites, prices = [], [], [], []

        site_tags = soup.select(
            "div.border-b.border-gray-100 > div > div.cursor-pointer > div > div > div > div.items-center > img")
        for tag in site_tags:
            sites.append(tag["alt"])

        price_tags = soup.select(
            "div.border-b.border-gray-100 > div > div.cursor-pointer > div > div > div > span.font-bold")
        for tag in price_tags:
            prices.append(tag.text)

        image_tags = soup.select(
            "div.border-b.border-gray-100 > div > div.cursor-pointer > div.relative > div > img[src]")
        for tag in image_tags:
            decode_url = tag["src"]
            img_urls.append(decode_url)
            names.append(tag["alt"])

        for product in zip(names, sites, prices, img_urls):
            item = items.MoaItem()
            item = {
                "name": product[0].strip(),
                "site": product[1].strip(),
                "price": product[2].strip(),
                "imageUrl": product[3].strip(),
            }
            yield item
