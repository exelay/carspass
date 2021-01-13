import json
import yaml
import logging
from datetime import datetime
from requests import PreparedRequest

import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    url = str()
    proxy_url = "https://app.scrapingbee.com/api/v1/"

    def start_requests(self):
        req = PreparedRequest()

        self.url = 'https://www.avito.ru/sankt-peterburg/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?s=104'
        proxy_params = {
            "api_key": "EHW1NW8Y19PCOMPHBDARWQ2A1BOS6GIDEP9ZBWAWUXX6BUE0PIIL94PUW813WY6LISV941770L7R2U4B",
            "url": self.url,
            "render_js": "false",
        }
        req.prepare_url(self.proxy_url, proxy_params)
        url = req.url

        yield scrapy.Request(url=url, callback=self.parse_item)

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
    def get_publish_date(ad):
        try:
            unix_time = int(ad['sortTimeStamp']) // 1000
            return datetime.fromtimestamp(unix_time).isoformat()
        except Exception as e:
            logging.debug(f"Failed to get publish date. {e}")

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
            mileage = payload.split(',')[0][:-2].replace(' ', '')
            return int(mileage)
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

    @staticmethod
    def get_brand(ad):
        try:
            url = ad["urlPath"]
            car_metadata = url.split('/')[-1].split('_')
            return car_metadata[0]
        except Exception as e:
            logging.debug(f"Failed to get brand. {e}")

    @staticmethod
    def get_model(ad):
        try:
            url = ad["urlPath"]
            car_metadata = url.split('/')[-1].split('_')
            return car_metadata[1]
        except Exception as e:
            logging.debug(f"Failed to get model. {e}")

    @staticmethod
    def get_year(ad):
        try:
            url = ad["urlPath"]
            car_metadata = url.split('/')[-1].split('_')
            return int(car_metadata[2])
        except Exception as e:
            logging.debug(f"Failed to get year. {e}")

    @staticmethod
    def get_transmission(ad):
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            transmission = car_data.split()[4].lower()
            return transmission
        except Exception as e:
            logging.debug(f"Failed to get transmission. {e}")

    def get_frame_type(self, ad):
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            frame_type = car_data.split()[7].strip(',')
            with open(f'conventions/{self.name}.yaml') as f:
                frame_types = yaml.load(f, Loader=yaml.FullLoader)['frame_type']
            return frame_types[frame_type]
        except Exception as e:
            logging.debug(f"Failed to get frame type. {e}")

    @staticmethod
    def get_power(ad):
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            power = car_data.split()[5].strip('(')
            return int(power)
        except Exception as e:
            logging.debug(f"Failed to get power. {e}")

    @staticmethod
    def get_volume(ad):
        try:
            car_data = ad['iva']['AutoParamsStep'][0]['payload']['text']
            volume = car_data.split()[3]
            return float(volume)
        except Exception as e:
            logging.debug(f"Failed to get volume. {e}")

    def parse_item(self, response):
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
                'year': self.get_year(ad),
                'transmission': self.get_transmission(ad),
                'frame_type': self.get_frame_type(ad),
                'power': self.get_power(ad),
                'volume': self.get_volume(ad),
                'metro': None,
                'link': self.get_link(ad),
                'actual': True,
                'source': self.name,
                'scraped_at': datetime.now().isoformat(),
            }
