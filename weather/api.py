from core.network_base import BaseAPIClient
from core.config import config

class WeatherAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(config.WEATHER_BASE_URL)
        self.api_key = config.WEATHER_API_KEY
        print(f"DEBUG: API Key is: {self.api_key}")

    def get_weather_data(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        return self.make_request("weather", params=params)