import logging
import schedule
import time

from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI()
PROJECT_NAME = 'carspass'

cities = [
    'spb',
    'msk'
]


def run():
    spiders = scrapyd.list_spiders(PROJECT_NAME)
    for spider in spiders:
        for city in cities:
            scrapyd.schedule(PROJECT_NAME, spider, city=city)


if __name__ == '__main__':
    schedule.every(1).minutes.do(run)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
