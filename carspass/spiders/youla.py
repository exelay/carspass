import re
import json
import logging

from datetime import datetime
from urllib.parse import unquote

import scrapy
import yaml
from transliterate import translit


class YoulaSpider(scrapy.Spider):
    name = 'amru'
    allowed_domains = ['youla.ru', 'am.ru']
    scraped_time = datetime.now().isoformat(timespec='seconds')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(f'dictionaries/map.{self.name}.json', 'r', encoding='utf-8') as file:
            self.dictionary = json.load(file)

    def start_requests(self) -> scrapy.Request:
        url = 'https://auto.youla.ru/sankt-peterburg/cars/used/?searchOrder=104&publication=1'
        yield scrapy.Request(url=url, callback=self.parse_item, meta={'dont_proxy': True})

    @staticmethod
    def get_id(ad) -> str:
        try:
            return ad['id']
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad) -> str:
        try:
            return ad['photos'][1][1][1][3]
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad) -> str:
        try:
            unix_time = int(ad["actualizationDate"][2:]) // 1000
            return datetime.fromtimestamp(unix_time).isoformat(timespec='seconds')
        except Exception as e:
            logging.debug(f"Failed to get publish date. {e}")

    @staticmethod
    def get_title(ad) -> str:
        try:
            return ad["fullTitle"]
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad) -> int:
        try:
            return ad["prices"][1][5]
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad) -> int:
        try:
            mileage = ad['info'][1][0][1][5][:-2].replace(' ', '')
            return int(mileage)
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad) -> str:
        try:
            capacity = ad['engineVol']
            transmission = ad['info'][1][5][1][3]
            power = ad['info'][1][2][1][3][:-5]
            return f"{capacity} / {transmission} / {power}"
        except Exception as e:
            logging.debug(f"Failed to get technical information. {e}")

    @staticmethod
    def get_location(ad) -> str:
        try:
            return ad['city']
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad) -> str:
        try:
            return ad['link']
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    @staticmethod
    def get_brand(ad) -> str:
        try:
            brand = translit(ad['brandAlias'], 'ru', reversed=True)
            return brand
        except Exception as e:
            logging.debug(f"Failed to get brand. {e}")

    @staticmethod
    def get_model(ad) -> str:
        try:
            brand = translit(ad['brandAlias'], 'ru', reversed=True)
            model = translit(ad['modelAlias'], 'ru', reversed=True)
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
    def get_year(ad) -> int:
        try:
            return int(ad['year'])
        except Exception as e:
            logging.debug(f"Failed to get year. {e}")

    def get_transmission(self, ad) -> str:
        try:
            transmission = ad['info'][1][5][1][3]
            with open(f'conventions/{self.name}.yaml') as f:
                transmissions = yaml.load(f, Loader=yaml.FullLoader)['transmission']
            return transmissions[transmission]
        except Exception as e:
            logging.debug(f"Failed to get transmission. {e}")

    def get_frame_type(self, ad) -> str:
        try:
            frame_type = int(ad["searchQuery"][1][1])
            with open(f'conventions/{self.name}.yaml') as f:
                frame_types = yaml.load(f, Loader=yaml.FullLoader)['frame_type']
            return frame_types[frame_type]
        except Exception as e:
            logging.debug(f"Failed to get frame type. {e}")

    @staticmethod
    def get_power(ad) -> int:
        try:
            power = ad['info'][1][2][1][3][:-5]
            return int(power)
        except Exception as e:
            logging.debug(f"Failed to get power. {e}")

    @staticmethod
    def get_volume(ad) -> float:
        try:
            return float(ad['engineVol'])
        except Exception as e:
            logging.debug(f"Failed to get volume. {e}")

    def parse_item(self, response) -> dict:
        site_data = unquote(
            re.findall(r"window\.transitState = decodeURIComponent\(\"([\s\S]+?)\"\);</script>", response.text)[0]
        )
        ads = json.loads(site_data)[1][31][1]
        for ad in ads:
            ad = ad[1]
            ad = {ad[i]: ad[i+1] for i in range(0, len(ad), 2)}
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
                'actual': True,
                'source': self.name,
                'source_brand': self.get_brand(ad),
                'source_model': self.get_model(ad),
                'scraped_at': self.scraped_time,
            }
