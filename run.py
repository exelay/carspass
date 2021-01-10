import logging
import schedule
import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl('amru')
    process.crawl('autoru')

    process.start()


if __name__ == '__main__':
    schedule.every().hour.do(main)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
