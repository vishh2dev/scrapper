# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field() 
    # brand = scrapy.Field()
    # memory = scrapy.Field()
    # h_interface = scrapy.Field()
    # special_features = scrapy.Field()
    # speed = scrapy.Field()
    product_details = scrapy.Field()