import logging

import scrapy


class DromSpider(scrapy.Spider):
    name = 'drom'
    allowed_domains = ['drom.ru']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36"

    def __init__(self, *args, **kwargs):
        super(DromSpider, self).__init__(*args, **kwargs)
        self.token = getattr(self, "token")

        self.brand = getattr(self, "brand")
        self.model = getattr(self, "model")

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

    def start_requests(self):
        url = (
            f"https://auto.drom.ru/{self.brand}/{self.model}/used/"
            f"?cid[]={self.city}&minprice={self.price_min}"
            f"&maxprice={self.price_max}"
            f"&minyear={self.year_min}&maxyear={self.year_max}"
            f"&transmission={self.transmission}"
            f"&mv={self.v_min}&xv={self.v_max}&distance={self.radius}"
            f"&w={self.steering_w}&{self.car_body}"
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
    def get_title(ad):
        try:
            return ad.xpath('.//span[@data-ftid="bull_title"]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            return ad.xpath('.//span[@data-ftid="bull_price"]/text()').get()
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
                'publish_date': '',
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

        next_page = response.xpath('//a[@data-ftid="component_pagination-item-next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, headers={'User-Agent': self.user_agent}, callback=self.parse_item)
