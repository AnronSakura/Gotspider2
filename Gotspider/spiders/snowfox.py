# -*- coding: utf-8 -*-

import scrapy
import redis
from lxml import etree
from random import randint
from scrapy.http.request import Request
from scrapy import Selector
from lxml import etree
from Gotspider2.items import Gotspider2Item

class SnowfoxSpider(scrapy.Spider):
    name = 'snowfox'
    allowed_domains = 'https://www.gdwxcn.com'
    start_urls = 'https://www.gdwxcn.com/jinyong/xsfh/'
    tail_url = '.html'
    #从start_requests发送请求
    def start_requests(self):
        USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
        yield scrapy.Request(url=self.start_urls,callback=self.parse1)

    def parse1(self, response):
        son_urls=response.xpath('//div[@class="zhangjie"]/ul/li/a/@href').extract()
        
        for son_url in son_urls:#章节链接
            son_url=self.allowed_domains+son_url
            item = Gotspider2Item()
            item['url']=son_url
            yield scrapy.Request(url=son_url,meta={'item':item},callback=self.parse2,dont_filter=True)
        
    
    def parse2(self, response):
        item = response.meta['item']
        self.characterlists=[]
        with open(r'D:/PFE/srtp/共现矩阵/np_雪山飞狐.txt', 'r',encoding='GBK') as f:
            lines = f.readlines()
        for line in lines:
            self.characterlists.append((line.strip()).split('\t'))
        
        selector = etree.HTML(response.text)
        content =  ''.join(list(map(lambda p: p.strip(),selector.xpath('//div[@class="xszwy"]/div[@class="xsnr"]/div[@class="xstext"]/text()'))))
        item['content'] = content#章节内容
        characters = []
        for row in self.characterlists:
            for role in row:
                if role in content:
                    characters.append(role)
        item['characters'] = '/'.join(list(set(characters)))#人物
        
        chapter=response.xpath('//div[@class="xszwy"]/div[@class="xsnr"]/h1/text()').extract()
        #章节名称
        item['chapter']=chapter[0]
        yield item
