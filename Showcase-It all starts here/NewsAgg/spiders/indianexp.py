# -*- coding: utf-8 -*-
import scrapy


class IndianexpSpider(scrapy.Spider):
    name = 'indianexp'
    allowed_domains = ['indianexpress.com']
    start_urls = ['https://www.indianexpress.com/latest-news/2/']

    def parse(self, response):
        Links = response.css("div.title>a::attr(href)").extract()

        i = 0
        for Link in Links:
            if(i >= 10):
                break
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[itemprop="headline"]::text').extract_first(default="")
        Source = "The Indian Express"
        SourceLink = "https://indianexpress.com/"
        ImageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first(default="")
        
        ContentList = response.css('div.full-details>p::text').extract()
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
