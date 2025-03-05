import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    
    custom_settings = {
        'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS': 32,  # More simultaneous requests
        'DOWNLOAD_DELAY': 0,        # No delay (site is built for scraping)
        'LOG_LEVEL': 'INFO',        # Reduce verbosity
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 3600,  # Cache for one hour
    }
    
    def parse(self, response):
        # Extract basic data from the current page
        data = {
            'url': response.url,
            'title': response.css('title::text').get()
        }
        yield data
        
        # Extract all internal links (using a simple filter for links starting with '/')
        links = response.css('a::attr(href)').getall()
        for link in links:
            # Only follow internal links (relative links or absolute ones on quotes.toscrape.com)
            if link.startswith('/') or "quotes.toscrape.com" in link:
                full_url = response.urljoin(link)
                yield response.follow(full_url, callback=self.parse)
