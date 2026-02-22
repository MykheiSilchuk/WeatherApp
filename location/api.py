from core.network_base import BaseAPIClient
from core.config import config

class LocationAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(config.LOCATION_BASE_URL)
        # Auth header required by CountryregionCity API
        self.headers = {"X-CSCAPI-KEY": config.LOCATION_API_KEY}

    def get_countries(self):
        return self.make_request("countries", headers=self.headers)
    
    def get_regions(self, country_code):
        return self.make_request(f"countries/{country_code}/states", headers=self.headers)
    
    def get_cities(self, country_code, region_code):
        return self.make_request(f"countries/{country_code}/states/{region_code}/cities", headers=self.headers)