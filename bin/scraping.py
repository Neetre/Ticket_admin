from bs4 import BeautifulSoup
import requests

# full request:
# https://www.skyscanner.com/transport/flights/nyca/icn/250603/250610/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false
# base: https://www.skyscanner.com/

URL = "https://www.skyscanner.com/transport/flights/nyca/icn/250603/250610/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"

class Scraper:
    def __init__(self, website):
        self.website = website

    def read_website(self):
        return requests.get(self.website)
    
    def clear(self, data):
        soup = BeautifulSoup(data, "html.parser")
        airlines = soup.find("span", class_="BpkText_bpk-text__ODgwN BpkText_bpk-text--xs__MWRhZ").text
        for airline in airlines[:10]:
            print(airline)


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