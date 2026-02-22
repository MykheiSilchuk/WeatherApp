from core.network_base import BaseAPIClient
from core.config import config

class WeatherAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(config.WEATHER_BASE_URL)
        self.api_key = config.WEATHER_API_KEY
        self.units = config.UNITS
        self.lang = config.LANG

    def get_weather_data(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang
        }
        return self.make_request("weather", params=params)