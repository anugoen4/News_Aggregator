# -*- coding: utf-8 -*-
import scrapy

class ThehinduSpider(scrapy.Spider):
    name = 'thehindu'
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/sitemap/']

    def parse(self, response):
        Links = response.css("article>a::attr(href)").extract()
        i = 0
        for Link in Links:
            if(i >= 10):
                break
            yield scrapy.Request(Link, callback = self.ParseNews)
            i += 1

    def ParseNews(self, response):
        HeadL = response.css("h1.title::text").extract_first(default="")
        HLink = response.url
        Source = "The Hindu"
        SourceLink = "https://www.thehindu.com/"
        ImageLink = response.css("img.lead-img::attr(src)").extract_first(default="")

        ContentList = response.css('div[id^="content-body-"]>p::text').extract()
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