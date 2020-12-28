import re
import pytz
import json
import logging

from datetime import datetime
from urllib.parse import unquote

import scrapy


class YoulaSpider(scrapy.Spider):
    name = 'amru'
    allowed_domains = ['youla.ru']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36"

    def __init__(self, *args, **kwargs):
        super(YoulaSpider, self).__init__(*args, **kwargs)
        self.token = getattr(self, "token")

        self.brand = getattr(self, "brand", None)
        self.model = getattr(self, "model", None)

        self.city = getattr(self, "city", "sankt-peterburg")
        self.price_min = getattr(self, "price_min", None)
        self.price_max = getattr(self, "price_max", None)
        self.year_min = getattr(self, "year_min", None)
        self.year_max = getattr(self, "year_max", None)
        self.transmission = getattr(self, "transmission", None)
        self.v_min = getattr(self, "v_min", None)
        self.v_max = getattr(self, "v_max", None)
        self.radius = getattr(self, "radius", None)
        self.steering_w = getattr(self, "steering_w", None)
        self.car_body = getattr(self, "car_body", None)
        self.vendor = getattr(self, "vendor", None)
        self.latest_ads = getattr(self, "latest_ads", None)

    def start_requests(self):
        if self.brand and self.model:
            url = (
                f"https://am.ru/{self.city}/cars/used/{self.brand}/{self.model}/"
                f"?priceMin={self.price_min}&priceMax={self.price_max}"
                f"&yearMin={self.year_min}&yearMax={self.year_max}"
                f"&gearTypes%5B0%5D={self.transmission}"
                f"&engineVolumeMin={self.v_min}&engineVolumeMax={self.v_max}"
                f"&wheelTypes%5B0%5D={self.steering_w}&bodyTypes%5B0%5D={self.car_body}"
            ).replace('None', '')
        elif self.brand:
            url = (
                f"https://am.ru/{self.city}/cars/used/{self.brand}/"
                f"?priceMin={self.price_min}&priceMax={self.price_max}"
                f"&yearMin={self.year_min}&yearMax={self.year_max}"
                f"&gearTypes%5B0%5D={self.transmission}"
                f"&engineVolumeMin={self.v_min}&engineVolumeMax={self.v_max}"
                f"&wheelTypes%5B0%5D={self.steering_w}&bodyTypes%5B0%5D={self.car_body}"
            ).replace('None', '')
        else:
            url = (
                f"https://am.ru/{self.city}/cars/used/"
                f"?priceMin={self.price_min}&priceMax={self.price_max}"
                f"&yearMin={self.year_min}&yearMax={self.year_max}"
                f"&gearTypes%5B0%5D={self.transmission}&brandOrigin={self.vendor}"
                f"&engineVolumeMin={self.v_min}&engineVolumeMax={self.v_max}"
                f"&wheelTypes%5B0%5D={self.steering_w}&bodyTypes%5B0%5D={self.car_body}"
            ).replace('None', '')

        yield scrapy.Request(url=url, headers={'User-Agent': self.user_agent}, callback=self.parse_item)

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
            tz_moscow = pytz.timezone('Europe/Moscow')
            unix_time = int(ad[1][11][2:]) // 1000
            return datetime.fromtimestamp(unix_time, tz=tz_moscow).isoformat()
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
                'publish_date': '',
                'title': self.get_title(ad),
                'price': self.get_price(ad),
                'mileage': self.get_mileage(ad),
                'tech_info': self.get_tech_info(ad),
                'location': self.get_location(ad),
                'metro': '',
                'link': self.get_link(ad),
                'actual': True,
                'source': 'youla',
            }

        next_page = response.xpath('//a[.//span[contains(text(), "Вперед")]]/@href').get()
        if next_page:
            absolute_url = f'https://auto.youla.ru{next_page}'
            yield scrapy.Request(url=absolute_url, headers={'User-Agent': self.user_agent},
                                 callback=self.parse_item)
