# coding=UTF-8

import scrapy
import json

#'http://www.accupass.com/search/changeconditions/r/0/'+ str(num) +'/5/0/0/'+ str(page) +'/00010101/99991231'
#str(num)=1:藝文, str(page)=0:第一頁
#scrapy crawl accupass -o art_keywords.json


class AccupassSpider(scrapy.Spider):
    name = "accupass"
    start_urls = ["http://www.accupass.com/search/changeconditions/r/0/13/5/0/0/0/00010101/99991231"]
    
    #抓取本頁所有活動網址和下一頁網址
    def parse(self, response):            
        #print response.url
        
        #活動網址
        events = response.xpath('//div[@event-row]/@event-row').extract()
        print(events)
        for event in events:
            event_id = json.loads(event)['eventIdNumber']
            event_url = "http://www.accupass.com/event/register/" + event_id
            yield scrapy.Request(event_url, callback=self.parse_event)
        
        #下一頁網址
        url = response.xpath('//a[contains(.,">")]/@href').extract()[0][8:]
        if url != "javascript:;":
            next_url = "http://www.accupass.com/search/changeconditions/" + url
            yield scrapy.Request(next_url, callback=self.parse)

    #抓取本頁活動關鍵字        
    def parse_event(self, response):
        yield {
            "subject" : response.xpath('//meta[@name="subject"]/@content').extract()[0].encode('utf8'),
            "description" : response.xpath('//meta[@name="description"]/@content').extract()[0].encode('utf8'),
            "keywords" : response.xpath('//meta[@name="keywords"]/@content').extract()[0].encode('utf8'),
            "class" : "other"
        }  
        
 
        
        