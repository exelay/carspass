import re
import json
import logging

from datetime import datetime
from urllib.parse import unquote

import scrapy


class YoulaSpider(scrapy.Spider):
    name = 'amru'
    allowed_domains = ['youla.ru', 'am.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scraping_time = datetime.today().date().isoformat()

    def start_requests(self):
        url = 'https://auto.youla.ru/rossiya/cars/used/?publication=1'
        yield scrapy.Request(url=url, callback=self.parse_item)

    @staticmethod
    def get_id(ad):
        try:
            return ad[1][81]
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            return ad[1][5][1][0][1][3]
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad):
        try:
            unix_time = int(ad[1][11][2:]) // 1000
            return datetime.fromtimestamp(unix_time).isoformat()
        except Exception as e:
            logging.debug(f"Failed to get publish date. {e}")

    @staticmethod
    def get_title(ad):
        try:
            return ad[1][27]
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            return ad[1][33][1][5]
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            return ad[1][47][1][0][1][5]
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            capacity = ad[1][55]
            transmission = ad[1][47][1][5][1][3]
            raw_power = ad[1][47][1][2][1][3]
            power = re.match(r"[+-]?([0-9]*[.])?[0-9]+", raw_power).group()
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad):
        try:
            return ad[1][39]
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad):
        try:
            return ad[1][79]
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    def parse_item(self, response):
        site_data = unquote(
            re.findall(r"window\.transitState = decodeURIComponent\(\"([\s\S]+?)\"\);</script>", response.text)[0]
        )
        ads = json.loads(site_data)[1][31][1]
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
                'actual': True,
                'source': 'amru',
            }

        next_page = response.xpath('//a[.//span[contains(text(), "Вперед")]]/@href').get()
        if next_page:
            absolute_url = f'https://auto.youla.ru{next_page}'
            yield scrapy.Request(url=absolute_url, callback=self.parse_item)
