# -*- coding: utf-8 -*-
import scrapy


class IndiatodaySpider(scrapy.Spider):
    name = 'indiatoday'
    allowed_domains = ['indiatoday.in']
    start_urls = ['https://www.indiatoday.in/']

    def parse(self, response):
        Links = response.css('li[class*="top-story-"]>a::attr(href)').extract()
        i = 0
        for Link in Links:
            if(i >= 10):
                break
            Link = response.urljoin(Link)
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[itemprop="headline"]::text').extract_first(default="")
        Source = "India Today"
        SourceLink = "https://www.indiatoday.in/"
        ImageLink = response.css('img[itemprop="contentUrl"]::attr(src)').extract_first(default="")
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