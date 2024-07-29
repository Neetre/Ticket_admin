from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

# full request:
# https://www.skyscanner.com/transport/flights/nyca/icn/250603/250610/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false
# base: https://www.skyscanner.com/

URL = "https://www.skyscanner.com/transport/flights/{}/{}/250603/250610/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"

class Scraper:
    def __init__(self, website):
        self.website = website
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def read_website(self, origin, destination, date):
        self.driver.get(self.website)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "BpkText_bpk-text__ODgwN BpkText_bpk-text--xs__MWRhZ"))
        )
        page_source = self.driver.page_source
        with open("../data/website.html", "w") as file:
            file.write(page_source)
        return page_source
    
    def clear(self, data):
        soup = BeautifulSoup(data, "html.parser")
        airlines = soup.find("span", class_="BpkText_bpk-text__ODgwN BpkText_bpk-text--xs__MWRhZ").text
        for airline in airlines[:10]:
            print(airline)
            
    def search(self, origin, destination, date):
        data = self.read_website(origin, destination, date)
        return self.clear(data)
            
    def __del__(self):
        self.driver.quit()


def main():
    scraper = Scraper(URL)
    request = scraper.read_website()
    if request.status_code == 200:
        print("OK")
    else:
        print("Womp Womp")

    with open("../data/website.html", "w") as file:
        file.write(request.text)

    scraper.clear(request.text)


if __name__ == "__main__":
    main()