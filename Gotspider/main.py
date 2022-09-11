# import os
# os.system('scrapy crawl snowfox')
from scrapy import cmdline

cmdline.execute("scrapy crawlall".split())