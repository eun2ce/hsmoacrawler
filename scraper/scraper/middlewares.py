import time
from logging import getLogger

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumMiddleware(object):
    def __init__(self):
        self.logger = getLogger(__name__)
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("Content-Type=application/json; charset=utf-8")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()

        self.wait = 5

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        self.logger.debug("SeleniumMiddleware is starting")

        try:
            self.driver.get(request.url)
            time.sleep(self.wait)

            return HtmlResponse(url=self.driver.current_url, status=200, body=self.driver.page_source.replace("\\", ""),
                                request=request,
                                encoding="utf-8")
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)