import json
import yaml
import logging
from datetime import datetime

import scrapy


class DromSpider(scrapy.Spider):
    name = 'drom'
    allowed_domains = ['drom.ru']
    scraped_time = datetime.now().isoformat(timespec='seconds')

    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        with open(f'dictionaries/map.{self.name}.json', 'r', encoding='utf-8') as file:
            self.dictionary = json.load(file)
        with open(f'conventions/{self.name}.yaml') as f:
            self.conventions = yaml.load(f, Loader=yaml.FullLoader)
        self.city = self.conventions['city'][city]

    def start_requests(self):
        url = f'https://{self.city}.drom.ru/auto/used/all?distance=200'
        yield scrapy.Request(url=url, callback=self.parse_item, meta={'dont_proxy': True})

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

            return datetime.fromtimestamp(unix_time).isoformat(timespec='seconds')
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
    def get_brand(ad) -> str:
        try:
            brand = ad['url'].split('/')[3]
            return brand
        except Exception as e:
            logging.debug(f"Failed to get brand. {e}")

    @staticmethod
    def get_model(ad) -> str:
        try:
            brand = ad['url'].split('/')[3]
            model = ad['url'].split('/')[4]
            return model
        except Exception as e:
            logging.debug(f"Failed to get model. {e}")

    def get_vendor(self, ad) -> str:
        brand = self.get_brand(ad)
        with open("conventions/vendors.json", "r") as file:
            vendors = json.loads(file.read())
        if brand in vendors['domestic']:
            return 'domestic'
        else:
            return 'foreign'

    @staticmethod
    def get_year(ad):
        try:
            title = ad['title'].lower().split(',')
            return int(title[-1])
        except Exception as e:
            logging.debug(f"Failed to get year. {e}")

    @staticmethod
    def get_transmission(ad):
        try:
            transmission = ad['description']['transmission']
            with open('conventions/drom.yaml') as f:
                transmissions = yaml.load(f, Loader=yaml.FullLoader)['transmission']
            return transmissions[transmission]
        except Exception as e:
            logging.debug(f"Failed to get transmission. {e}")

    def get_frame_type(self, ad):
        try:
            frame_type = ad['frameType']
            return self.conventions['frame_type'][frame_type]
        except Exception as e:
            logging.debug(f"Failed to get frame type. {e}")

    @staticmethod
    def get_power(ad):
        try:
            return ad['description']['power']
        except Exception as e:
            logging.debug(f"Failed to get power. {e}")

    @staticmethod
    def get_volume(ad):
        try:
            return ad['description']['volume'] / 1000
        except Exception as e:
            logging.debug(f"Failed to get volume. {e}")

    @staticmethod
    def get_actual(ad):
        try:
            return not ad['sold']
        except Exception as e:
            logging.debug(f"Failed to get actual. {e}")

    @staticmethod
    def is_pined(ad):
        if ad.get('promotionStatus'):
            return True
        else:
            return False

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
                'brand': self.get_brand(ad),
                'model': self.get_model(ad),
                'vendor': self.get_vendor(ad),
                'year': self.get_year(ad),
                'transmission': self.get_transmission(ad),
                'frame_type': self.get_frame_type(ad),
                'power': self.get_power(ad),
                'volume': self.get_volume(ad),
                'metro': None,
                'link': self.get_link(ad),
                'actual': self.get_actual(ad),
                'source': self.name,
                'pined': self.is_pined(ad),
                'scraped_at': self.scraped_time,
                'source_brand': self.get_brand(ad),
                'source_model': self.get_model(ad),
            }
