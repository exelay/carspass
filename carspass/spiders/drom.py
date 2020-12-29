import yaml
import logging
from datetime import datetime
from dateutil.parser import parse

import scrapy


class DromSpider(scrapy.Spider):
    name = 'drom'
    allowed_domains = ['drom.ru']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36"

    def __init__(self, *args, **kwargs):
        super(DromSpider, self).__init__(*args, **kwargs)
        self.token = getattr(self, "token")

        self.brand = getattr(self, "brand", None)
        self.model = getattr(self, "model", None)

        self.city = getattr(self, "city", 135)
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
                f"https://auto.drom.ru/{self.brand}/{self.model}/used/"
                f"?cid[]={self.city}&minprice={self.price_min}"
                f"&maxprice={self.price_max}"
                f"&minyear={self.year_min}&maxyear={self.year_max}"
                f"&transmission={self.transmission}"
                f"&mv={self.v_min}&xv={self.v_max}&distance={self.radius}"
                f"&w={self.steering_w}&{self.car_body}"
            ).replace('None', '')
        elif self.brand:
            url = (
                f"https://auto.drom.ru/{self.brand}/used/"
                f"?cid[]={self.city}&minprice={self.price_min}"
                f"&maxprice={self.price_max}"
                f"&minyear={self.year_min}&maxyear={self.year_max}"
                f"&transmission={self.transmission}"
                f"&mv={self.v_min}&xv={self.v_max}&distance={self.radius}"
                f"&w={self.steering_w}&{self.car_body}"
            ).replace('None', '')
        else:
            url = (
                f"https://auto.drom.ru/used/"
                f"?cid[]={self.city}&minprice={self.price_min}"
                f"&maxprice={self.price_max}"
                f"&minyear={self.year_min}&maxyear={self.year_max}"
                f"&transmission={self.transmission}"
                f"&mv={self.v_min}&xv={self.v_max}&distance={self.radius}"
                f"&w={self.steering_w}&{self.car_body}&inomarka={self.vendor}"
            ).replace('None', '')

        yield scrapy.Request(url=url, headers={'User-Agent': self.user_agent}, callback=self.parse_item)

    @staticmethod
    def get_id(ad):
        try:
            link = ad.xpath('./@href').get()
            return link.split('/')[-1][:-5]
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            return ad.xpath('.//img/@data-src').get()
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad):
        try:
            with open('conventions.yaml') as f:
                month_nums = yaml.load(f, Loader=yaml.FullLoader)['month_nums']
            date = ad.xpath('.//div[@data-ftid="bull_date"]/text()').get()
            day = date.split()[0]
            try:
                month = date.split()[1]
            except IndexError:
                month = 'empty'
            month_num = month_nums.get(month[:3])
            if not month_num:
                if day.startswith('час'):
                    hours = int(day)
                    unix_time = datetime.timestamp(datetime.today())
                    unix_time -= hours * 3600
                elif day.startswith('мин'):
                    minute = int(day)
                    unix_time = datetime.timestamp(datetime.today())
                    unix_time -= minute * 60
                else:
                    unix_time = datetime.timestamp(datetime.today())
                return datetime.fromtimestamp(unix_time).isoformat()
            return parse(f"{day}.{month_num}").isoformat()
        except Exception as e:
            logging.debug(f'Could not find publish date. Unexpected error: {e}')

    @staticmethod
    def get_title(ad):
        try:
            return ad.xpath('.//span[@data-ftid="bull_title"]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            price = ad.xpath('.//span[@data-ftid="bull_price"]/text()').get().replace(' ', '')
            return int(price)
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            return ad.xpath('.//span[@data-ftid="bull_description-item"][5]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            capacity = ad.xpath('.//span[@data-ftid="bull_description-item"][1]/text()').get().split()[0]
            power = ad.xpath('.//span[@data-ftid="bull_description-item"][1]/text()').get().split()[2].strip('(')
            transmission = ad.xpath('.//span[@data-ftid="bull_description-item"][3]/text()').get()
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad):
        try:
            return ad.xpath('.//span[@data-ftid="bull_location"]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad):
        try:
            return ad.xpath('./@href').get()
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    def parse_item(self, response):
        for ad in response.xpath('//a[@data-ftid="bulls-list_bull"]'):
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
                'actual': True if self.get_title(ad) else False,
                'source': 'drom',
            }

        # next_page = response.xpath('//a[@data-ftid="component_pagination-item-next"]/@href').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, headers={'User-Agent': self.user_agent}, callback=self.parse_item)
