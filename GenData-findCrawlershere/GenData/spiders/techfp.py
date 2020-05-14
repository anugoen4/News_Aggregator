# -*- coding: utf-8 -*-
import scrapy


class TechfpSpider(scrapy.Spider):
    name = 'techfp'
    allowed_domains = ['firstpost.com']
    start_urls = ['https://www.firstpost.com/tech/news-analysis/page/2']

    def parse(self, response):
        Links = response.css('div.text-wrapper>a[href*="firstpost.com"]::attr(href)').extract()
        for Link in Links:
            yield scrapy.Request(Link, callback = self.ParseNews)

        CurrPageNum = int( response.css("a.active::text").extract_first() )
        print(CurrPageNum)
        if( CurrPageNum < 250 ):
            NextPageLink = response.css('a[rel="next"]::attr(href)').extract_first()
            yield scrapy.Request(NextPageLink, callback = self.parse)

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1.post-title::text').extract_first()
        Source = "FirstPost"
        SourceLink = "https://www.firstpost.com/"
        ImageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first()
        if(ImageLink is None):
            ImageLink = ""
        ContentList = response.css('div.text-content-wrap>p::text').extract()
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