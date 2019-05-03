# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelscheckersItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    sleeps = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    _id = scrapy.Field()
    pass
