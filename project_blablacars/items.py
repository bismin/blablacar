# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field 
class BlablacarItem(scrapy.Item):
      
      source = scrapy.Field()
      destination=scrapy.Field()
      departure_point=scrapy.Field()
      drop_off_point=scrapy.Field()
      name=scrapy.Field()
      age=scrapy.Field()
      price=scrapy.Field()
      date=scrapy.Field()
      seats_left=scrapy.Field()
      image=scrapy.Field()
      car_owner_rating=scrapy.Field()
      absolute_url=scrapy.Field()
