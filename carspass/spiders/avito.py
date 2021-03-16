import json
import yaml
import logging
from datetime import datetime

import scrapy
from scraper_api import ScraperAPIClient


client = ScraperAPIClient('593e157d53727b72a8a825660cd50868')


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru', 'api.scraperapi.com']
    scraped_time = datetime.now().isoformat(timespec='seconds')

    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        with open(f'dictionaries/map.{self.name}.json', 'r', encoding='utf-8') as file:
            self.dictionary = json.load(file)
        with open(f'conventions/{self.name}.yaml') as f:
            self.conventions = yaml.load(f, Loader=yaml.FullLoader)
        self.city = self.conventions['city'][city]

    def start_requests(self) -> scrapy.Request:
        url = f'https://www.avito.ru/{self.city}/avtomobili/s_probegom?radius=200&s=104'
        yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse_item, meta={'dont_proxy': True})

    @staticmethod
    def get_id(ad) -> str:
        try:
            return ad.get('id')
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad) -> str:
        try:
            return ad['gallery']['imageLargeVipUrl']
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad) -> str:
        try:
            unix_time = int(ad['sortTimeStamp']) // 1000
            return datetime.fromtimestamp(unix_time).isoformat(timespec='seconds')
        except Exception as e:
            logging.debug(f"Failed to get publish date. {e}")

    @staticmethod
    def get_title(ad) -> str:
        try:
            return ad['title']
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad) -> int:
        try:
            return ad['priceDetailed']['value']
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad) -> int:
        try:
            payload = ad['iva']['AutoParamsStep'][0]['payload']['text']
            mileage = payload.split(',')[0][:-2].replace(' ', '')
            return int(mileage)
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad) -> str:
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
    def get_location(ad) -> str:
        try:
            return ad['location']['name']
        except Exception as e:
            logging.debug(f"Failed to get location. {e}")

    @staticmethod
    def get_link(ad) -> str:
        try:
            return f"https://www.avito.ru/{ad['urlPath']}"
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    @staticmethod
    def get_brand(ad) -> str:
        try:
            brand = ad["urlPath"].split('/')[-1].split('_')[0]
            return brand
        except Exception as e:
            logging.debug(f"Failed to get brand. {e}")

    @staticmethod
    def get_model(ad) -> str:
        try:
            model = ad["urlPath"].split('/')[-1].split('_')[1]
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
            url = ad["urlPath"]
            car_metadata = url.split('/')[-1].split('_')
            return int(car_metadata[2])
        except Exception as e:
            logging.debug(f"Failed to get year. {e}")

    @staticmethod
    def get_transmission(ad) -> str:
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            transmission = car_data.split()[4].lower()
            return transmission
        except Exception as e:
            logging.debug(f"Failed to get transmission. {e}")

    def get_frame_type(self, ad) -> str:
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            frame_type = car_data.split()[7].strip(',')
            return self.conventions['frame_type'][frame_type]
        except Exception as e:
            logging.debug(f"Failed to get frame type. {e}")

    @staticmethod
    def get_power(ad) -> int:
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            power = car_data.split()[5].strip('(')
            return int(power)
        except Exception as e:
            logging.debug(f"Failed to get power. {e}")

    @staticmethod
    def get_volume(ad) -> float:
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            volume = car_data.split()[3]
            return float(volume)
        except Exception as e:
            logging.debug(f"Failed to get volume. {e}")

    def parse_item(self, response) -> dict:
        p_loader = json.loads(response.xpath('//div[@class="js-initial"]/@data-state').get())
        ads = [item for item in p_loader['catalog']['items'] if item['type'] == 'item']
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
                'actual': True,
                'source': self.name,
                'source_brand': self.get_brand(ad),
                'source_model': self.get_model(ad),
                'scraped_at': self.scraped_time,
            }
