import json
import logging

import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36"

    def __init__(self, *args, **kwargs):
        super(AvitoSpider, self).__init__(*args, **kwargs)
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

    def start_requests(self):
        if self.brand and self.model:
            url = (
                f"https://www.avito.ru/"
                f"{self.city}/avtomobili/s_probegom/"
                f"{self.brand}/{self.model}"
                f"?pmax={self.price_max}&pmin={self.price_min}"
                f"&radius={self.radius}"
            ).replace('None', '')
        elif self.brand:
            url = (
                f"https://www.avito.ru/"
                f"{self.city}/avtomobili/s_probegom/"
                f"{self.brand}"
                f"?pmax={self.price_max}&pmin={self.price_min}"
                f"&radius={self.radius}"
            ).replace('None', '')
        else:
            url = (
                f"https://www.avito.ru/"
                f"{self.city}/avtomobili/s_probegom/"
                f"?pmax={self.price_max}&pmin={self.price_min}"
                f"&radius={self.radius}"
            ).replace('None', '')

        yield scrapy.Request(url=url, headers={'User-Agent': self.user_agent}, callback=self.parse_item)

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
