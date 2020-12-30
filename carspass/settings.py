# Scrapy settings for carspass project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'carspass'

SPIDER_MODULES = ['carspass.spiders']
NEWSPIDER_MODULE = 'carspass.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/86.0.4240.198 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
# CONCURRENT_REQUESTS_PER_IP = 5

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/"
              "apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cookie": "_csrf_token=072e78d64aaa00059e347bb6f08cc1ec233e274bdb3e9303; "
              "suid=62d66ddf8744e5905ddb28c71e252964.bb3de41a5069195d6e9a472c32784fae; "
              "from=direct; _ym_uid=16025271801045893798; bltsr=1; yandexuid=5324645381598645529; "
              "my=YwA%3D; gdpr=0; gids=213; gradius=1000; mmm-search-accordion-is-open-cars=%5B0%5D; "
              "pro_avto_popup=closed; yuidlt=1; "
              "autoru_sid=a%3Ag5f9984df22n2pejuqk1j1s6271ed0oa.e864bdc97bfbcd4651c8ea3f75f70ade%7C1605106143960.604800."
              "mfd1CLI3jQBtrQCt05Ft2A.vQ53nxCy62tk33W6IAh1_Vu3lExMX79IVL2f9Jo4z6E; "
              "crookie=PnWKG85CKJZVTexFSQo9V3rlbxplIHaIaMgIasyAvanzqQhJnWx25cAlio0uu86YINYoPeKIIJbV3FoOvGpycwnmyWc=; "
              "cmtchd=MTYwNTAxMDc0NzIzOA==; "
              "autoruuid=g5f9984df22n2pejuqk1j1s6271ed0oa.e864bdc97bfbcd4651c8ea3f75f70ade; "
              "yuidcs=1; parts_ur=; _ym_isad=1; autoru_gdpr=1; X-Vertis-DC=sas; proven_owner_popup=closed; "
              "_ym_visorc_22753222=b; from_lifetime=1605276065824; _ym_d=1605276066,",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'carspass.middlewares.CarspassSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'carspass.middlewares.CarspassDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'carspass.pipelines.MongodbPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.25
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 0.5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORT_ENCODING = 'utf-8'
