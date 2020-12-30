import logging
from requests import PreparedRequest

import scrapy


class AutoSpider(scrapy.Spider):
    name = 'autoru'
    allowed_domains = ['auto.ru']

    def __init__(self, *args, **kwargs):
        super(AutoSpider, self).__init__(*args, **kwargs)
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
        req = PreparedRequest()
        params = {
            'pmin': self.price_min,
            'pmax': self.price_max,
            'radius': self.radius,
        }
        if self.brand and self.model:
            abs_url = f"https://auto.ru/{self.city}/cars/{self.brand}/{self.model}/used/"
        elif self.brand:
            abs_url = f"https://auto.ru/{self.city}/cars/{self.brand}/used/"
        elif self.vendor:
            abs_url = f"https://auto.ru/{self.city}/cars/{self.vendor}/used/"
        else:
            abs_url = f"https://auto.ru/{self.city}/cars/used/"
        req.prepare_url(abs_url, params)
        url = req.url

        yield scrapy.Request(url=url, callback=self.parse_item)

    @staticmethod
    def get_id(ad):
        try:
            link = ad.xpath('.//meta[@itemprop="url"]/@content').get()
            return link.split('/')[-2].split('-')[0]
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            return ad.xpath('.//meta[@itemprop="image"]/@content').get()
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_title(ad):
        try:
            return ad.xpath('.//meta[@itemprop="name"]/@content').get()
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            return ad.xpath('.//meta[@itemprop="price"]/@content').get()
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            mileage = ad.xpath('.//div[@class="ListingItem-module__kmAge"]/text()').get().\
                encode('ascii', errors='ignore')
            return mileage.decode('utf-8')
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            capacity = ad.xpath('.//meta[@itemprop="engineDisplacement"]/@content').get().split()[0]
            power = ad.xpath('.//meta[@itemprop="enginePower"]/@content').get().split()[0]
            transmission = ad.xpath('.//meta[@itemprop="vehicleTransmission"]/@content').get()
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad):
        try:
            return ad.xpath('.//span[contains(@class, "MetroListPlace__regionName")]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad):
        try:
            return ad.xpath('.//meta[@itemprop="url"]/@content').get()
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    def parse_item(self, response):
        for ad in response.xpath('//div[contains(@class, "ListingItem-module__container")]'):
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
                'actual': True if self.get_price(ad) else False,
                'source': 'auto',
            }

        next_page = response.xpath('//a[contains(@class, "ListingPagination-module__next")]/@href').get()
        page_number = int(next_page.split('/')[-1][-1])
        if next_page and page_number <= 5:
            yield scrapy.Request(url=next_page, callback=self.parse_item)
