import logging

import scrapy


class AutoSpider(scrapy.Spider):
    name = 'autoru'
    allowed_domains = ['auto.ru']

    def start_requests(self):
        url = 'https://auto.ru/sankt-peterburg/cars/used/?sort=cr_date-desc&top_days=1'
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
