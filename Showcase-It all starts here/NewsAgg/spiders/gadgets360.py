# -*- coding: utf-8 -*-
import scrapy


class Gadgets360Spider(scrapy.Spider):
    name = 'gadgets360'
    allowed_domains = ['gadgets.ndtv.com']
    start_urls = ['https://gadgets.ndtv.com/news/']

    def parse(self, response):
        Links = response.css("div.caption_box>a::attr(href)").extract()
        i = 0
        for Link in Links:
            if(i >= 10):
                break
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('div.lead_heading>h1::text').extract_first(default="")
        Source = "Gadgets360"
        SourceLink = "https://gadgets.ndtv.com/"
        ImageLink = response.css('img[src*="i.gadgets360cdn.com"]::attr(src)').extract_first(default="")
        ContentList = response.css('div.content_text>p::text').extract()
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