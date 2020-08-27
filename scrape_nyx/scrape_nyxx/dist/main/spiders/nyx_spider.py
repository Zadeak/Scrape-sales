import scrapy
import os
from .items import ScrapeNyxItem


def clean_price(text):
    digits = [ symbol for symbol in text if symbol.isdigit() or symbol == ","]
    cleaned_text = ''.join(digits)
    if not cleaned_text:
        return None
    else:
        return cleaned_text

def clean_name(text):
    symbols = [ symbol for symbol in text if symbol.isalpha()]
    cleaned_text = ''.join(symbols)
    if not cleaned_text:
        return None
    else:
        return cleaned_text


class PricesSpider(scrapy.Spider):

    name = "prices"
    filepath = os.path.abspath("") + "\data"
    custom_settings = {
        'FILE_STORE': filepath,

    }
    start_urls = ["https://www.kaubamaja.ee/ilu/brandid/nyx-professional-makeup"]



    def parse(self, response):
        items = ScrapeNyxItem()
        for product_div in response.css('li.products-grid__item'):
            isExists = product_div.css('.old-price').extract_first(default='not-found')
            if isExists == 'not-found':
                pass
            else:
                title = product_div.css(".products-grid__name.product-name::text").getall()
                new_title = title[1]

                price_box = product_div.css(".price-box")
                old_price = price_box.css('.old-price')
                raw_old_cost = old_price.css('.price::text').get()
                old_cost = raw_old_cost and clean_price(raw_old_cost) or None
                new_cost = price_box.css('.special-price')
                raw_new_price = new_cost.css('.price::text').get()
                new_price = raw_new_price and clean_price(raw_new_price) or None
                link = product_div.css('a.product-image')
                href = link.css('::attr(href)').get()
                picture = product_div.css('.products-grid__image')
                picture_link = picture.css('img').xpath('@src').getall()
                items["title"] = new_title
                items["old_cost"] = old_cost
                items["new_price"] = new_price
                items["link"] = href
                if len(picture_link) > 1:
                    items["picture"] = picture_link[1]
                else:
                    items["picture"] = picture_link[0]

                yield  items
        next_page = response.css('li.pagination__item a.pagination__link.pagination__link--next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)




