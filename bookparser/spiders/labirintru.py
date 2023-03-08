import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@title="Следующая"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_books)




    def parse_books(self, response: HtmlResponse):
        name = response.xpath('//div[@id="product-about"]/h2/text()').get()
        authors = response.xpath("//a[@data-event-label='author']/text()").get()
        sale = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        action_sale = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rate = response.xpath('//div[@id="rate"]/text()').get()
        url = response.url

        yield BookparserItem(name=name, authors=authors, sale=sale, action_sale=action_sale, rate=rate, url=url)

