import scrapy


class QuotesSpider(scrapy.Spider):
    name = "science"

    #urls_list = []
    #for i in range(1,5): #253
        #urls_list.append("https://www.sciencemag.org/careers/articles?page="+str(i))

    def start_requests(self):
        urls_list = []
        for i in range(1,5): #254
            urls_list.append("https://www.sciencemag.org/careers/articles?page="+str(i))
        #urls = ["https://www.sciencemag.org/careers/articles?page=10", "https://www.sciencemag.org/careers/articles?page=11", "https://www.sciencemag.org/careers/articles?page=12", "https://www.sciencemag.org/careers/articles?page=13"]
        for url in urls_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for block in response.css("div.media__body"):
            yield {
                "text" : block.css("a::text").get(),
                "preview" : block.css("div.media__deck::text").get(),
                "byline" : block.css("p.byline").get()
            }

