from typing import Iterable
import scrapy
from amazon.items import AmazonScraperItem
from urllib.parse import urlencode
import time 
import os
# from dotenv import load_dotenv

# load_dotenv()
# create a new apikey from scrapy
API_KEY = 'd51f6df1-f9d0-4c23-a6c0-b7215457f25f'
def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    # allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in"]

    def start_requests(self):
        keyword = ['1968123031']
        n_pages = 2

        for word in keyword:
            for page in range(1, n_pages + 1):  # Proper pagination
                url = f'https://www.amazon.in/gp/bestsellers/apparel/{word}/ref=zg_bs_pg_{page}_apparel'
                yield scrapy.Request(get_scrapeops_url(url), callback=self.parse)
                time.sleep(2)  # Add a delay to handle rate limiting


    def parse(self, response):
        
        products = list(set(response.css('a.a-link-normal ::attr(href)').getall()))  
        
        for prt in products:
            if prt:  # Ensure the product link is not empty
                prt_url = "https://www.amazon.in" + prt
                yield response.follow(get_scrapeops_url(prt_url), callback=self.parse_prt)

    def parse_prt(self, response):
        object = AmazonScraperItem()
        # table = response.css('table.a-normal.a-spacing-micro tr')
        object['name'] = response.css('span#productTitle ::text').get(default='No Name Available').strip()
        object['price'] = response.css('span.a-price-whole ::text').get(default='No Price Available').strip()
        # object['brand'] = table[0].css('td.a-span9 span ::text').get()
        # object['memory'] = table[1].css('td.a-span9 span ::text').get()
        # object['h_interface'] = table[2].css('td.a-span9 span ::text').get()
        # object['special_features'] = table[3].css('td.a-span9 span ::text').get()
        # object['speed'] = table[4].css('td.a-span9 span ::text').get()
        product_details = {}
        details = response.css('div.a-fixed-left-grid.product-facts-detail')
        for detail in details:
            key = detail.css('div.a-col-left span span ::text').get(default='').strip()
            value = detail.css('div.a-col-right span span ::text').get(default='').strip()
            if key and value:
                product_details[key] = value

        object['product_details'] = product_details
        yield object

        