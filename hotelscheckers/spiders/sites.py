# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
import pymongo
from scrapy.conf import settings
from hotelscheckers.items import HotelscheckersItem
import re

class HotelsSpider(scrapy.Spider):
    name = 'sites'
    allowed_domains = ['fivestargulfrentals.com']
    start_urls = ['https://www.fivestargulfrentals.com/search-results/']

    # Add a maxdepth attribute
    maxdepth = 10

    def __init__(self):
        """
        This website elements returns in {} which probably are added by some framework in JavaScript. Scrapy can't run JavaScript. 
        It is needed use Selenium to control web browser which can load page, run javascript and gives HTML with all elements.
        """
        self.driver = webdriver.Firefox(executable_path="D:/May/scrapy/geckodriver.exe") #CONFIGURE PATH TO DRIVER

        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

        # if database:
        #     settings['MONGODB_DB'] = database
        self.db = connection[settings['MONGODB_DB']]

    def parse(self, response):
        #This website needs to be navigated in order to get the urls because of JS. So we need to get inside each image container get the url
        #and go back to the search results
        item = HotelscheckersItem()

        urls_ = [] # List of urls
        urls_from_db = self.db[settings['MONGODB_COLLECTION']].distinct('_url') 
        urls_ = urls_from_db
        max_retries = 10 # Max retries in repetition

        for link in urls_:
            request = scrapy.Request(link, callback=self._parse_url_content)
            request.meta['item'] = item 
            yield request

    def _parse_url_content(self, response):
        name_selector = response.xpath("//div[@class='property_description']/h3")
        name_text = name_selector.xpath("text()").extract_first()

        description_text = response.xpath("//div[@class='property_description']/text()").extract()

        

        sleep_bathroom_bedroom = response.xpath("//div[@class='unit-name-header-wrap']/div/h2/text()").extract_first()
        sleep_bathroom_bedroom = str(sleep_bathroom_bedroom)
        sleep_bathroom_bedroom = re.findall(r'\d+(?:\.\d+)?', sleep_bathroom_bedroom)
        


        item = response.meta['item']
        item['url'] = response.url
        item['name'] = name_text
        item['description'] = description_text
        item['bedrooms'] = sleep_bathroom_bedroom[0]
        item['bathrooms'] = sleep_bathroom_bedroom[1]
        item['sleeps'] = sleep_bathroom_bedroom[2]

        #THE LOCATION TAB NEEDS TO BE CLICKED SO WE USE SELENIUM
        self.driver.get(response.url)
        self.driver.find_element_by_xpath("//ul[@class='nav nav-pills nav-justified nav-tabs nav-tabsCarusel']/li[4]/a[1]").click()
        location = self.driver.find_element_by_xpath("//div[@id='location-title']/div[@class='row' and 1]/div[1]/div[@id='property-location' and 1]/iframe[1]")
        location = str(location.get_attribute("src"))
        item['location'] = location.split("=")[2]
        time.sleep(5)

        #WE GET THE URL IN ORDER TO GET IMAGES
       


        relative_img_urls = response.css("img::attr(src)").extract() 
        item["image_urls"] = self.url_join(relative_img_urls, response) 


        try:
            self.db[settings['MONGODB_COLLECTION_TARGET']].insert(item)
        except Exception as e:
            print(str(e))

        yield item

    def url_join(self, urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))

        return joined_urls