# -*- coding: utf-8 -*-
import scrapy


class NdtvSpider(scrapy.Spider):
    name = 'ndtv'
    allowed_domains = ['ndtv.com']
    start_urls = ['https://www.ndtv.com/top-stories']

    def parse(self, response):
        Links = response.css("div.nstory_header>a::attr(href)").extract()
        i = 0
        for Link in Links:
            if(i >= 10):
                break
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[itemprop="headline"]::text').extract_first(default="")
        Source = "FirstPost"
        SourceLink = "https://www.firstpost.com/"
        ImageLink = response.css("img#story_image_main::attr(src)").extract_first(default="")

        ContentList = response.css('div[itemprop="articleBody"]>p::text').extract()
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