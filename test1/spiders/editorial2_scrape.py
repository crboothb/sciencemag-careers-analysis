import scrapy


class QuotesSpider(scrapy.Spider):
    name = "science_article"

    def start_requests(self):
        urls_list = ["https://www.sciencemag.org/careers/articles"]
        for i in range(255): #254
            urls_list.append("https://www.sciencemag.org/careers/articles?page="+str(i))
        #urls = ["https://www.sciencemag.org/careers/articles?page=10", "https://www.sciencemag.org/careers/articles?page=11", "https://www.sciencemag.org/careers/articles?page=12", "https://www.sciencemag.org/careers/articles?page=13"]
        for url in urls_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_tags(self, response):
        post = response.css("div.meta-line")
        yield {
            "headline" : response.css("h1.article__headline::text").get(),
            "tags" : post.css("a::text").getall(),
            "byline" : response.css("p.byline").get(),
            "text" : response.css("p::text").getall()
        }

    def parse(self, response):
        # for block in response.css("div.media__body"):
            # yield {
                # "text" : block.css("a::text").get(),
                # "preview" : block.css("div.media__deck::text").get(),
                # "byline" : block.css("p.byline").get()
            # }
        for block in response.css("div.media__body"):
            href = block.css("a::attr(href)")[0]
            # print("href!!!!!!!!!!!!!   ", href)
            yield response.follow(href, self.parse_tags)