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
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

COOKIES_DEBUG = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/"
#               "apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "cookie": "yandexuid=5324645381598645529; yuidss=5324645381598645529; "
#               "ymex=1914005529.yrts.1598645529#1914005529.yrtsi.1598645529; _ym_uid=1598869015161464602; "
#               "my=YwA=; gdpr=0; yandex_login=alexeykirpa; yabs-sid=1955603231602190189; "
#               "i=MegyYOZZz6WdDgHuRhybzKC8ej3WehyQR/+LNFrUkVb0wQV9BvpAkr9GpkeM4WA35dZMTIJ/XjOlRJQQVaFjVCNSQZc=; "
#               "_ym_d=1606568652; yabs-frequency=/5/0W000EgQZLy00000/vdUmS9K00010FY1C1NDmb000040-8Ki5St2K0000G3uX/; "
#               "is_gdpr=0; is_gdpr_b=CLuMORDGDygC; HOhdORSx=1; "
#               "ys=udn.cDrQkNC70LXQutGB0LXQuSDQmtC40YDQv9Cw#c_chck.56096774; "
#               "Session_id=3:1610022364.5.0.1599834695875:Nh25XQ:4.1|555458220.0.2|228431.196368."
#               "swu8rspoyqSUAJvuXc87Mz6ZuqQ; sessionid2=3:1610022364.5.0.1599834695875:Nh25XQ:4.1|555458220.0.2|"
#               "228431.147426.s7pyWgXj0FCKZcDABnf8mnW8xGE",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
#                   "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
# }

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
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 0.25
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 0.5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORT_ENCODING = 'utf-8'
