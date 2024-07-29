import os
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

SKYSCANNER = os.environ.get("SKYSCANNER")
KAYAK = os.environ.get("KAYAK")

class FlightSearchEngine:
    def __init__(self):
        self.api_keys = {
            "skyscanner" : SKYSCANNER,
            "kayak" : KAYAK,
            # should add more
        }

    def search_flights(self, origin, destination, date):
        results = []
        results.extend(self._search_skyscanner(origin, destination, date))
        results.extend(self._search_kayak(origin, destination, date))
        # add more API searches
        return sorted(results, key=lambda x: x['price'])
    
    def _search_skyscanner(self, origin, destination, date):
        # skyscanner research
        pass

    def _search_kayak(self, origin, destination, date):
        # kayak research
        pass


def main():
    search_engine = FlightSearchEngine()
    best_flights = search_engine.search_flights("NYC", "LON", datetime(2024, 8, 1))
    for flight in best_flights:
        print(f"Airline: {flight['airline']}, Price: {flight['price']}")