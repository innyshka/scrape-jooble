import scrapy
from scrapy.selector import Selector
from scrapy.http import Response
from selenium import webdriver
import time

from selenium.webdriver.common.by import By


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["ua.jooble.org"]
    start_urls = ["https://ua.jooble.org/SearchResult?ukw=python%20developer"]
    def __init__(self):
        self.driver = webdriver.Chrome()

    def handle_special_button(self):
        try:
            special_button = self.driver.find_element(By.CSS_SELECTOR,
                                                      ".jkit_AySJs.jkit_eN9GM.jkit_KD_j8.jkit_poLCo.TTTs-J")
            special_button.click()
            time.sleep(5)
            return True
        except Exception as e:
            print("Exception while handling special button:", e)
            return False


    def handle_close_button(self):
        try:
            close_button = self.driver.find_element(By.CSS_SELECTOR,
                                               ".jkit_Ccqe_.jkit_phOlM.jkit_MDaX0.jkit_QFRb9.jkit_xvodn.SpP7vI")  # Знаходимо кнопку закриття
            close_button.click()  # Клікаємо на кнопку закриття
        except Exception as e:
            print("Рекламне вікно не виявлено або вже закрите:", e)

    def scroll_to_load_content(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                if not self.handle_special_button():
                    break
            last_height = new_height

    def parse(self, response: Response, **kwargs):
        self.driver.get(response.url)
        self.handle_close_button()
        self.scroll_to_load_content()

        sel = Selector(text=self.driver.page_source)
        for vacancy in sel.css(".ojoFrF"):
            yield {
                "title": vacancy.css(".jkit_Efecu::text").get()
            }

    def closed(self, reason):
        self.driver.quit()
