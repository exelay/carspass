import json
import yaml
import logging
from datetime import datetime

import scrapy


class AutoSpider(scrapy.Spider):
    name = 'autoru'
    allowed_domains = ['auto.ru']
    scraped_time = datetime.now().isoformat(timespec='seconds')

    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        with open(f'dictionaries/map.{self.name}.json', 'r', encoding='utf-8') as file:
            self.dictionary = json.load(file)
        with open(f'conventions/{self.name}.yaml') as f:
            self.conventions = yaml.load(f, Loader=yaml.FullLoader)
        self.city = self.conventions['city'][city]

    def start_requests(self):
        url = f'https://auto.ru/{self.city}/cars/used/?sort=cr_date-desc&top_days=1'
        yield scrapy.Request(url=url, callback=self.parse_item, meta={'dont_proxy': True})

    @staticmethod
    def get_id(ad):
        try:
            link = ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/@href').get()
            return link.split('/')[-2].split('-')[0]
        except Exception as e:
            logging.debug(f"Failed to get id. {e}")

    @staticmethod
    def get_img_link(ad):
        try:
            img_link = ad.xpath('.//div[@class="LazyImage Brazzers__image"]/@data-src').get()
            return 'https:' + img_link
        except Exception as e:
            logging.debug(f"Failed to get image link. {e}")

    @staticmethod
    def get_publish_date(ad):
        try:
            date = ad.xpath('.//span[@class="MetroListPlace__content MetroListPlace_nbsp"]/text()').get().\
                split('\xa0')

            if len(date) < 2:
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
            return ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/text()').get()
        except Exception as e:
            logging.debug(f"Failed to get title. {e}")

    @staticmethod
    def get_price(ad):
        try:
            price = ad.xpath('.//div[@class="ListingItemPrice-module__content"]//text()')\
                .get().encode('ascii', errors='ignore')
            return int(price.decode('utf-8'))
        except Exception as e:
            logging.debug(f"Failed to get price. {e}")

    @staticmethod
    def get_mileage(ad):
        try:
            mileage = ad.xpath('.//div[@class="ListingItem-module__kmAge"]/text()').get().\
                encode('ascii', errors='ignore')
            return int(mileage.decode('utf-8'))
        except Exception as e:
            logging.debug(f"Failed to get mileage. {e}")

    @staticmethod
    def get_tech_info(ad):
        try:
            info = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][1]/text()')\
                .get().split('\u2009/\u2009')
            capacity = float(info[0].split()[0])
            power = int(info[1].split()[0])
            transmission = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][2]/text()').get()
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
            return ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/@href').get()
        except Exception as e:
            logging.debug(f"Failed to get link. {e}")

    @staticmethod
    def get_brand(ad):
        try:
            brand = ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/@href').get().split('/')[6]
            return brand
        except Exception as e:
            logging.debug(f"Failed to get brand. {e}")

    @staticmethod
    def get_model(ad):
        try:
            brand = ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/@href').get().split('/')[6]
            model = ad.xpath('.//a[@class="Link ListingItemTitle-module__link"]/@href').get().split('/')[7]
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
            year = ad.xpath('.//div[@class="ListingItem-module__year"]/text()').get()
            return int(year)
        except Exception as e:
            logging.debug(f"Failed to get year. {e}")

    def get_transmission(self, ad):
        try:
            transmission = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][2]/text()').get()
            return self.conventions['transmission'][transmission]
        except Exception as e:
            logging.debug(f"Failed to get transmission. {e}")

    def get_frame_type(self, ad):
        try:
            frame_type = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][3]/text()').get()
            return self.conventions['frame_type'][frame_type]
        except Exception as e:
            logging.debug(f"Failed to get frame type. {e}")

    @staticmethod
    def get_power(ad):
        try:
            info = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][1]/text()') \
                .get().split('\u2009/\u2009')
            power = int(info[1].split()[0])
            return power
        except Exception as e:
            logging.debug(f"Failed to get power. {e}")

    @staticmethod
    def get_volume(ad):
        try:
            info = ad.xpath('.//div[@class="ListingItemTechSummaryDesktop__cell"][1]/text()') \
                .get().split('\u2009/\u2009')
            capacity = float(info[0].split()[0])
            return float(capacity)
        except Exception as e:
            logging.debug(f"Failed to get volume. {e}")

    def parse_item(self, response):
        ads = response.xpath('//div[contains(@class, "ListingItem-module__container")]')
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
