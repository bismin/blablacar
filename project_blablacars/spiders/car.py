# -*- coding: utf-8 -*-
import scrapy


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi']
    start_urls = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi&fcc=IN&tn=chandigarh&tcc=IN&sort=trip_date&order=asc&limit=10&page=1']

    def parse(self, response):
	jobs = response.xpath('//div[@class="description span5"]')
	for job in jobs:
		source=job.xpath('h3[@class="fromto"]/span[@class="from trip-roads-stop"]/text()').extract_first()
		destination=job.xpath('h3[@class="fromto"]/span[@class="trip-roads-stop"]/text()').extract_first()
		yield{'source':source,'destination':destination}
