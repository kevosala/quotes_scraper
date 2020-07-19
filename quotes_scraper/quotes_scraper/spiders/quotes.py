import scrapy

#Titulo web = //h1/a/text()
#citas = //span[@class="text" and @itemprop="text"]/text()
#Top10 = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
# o =    response.xpath('//div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()').getall()

class QuotesSpider(scrapy.Spider):
    name = 'quotes' #Nombre unico con el que scrapy se va refereir a este spider dentro del proyecto
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ] #peticion http

    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT':'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 1048,
        'MEMUSAGE_NOTIFY_MAIL':['kevin.sala94@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'KSZ',
        'FEED_EXPORT_ENCODING': 'utf-8'

    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
        else:
            yield {
                'quotes':quotes
            }

        

    def parse(self,response): #analizar un archivo para extraer información 
        
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield{
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
