# -*- coding: utf-8 -*-
import scrapy
import requests_html

from XYWYCrawler.items import XywycrawlerItem

class XywySpiderSpider(scrapy.Spider):
    name = 'xywy_spider'
    allowed_domains = ['club.xywy.com']
    # start_urls = ['http://club.xywy.com/']
    def start_requests(self):
        urls = []
        cur_url = "http://club.xywy.com/keshi/{}.html"
        sess = requests_html.HTMLSession()
        for i in range(1, 65):
            response = sess.get(cur_url.format(i))
            tmp_urls = response.html.xpath("//ul[@class='club_Date clearfix']/li/a/@href")
            urls += tmp_urls
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        divs = response.xpath("//div[@class='club_dic']")
        sess = requests_html.HTMLSession()
        for div in divs:
            keshi = div.xpath(".//var/a/text()").extract_first()
            title = div.xpath(".//em/a/text()").extract_first()
            url = div.xpath(".//em/a/@href").extract_first()
            contents = div.xpath(".//div[@class='club_dic_p clearfix']/p/text()").extract()
            content = "\n".join(contents)

            r = sess.get(url)
            answers = []
            answer_divs = r.html.xpath("//div[@class='docall clearfix ']")
            for answer_div in answer_divs:
                ans = answer_div.find("div")[12].text
                answers.append(ans)

            item = XywycrawlerItem()
            item["title"] = title
            item["content"] = content
            item["url"] = url
            item["keshi"] = keshi
            item["answers"] = answers

            yield item

        links = response.xpath("//div[@class='subFen']/a/@href").extract()
        texts = response.xpath("//div[@class='subFen']/a/text()").extract()
        if(texts[-1] == "[下一页]"):
            next_link = links[-1]
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse)
