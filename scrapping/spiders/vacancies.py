import scrapy


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["ua.jooble.org"]
    start_urls = ["https://ua.jooble.org/SearchResult?p=2"]

    def parse(self, response):
        pass
