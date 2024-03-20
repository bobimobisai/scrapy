from selenium import webdriver
import time
import json
import scrapy


base_url = "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating"
base_url2 = (
    "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page=2&sorting=rating"
)
base_url3 = "https://www.ozon.ru/product/apple-smartfon-iphone-14-novyy-original-ne-aktivirovan-dual-sim-1-sim-2-6-128-gb-lazurnyy-786035067/?asb2=1hTFNzVDfeSqlYI4uGBUeVkIB5E_tcGGzKqqRoc50gBWftOySj-WfnFdD3bejudTjB01UBFlkVJwtmi0_Lu7lQ&avtc=1&avte=2&avts=1710891532"
with open("cook.json", "r") as cookie:
    cookies = json.load(cookie)

driver = webdriver.Chrome()


def pageOpen(url):
    driver.get(url)
    time.sleep(5)
    driver.delete_all_cookies()
    for cooks in cookies:
        driver.add_cookie(cooks)

    driver.get(url)

    time.sleep(5)

    return driver.page_source


res2 = pageOpen(base_url3)
res2 = pageOpen(base_url2)
time.sleep(25)


class MySpider(scrapy.Spider):
    name = "ozon"
    start_urls = [base_url, base_url2]

    def start_requests(self):
        pass

    def parse(self, response):
        product_links = response.xpath(
            '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]//a[starts-with(@href, "/product/")]/@href'
        ).extract()

        for link in product_links:
            full_link = "https://www.ozon.ru" + link
            yield scrapy.Request(
                url=full_link,
                callback=self.parse_product,
            )

    def parse_product(self, response):

        result = response.xpath(
            '//*[@id="section-characteristics"]/div[2]/div[8]/div[2]/dl[4]/dd'
        ).extract_first()

        yield {"result": result}
