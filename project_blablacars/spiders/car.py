# -*- coding: utf-8 -*-
import scrapy


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi']
    start_urls = ['http://https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi/']

    def parse(self, response):
        pass
