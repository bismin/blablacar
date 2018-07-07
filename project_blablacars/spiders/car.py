# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scrapy import Request


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['blablacar.in']
    start_urls = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi&fcc=IN&tn=chandigarh&tcc=IN&sort=trip_date&order=asc&limit=10&page=1']

    def parse(self, response):
	jobs = response.xpath('//div[@class="description span5"]')
	for job in jobs:
		source=job.xpath('h3[@class="fromto"]/span[@class="from trip-roads-stop"]/text()').extract_first()
		destination=job.xpath('h3[@class="fromto"]/span[@class="trip-roads-stop"]/text()').extract_first()
		departure_point=job.xpath('dl[@class="geo-from"]/dd[@class="js-tip-custom"]/text()').extract_first()
		drop_off_point=job.xpath('dl[@class="geo-to"]/dd[@class="js-tip-custom"]/text()').extract_first()
		
		departure_date=dateparser.parse(job.xpath('h3[@class="time u-darkGray"]/text()').extract_first())
	
		yield{'source':source,'destination':destination,'departure_point':departure_point,'drop_off_point':drop_off_point,'departure_date':departure_date}
