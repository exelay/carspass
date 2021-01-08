from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())


def main():
    process.crawl('amru')
    process.crawl('autoru')

    process.start()


if __name__ == '__main__':
    main()
