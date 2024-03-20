from selenium import webdriver
import time
import json
import scrapy
import os

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

    def start_requests(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, "test.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        yield scrapy.Request(
            url="file:///" + file_path, callback=self.parse, dont_filter=True
        )

    def parse(self, response):
        product_links = response.xpath(
            '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]//a[starts-with(@href, "/product/")]/@href'
        ).extract()

        if product_links:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(current_dir, "links.txt")
            with open(filename, "w") as f:
                for link in product_links:
                    f.write(link + "\n")

            self.log(f"Saved links to {filename}")
