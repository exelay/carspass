import re
from urllib.parse import unquote

import pytz
import json
import logging
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YoulaSpider(CrawlSpider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36"

    def start_requests(self):  # TODO add spider arguments and make a request with them
        yield scrapy.Request(url='https://auto.youla.ru/rossiya/cars/used/audi/100/',
                             headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@data-target-id="button-link-serp-paginator"][last()]'),
             callback='parse_item', follow=True),
    )

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
