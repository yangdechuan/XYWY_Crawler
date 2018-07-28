# -*- coding: utf-8 -*-
import logging

import scrapy
import requests_html
import requests
from lxml import etree

from XYWYCrawler.items import XywycrawlerItem

#logging.basicConfig(level=logging.WARNING,
#                    format="{asctime} {levelname} {name} >> {message}",
#                    style="{",
#                    filename="log.txt", 
#                    filemode="w")
handler = logging.FileHandler("log.txt", mode="w", encoding="utf-8")
logger = logging.getLogger("tell_url")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class XywySpiderSpider(scrapy.Spider):      
    name = 'xywy_spider'
    allowed_domains = ['club.xywy.com']
    # start_urls = ['http://club.xywy.com/']
    def start_requests(self):
        urls = []
        cur_url = "http://club.xywy.com/keshi/{}.html"
        sess = requests_html.HTMLSession()
        for i in range(2, 3):
            response = sess.get(cur_url.format(i))
            tmp_urls = response.html.xpath("//ul[@class='club_Date clearfix']/li/a/@href")
            urls += tmp_urls
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        divs = response.xpath("//div[@class='club_dic']")
        for div in divs:
            keshi = div.xpath(".//var/a/text()").extract_first()
            title = div.xpath(".//em/a/text()").extract_first()
            url = div.xpath(".//em/a/@href").extract_first()
            contents = div.xpath(".//div[@class='club_dic_p clearfix']/p/text()").extract()
            content = "\n".join(contents)
            _id = url.split("/")[-1].replace(".htm", "").replace(".html", "")
            
            r = requests.get(url)
            html_con = etree.HTML(r.content)
            answers = html_con.xpath("//div[@class='docall clearfix ']//div[@class='pt15 f14 graydeep  pl20 pr20']/text()")

            item = XywycrawlerItem()
            item["title"] = title
            item["content"] = content
            item["url"] = url
            item["keshi"] = keshi
            item["answers"] = answers
            item["_id"] = _id

            yield item
        
        logger.warning("success crawl: {}".format(response.url))

        links = response.xpath("//div[@class='subFen']/a/@href").extract()
        texts = response.xpath("//div[@class='subFen']/a/text()").extract()
        if(texts[-1] == "[下一页]"):
            next_link = links[-1]
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse)
