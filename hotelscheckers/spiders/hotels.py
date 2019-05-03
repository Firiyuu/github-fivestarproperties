# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
import pymongo
from scrapy.conf import settings


class HotelsSpider(scrapy.Spider):
    name = 'hotels'
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
        self.driver.get(response.url)
        urls_ = [] # List of urls
        urls_from_db = self.db[settings['MONGODB_COLLECTION']].distinct('_url') 
        urls_ = urls_from_db
        max_retries = 10 # Max retries in repetition
        while True:
            image_containers = self.driver.find_elements_by_xpath("//div[@class='panel-image listing-img']/a[@class='media-photo media-cover']")
            for ic in image_containers:
                print("Containers number: " + str(len(image_containers)))
                try:
                    print(str(urls_))


                    
                    ic.click()
                    url = self.driver.current_url
                    time.sleep(5)

                    if url not in urls_: #If url is already in list, do not append.
                       urls_.append(url)
                       try:
                          status = self.db[settings['MONGODB_COLLECTION']].insert({'_url': str(url)})
                          print(str(status))
                       except Exception as e:
                       	  print("Database Error: " + str(e))

                    self.driver.back()
                    time.sleep(5)

                    continue
                    

                    
                except:
                    break
                self.driver.close()
