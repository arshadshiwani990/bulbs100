import scrapy
import json
import re


class A1000bulbsSpiderSpider(scrapy.Spider):
    name = '1000bulbs_spider'
    allowed_domains = ['1000bulbs.com']
    start_urls = ['http://1000bulbs.com/']

    def start_requests(self):
    
        # url='https://www.1000bulbs.com/fil/search?q=red'
        url='https://www.1000bulbs.com/fil/sitemaps/product.xml'
        yield scrapy.Request(url=url, callback=self.parse_site_map)


    def parse_site_map(self,response):


        products=re.findall('loc>(.+\/product\/[^<]+)',response.text)
        for product in products:

            yield scrapy.Request(url=product, callback=self.parse_product_page)
    
    def parse_product_page(self, response):
        
        title=response.xpath('//h1[@class="primary-color smaller"]/strong/text()').get()
        sku=response.xpath('//div[@class="sku"]/strong/following-sibling::text()').get().replace('\n"', '').strip()
        bulletpoints=response.xpath('//div[@class="small-12 columns truncate tooltip-container"]/ul/li/text()').extract()
        price=response.xpath('//div[@class="product-price"]//strong[@class="price"]/text()').get()
        specs=response.xpath('//div[@id="Specifications"]//table//tr')
        
        specs_dict={}
        for spec in specs:
            spec_name=spec.xpath('.//th/strong/text()').get()
            spec_value=spec.xpath('.//td/text()').get()
            specs_dict[spec_name]=spec_value
        

        item = {
            'upc': specs_dict.get('UPC'),
            'unit_price': price,
            'title': title,
            'description': response.xpath('//meta[@name="description"]/@content').get(),
            'image': response.xpath('//div[@data-image]/@data-image').get(),
            'url':response.url,
            # 'inc_vat_price': inc_vat_price.replace('£', '') if inc_vat_price else None
            
        }
        
        yield item
        