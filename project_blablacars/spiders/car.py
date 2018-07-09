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
		car_owner_name=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/h2[@class="ProfileCard-info ProfileCard-info--name u-truncate"]/text()').extract_first()
		car_owner_age=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-infosBlock"]/div[@class="ProfileCard-info"]/text()').re("([\d]+)")

		price=job.xpath('a/article[@class="row"]/div[@class="offer span2 u-alignRight"]/div[@class="price price-black"]/strong/span[@class=""]/text()').re("([\d]+)")

		date=job.xpath('a/article[@class="row"]/div[@class="description span5"]/h3[@class="time u-darkGray"]/text()').extract_first()	
		departure_date=dateparser.parse(date)
		seats_left=job.xpath('a/article[@class="row"]/div[@class="offer span2 u-alignRight"]/div[@class="availability"]/strong/text()').re("([\d]+)")
		car_owner_image=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-head"]/div[@class="ProfileCard-picture"]/div[@class="PhotoWrapper PhotoWrapper--medium"]/img/@src').extract_first()
		car_owner_rating=job.xpath('a/article[@class="row"]/div[@class="ProfileCard ProfileCard--condensed span2"]/div[@class="ProfileCard-row"]/p[@class="ratings-container"]/span[@class="u-textBold u-darkGray"]/text()').extract_first()
		relative_url = job.xpath('a/@href').extract_first()
 		absolute_url = response.urljoin(relative_url)




		item=BlablacarItem()
		item['source']=source
		item['destination']=destination
		item['departure_point']=departure_point
		item['drop_off_point']=drop_off_point
		item['car_owner_name']=car_owner_name
		item['car_owner_age']=car_owner_age
		item['price']=price
		item['departure_date']=departure_date
		item['seats_left']=seats_left
		item['car_owner_image']=car_owner_image 
		item['car_owner_rating']=car_owner_rating
		
		
		absolute_url = response.urljoin(relative_url)
		r=scrapy.Request(absolute_url, callback=self.parse_page)
		r.meta['item']=item
		yield r
	relative_next_url = response.xpath('//ul/li[@class="next"]/a/@href').extract_first()
	absolute_next_url = response.urljoin(relative_next_url)
 	yield Request(absolute_next_url, callback=self.parse)


    def parse_page(self, response):
	item=response.meta['item']
    	options = response.xpath('//div[@class="RideDetails-infoValue"]/span/span[@class="u-alignMiddle"]/text()').extract()
	car_model =response.xpath('//div[@class="Block Profile"]/div[@class="Block-section"]/div[@class="Profile-car u-table"]/p[@class="Profile-carDetails u-cell"]/text()').extract_first()
	car_color =response.xpath('//div[@class="Block Profile"]/div[@class="Block-section"]/div[@class="Profile-car u-table"]/p[@class="Profile-carDetails u-cell"]/text()[last()]').extract()
	item['options']=options
	item['car_model']=car_model
	item['car_color']=car_color

	yield item
