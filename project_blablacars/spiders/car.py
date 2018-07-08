# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scrapy import Request
from scrapy.linkextractors import LinkExtractor


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['blablacar.in']
    start_urls = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi&fcc=IN&tn=chandigarh&tcc=IN&sort=trip_date&order=asc&limit=10&page=1']

    def parse(self, response):
	jobs = response.xpath('//article[@class="row"]')
	for job in jobs:
		source=job.xpath('div[@class="description span5"]/h3[@class="fromto"]/span[@class="from trip-roads-stop"]/text()').extract_first()
		destination=job.xpath('div[@class="description span5"]/h3[@class="fromto"]/span[@class="trip-roads-stop"]/text()').extract_first()
		departure_point=job.xpath('div[@class="description span5"]/dl[@class="geo-from"]/dd[@class="js-tip-custom"]/text()').extract_first()
		drop_off_point=job.xpath('div[@class="description span5"]/dl[@class="geo-to"]/dd[@class="js-tip-custom"]/text()').extract_first()
		
		departure_date=dateparser.parse(job.xpath('div[@class="description span5"]/h3[@class="time u-darkGray"]/text()').extract_first())
    		name=job.xpath('div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/h2[@class="ProfileCard-info ProfileCard-info--name u-truncate"]/text()').extract_first()
		age=job.xpath('div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/div[@class="ProfileCard-info"]/text()').re("([\d]+)")
		price=job.xpath('div[@class="offer span2 u-alignRight"]/div[@class="price price-black"]/strong/span[@class=""]/text()').re("([\d]+)")

		
		seats_left=job.xpath('div[@class="offer span2 u-alignRight"]/div[@class="availability"]/strong/text()').re("([\d]+)")
		image=job.xpath('div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-picture"]/div[@class="PhotoWrapper PhotoWrapper--medium"]/img/@src').extract_first()

		yield{'image':image,'seats_left':seats_left,'price':price,'age':age,'name':name,'source':source,'destination':destination,'departure_point':departure_point,'drop_off_point':drop_off_point,'departure_date':departure_date}


	relative_next_url = response.xpath('//ul/li[@class="next"]/a/@href').extract_first()
	absolute_next_url = response.urljoin(relative_next_url)
 	yield Request(absolute_next_url, callback=self.parse)
