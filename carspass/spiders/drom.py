import yaml
import json
import logging
from datetime import datetime
from dateutil.parser import parse

import scrapy


class DromSpider(scrapy.Spider):
    name = 'drom'
    allowed_domains = ['drom.ru']

    def start_requests(self):
        url = 'https://spb.drom.ru/auto/used/all/'
        yield scrapy.Request(url=url, callback=self.parse_item)

    @staticmethod
    def get_id(ad):
        try:
            return ad['bullId']
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            return ad['images'][0]['src']
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad):
        try:
            date = ad['date'].split()

            if len(date) < 3:
                unix_time = datetime.timestamp(datetime.now())

            elif date[1].startswith('мин'):
                minute = int(date[0])
                unix_time = datetime.timestamp(datetime.now())
                unix_time -= minute * 60

            elif date[1].startswith('час'):
                hours = int(date[0])
                unix_time = datetime.timestamp(datetime.now())
                unix_time -= hours * 3600

            else:
                unix_time = datetime.timestamp(datetime.today())
                unix_time -= 24 * 3600

            return datetime.fromtimestamp(unix_time).isoformat()
        except Exception as e:
            logging.debug(f'Could not find publish date. Unexpected error: {e}')

    @staticmethod
    def get_title(ad):
        try:
            return ad['title']
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            return ad['price']
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            return ad['description']['mileage']
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            capacity = ad['description']['volume'] / 1000
            power = ad['description']['power']
            transmission = ad['description']['transmission']
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad):
        try:
            return ad['location']
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad):
        try:
            return ad['url']
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    @staticmethod
    def get_actual(ad):
        try:
            return not ad['sold']
        except Exception as e:
            logging.debug(f"Failed to get actual. {e}")

    def parse_item(self, response):
        site_data = response.xpath('//script[@data-drom-module="bulls-list"]/@data-drom-module-data').get()
        ads = json.loads(site_data)['bullList']['bullsData'][0]['bulls']
        for ad in ads:
            yield {
                'id': self.get_id(ad),
                'img_link': self.get_img_link(ad),
                'publish_date': self.get_publish_date(ad),
                'title': self.get_title(ad),
                'price': self.get_price(ad),
                'mileage': self.get_mileage(ad),
                'tech_info': self.get_tech_info(ad),
                'location': self.get_location(ad),
                'metro': '',
                'link': self.get_link(ad),
                'actual': self.get_actual(ad),
                'source': self.name,
                'scraped_at': datetime.now().isoformat(),
            }
