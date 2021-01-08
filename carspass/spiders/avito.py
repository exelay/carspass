import json
import logging
from datetime import datetime
from requests import PreparedRequest

import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    url = str()
    page_number = 1
    proxy_url = "https://app.scrapingbee.com/api/v1/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scraping_time = datetime.today().date().isoformat()

    def start_requests(self):
        req = PreparedRequest()

        self.url = 'https://www.avito.ru/sankt-peterburg/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=1&s=104'
        proxy_params = {
            "api_key": "EHW1NW8Y19PCOMPHBDARWQ2A1BOS6GIDEP9ZBWAWUXX6BUE0PIIL94PUW813WY6LISV941770L7R2U4B",
            "url": self.url,
            "render_js": "false",
        }
        req.prepare_url(self.proxy_url, proxy_params)
        url = req.url

        yield scrapy.Request(url=url, callback=self.parse_item)

    @staticmethod
    def get_id(ad):
        try:
            return ad.get('id')
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            return ad['gallery']['imageLargeVipUrl']
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_title(ad):
        try:
            return ad['title']
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            return ad['priceDetailed']['value']
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            payload = ad['iva']['AutoParamsStep'][0]['payload']['text']
            return payload.split(',')[0][:-2].replace(' ', '')
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            payload = ad['iva']['AutoParamsStep'][0]['payload']['text']
            tech_info = payload.split(',')[1].split()
            capacity = tech_info[0]
            transmission = tech_info[1]
            power = f"{tech_info[2].strip('(')} {tech_info[3].strip(')')}"
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad):
        try:
            return ad['location']['name']
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad):
        try:
            return f"https://www.avito.ru/{ad['urlPath']}"
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    def parse_item(self, response):
        p_loader = json.loads(response.xpath('//div[@class="js-initial"]/@data-state').get())
        ads = [item for item in p_loader['catalog']['items'] if item['type'] == 'item']
        for ad in ads:
            yield {
                'id': self.get_id(ad),
                'img_link': self.get_img_link(ad),
                'publish_date': None,
                'title': self.get_title(ad),
                'price': self.get_price(ad),
                'mileage': self.get_mileage(ad),
                'tech_info': self.get_tech_info(ad),
                'location': self.get_location(ad),
                'metro': None,
                'link': self.get_link(ad),
                'actual': True,
                'source': 'avito',
            }
        req = PreparedRequest()
        self.page_number += 1
        req.prepare_url(self.url, {'p': self.page_number})
        next_page = req.url
        proxy_params = {
            "api_key": "EHW1NW8Y19PCOMPHBDARWQ2A1BOS6GIDEP9ZBWAWUXX6BUE0PIIL94PUW813WY6LISV941770L7R2U4B",
            "url": next_page,
            "render_js": "false",
        }
        req.prepare_url(self.proxy_url, proxy_params)
        url = req.url
        if self.page_number <= 50:
            yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True)
