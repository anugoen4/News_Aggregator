# -*- coding: utf-8 -*-
import scrapy


class CricketfpSpider(scrapy.Spider):
    name = 'cricketfp'
    allowed_domains = ['firstpost.com']
    start_urls = ['https://www.firstpost.com/firstcricket/sports-news/']

    def parse(self, response):
        Links = response.css("a.item::attr(href)").extract()
        for Link in Links:
            yield scrapy.Request(Link, callback = self.ParseNews)

        CurrPageNum = int( response.css("a.active::text").extract_first() )
        print(CurrPageNum)
        if( CurrPageNum == 9 ):
            NextPageLink = "https://www.firstpost.com/firstcricket/sports-news/page/20"
            yield scrapy.Request(NextPageLink, callback = self.parse)
        if( CurrPageNum < 72 ):
            NextPageLink = response.css('a[rel="next"]::attr(href)').extract_first()
            yield scrapy.Request(NextPageLink, callback = self.parse)

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1.story-title::text').extract_first()
        Source = "FirstPost"
        SourceLink = "https://www.firstpost.com/"
        ImageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first()
        if(ImageLink is None):
            ImageLink = ""
        ContentList = response.css('div.article-full-content>p::text').extract()
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
