# -*- coding: utf-8 -*-
import scrapy


class WebCrawlerSpider(scrapy.Spider):
    name = "web_crawler"
    allowed_domains = ["http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx"]
    start_urls = ['http://http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx/']

    def parse(self, response):
        pass
