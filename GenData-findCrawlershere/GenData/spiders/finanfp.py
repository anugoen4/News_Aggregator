# -*- coding: utf-8 -*-
import scrapy


class FinanfpSpider(scrapy.Spider):
    name = 'finanfp'
    allowed_domains = ['firstpost.com']
    start_urls = ['https://www.firstpost.com/category/business/page/2']

    def parse(self, response):
        Links = response.css("ul.articles-list>li>a::attr(href)").extract()
        for Link in Links:
            yield scrapy.Request(Link, callback = self.ParseNews)

        NextPageLink = response.css('a[rel="next"]::attr(href)').extract_first()

        if(int(NextPageLink) < 250):
            NextPageLink = response.urljoin(NextPageLink)
            yield scrapy.Request(NextPageLink, callback = self.parse)

    def ParseNews(self, response):
        HLink = response.url      
        HeadL = response.css('h1[itemprop="headline"]::text').extract_first()
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
