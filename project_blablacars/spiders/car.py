# -*- coding: utf-8 -*-
import scrapy
from ..items import BlablacarItem
import dateparser
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['blablacar.in']
    start_urls = ['https://www.blablacar.in/ride-sharing/new-delhi/chandigarh/#?fn=new+delhi&fcc=IN&tn=chandigarh&tcc=IN&sort=trip_date&order=asc&limit=10&page=1']

    def parse(self, response):
	jobs = response.xpath('//li[@class="trip relative"]')
	for job in jobs:
		source=job.xpath('a/article[@class="row"]/div[@class="description span5"]/h3[@class="fromto"]/span[@class="from trip-roads-stop"]/text()').extract_first()
		destination=job.xpath('a/article[@class="row"]/div[@class="description span5"]/h3[@class="fromto"]/span[@class="trip-roads-stop"]/text()').extract_first()
		departure_point=job.xpath('a/article[@class="row"]/div[@class="description span5"]/dl[@class="geo-from"]/dd[@class="js-tip-custom"]/text()').extract_first()
		drop_off_point=job.xpath('a/article[@class="row"]/div[@class="description span5"]/dl[@class="geo-to"]/dd[@class="js-tip-custom"]/text()').extract_first()
		name=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/h2[@class="ProfileCard-info ProfileCard-info--name u-truncate"]/text()').extract_first()
		age=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/div[@class="ProfileCard-info"]/text()').re("([\d]+)")

		price=job.xpath('a/article[@class="row"]/div[@class="offer span2 u-alignRight"]/div[@class="price price-black"]/strong/span[@class=""]/text()').re("([\d]+)")

		date=job.xpath('a/article[@class="row"]/div[@class="description span5"]/h3[@class="time u-darkGray"]/text()').extract_first()	
		date=dateparser.parse(date)
		seats_left=job.xpath('a/article[@class="row"]/div[@class="offer span2 u-alignRight"]/div[@class="availability"]/strong/text()').re("([\d]+)")
		image=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-picture"]/div[@class="PhotoWrapper PhotoWrapper--medium"]/img/@src').extract_first()
		car_owner_rating=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-row"]/p[@class="ratings-container"]/span[@class="u-textBold u-darkGray"]/text()').extract_first()
		relative_url = job.xpath('a/@href').extract_first()
 		absolute_url = response.urljoin(relative_url)




		item=BlablacarItem()
		item['source']=source
		item['destination']=destination
		item['departure_point']=departure_point
		item['drop_off_point']=drop_off_point
		item['name']=name
		item['age']=age
		item['price']=price
		item['date']=date
		item['seats_left']=seats_left
		item['image']=image
		item['car_owner_rating']=car_owner_rating
		item['absolute_url']=absolute_url
		
		
		absolute_url = response.urljoin(relative_url)
		r=scrapy.Request(absolute_url, callback=self.parse_page)
		r.meta['item']=item
		yield r

    def parse_page(self, response):
	item=response.meta['item']
    	options = response.xpath('//div[@class="RideDetails-infoValue"]/span/span[@class="u-alignMiddle"]/text()').extract()
	item['options']=options
	yield item
