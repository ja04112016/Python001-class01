# Scrapy settings for myspiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspiders'

SPIDER_MODULES = ['myspiders.spiders']
NEWSPIDER_MODULE = 'myspiders.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
from fake_useragent import UserAgent
USER_AGENT = UserAgent().random

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   # 'Accept-Language': 'en',
    'cookie': '__mta=209157805.1593309164768.1593319601419.1593319967898.7; uuid_n_v=v1; uuid=E2AC5A80B8E111EA8E55532676AF0F4ABBEC4D0BCC524EA6A5FF45153286A02C; _csrf=2bb5acd48624d7ade08e012416085013abddcf550c3cff4acc67d44521219101; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593309165; _lxsdk_cuid=172f8a074b2c8-0a746d91ea30e2-143c6251-13c680-172f8a074b2c8; _lxsdk=E2AC5A80B8E111EA8E55532676AF0F4ABBEC4D0BCC524EA6A5FF45153286A02C; mojo-uuid=466965e267abff0399749a463a65f406; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593486113; __mta=209157805.1593309164768.1593319967898.1593486113115.8; _lxsdk_s=1730358a860-2d6-970-131%7C%7C1'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'myspiders.middlewares.MyspidersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'myspiders.middlewares.MyspidersDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'myspiders.pipelines.MyspidersPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
