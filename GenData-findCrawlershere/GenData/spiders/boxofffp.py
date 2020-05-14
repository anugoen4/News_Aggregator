# -*- coding: utf-8 -*-
import scrapy


class BoxofffpSpider(scrapy.Spider):
    name = 'boxofffp'
    allowed_domains = ['firstpost.com']
    start_urls = ['https://www.firstpost.com/entertainment/box-office/page-2']

    def parse(self, response):
        Links = response.css("div.col-md-4>div>a::attr(href)").extract()
        for Link in Links:
            yield scrapy.Request(Link, callback = self.ParseNews)

        CurrPageNum = int( response.css("a.page-link.active::text").extract_first() )
        print(CurrPageNum)
        if( CurrPageNum < 90 ):
            NextPageLink = response.css('a[rel="next"]::attr(href)').extract_first()
            yield scrapy.Request(NextPageLink, callback = self.parse)

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[itemprop="headline"]::text').extract_first()
        Source = "FirstPost"
        SourceLink = "https://www.firstpost.com/"
        ImageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first()
        if(ImageLink is None):
            ImageLink = ""
        ContentList = response.css('div.consumption>p::text').extract()
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