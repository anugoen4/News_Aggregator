# -*- coding: utf-8 -*-
import scrapy

class FirstpostSpider(scrapy.Spider):
    name = 'firstpost'
    allowed_domains = ["firstpost.com"]
    start_urls = ["https://www.firstpost.com/page/2"]

    def parse(self, response):
        Links = response.css("a.list-item-link::attr(href)").extract()
        i = 0
        for Link in Links:
            if(i >= 10):
                break
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[class*="title"]::text').extract_first(default="")
        Source = "FirstPost"
        SourceLink = "https://www.firstpost.com/"
        ImageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first(default="")
        ContentList = response.css('div[class*="-content"]>p::text').extract()
        Content = ""
        for Para in ContentList:
            Content += Para
        Output = {
            "HL": HeadL,
            "HLink": HLink,
            "Src": Source,
            "SrcLink": SourceLink,
            "ImgLink": ImageLink,
            "Text": Content
        }
        yield Output

