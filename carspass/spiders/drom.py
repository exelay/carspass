import yaml
import logging
from datetime import datetime
from dateutil.parser import parse

import scrapy


class DromSpider(scrapy.Spider):
    name = 'drom'
    allowed_domains = ['drom.ru']

    def start_requests(self):
        url = 'https://spb.drom.ru/auto/used/all/'
        yield scrapy.Request(url=url, callback=self.parse_item)

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
                'source': self.name,
                'scraped_at': datetime.now().isoformat(),
            }
