from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

# full request:
# https://www.skyscanner.com/transport/flights/nyca/icn/250603/250610/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false
# base: https://www.skyscanner.com/

URL = "https://www.skyscanner.com/transport/flights/{}/{}/{}/{}/"

class Scraper:
    def __init__(self, website):
        self.website = website
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        
    def solve_captcha(self):
        try:
            # Wait for the CAPTCHA button to be clickable
            captcha_button = self.driver.find_element_by_xpath("//div[@id='px-captcha']")
            # Create ActionChains objects
            action = ActionChains(self.driver)
            click = ActionChains(self.driver)

            # Click and hold the button
            action.click_and_hold(captcha_button)
            action.perform()

            # Wait for the button to be fully filled
            time.sleep(10)

            # Release the button
            action.release(captcha_button)
            action.perform()

            # Small pause
            time.sleep(0.2)

            # Release again (this might help in some cases)
            action.release(captcha_button)
            action.perform()

            # Wait for the CAPTCHA to be solved and page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".FlightsTicket_container__MTI1N"))
            )
            print("CAPTCHA solved successfully!")
        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
            # If automatic solving fails, ask for manual intervention
            input("Please solve the CAPTCHA manually and press Enter when done...")

    def read_website(self, origin, destination, start_date, end_date):
        self.driver.get(self.website.format(origin, destination, start_date, end_date))
        
        if "CAPTCHA" in self.driver.title or "captcha" in self.driver.current_url.lower():
            self.solve_captcha()

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".FlightsTicket_container__MTI1N"))
            )
        except:
            print("Flight results did not load in time. Please check the page manually.")
            input("Press Enter after verifying the page has loaded...")

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for page to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        return self.driver.page_source
    
    def clear(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        
        flights = []
        for flight in soup.select(".FlightsTicket_container__MTI1N"):
            price = flight.select_one(".BpkText_bpk-text__ODgwN.BpkText_bpk-text--lg__ZTY1M").text
            airline = flight.select_one(".BpkText_bpk-text__ODgwN.BpkText_bpk-text--xs__MWRhZ").text
            flights.append({
                'price': float(price.replace('$', '').replace('€', '').replace(',', '')),
                'airline': airline.strip()
            })
        
        return sorted(flights, key=lambda x: x['price'])
            
    def search(self, origin, destination, start_date, end_date):
        try:
            data = self.read_website(origin, destination, start_date, end_date)
            return self.clear(data)
        finally:
            self.driver.quit()
            
    def __del__(self):
        self.driver.quit()


def main():
    scraper = Scraper(URL)
    data = scraper.search("nyca", "lon", "240811", "240818")
    for flight in data[:5]:
        print(f"Airline: {flight['airline']}, Price: ${flight['price']:.2f}")

if __name__ == "__main__":
    main()