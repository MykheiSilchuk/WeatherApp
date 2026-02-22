from core.network_base import BaseAPIClient
from core.config import config

class WeatherAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(config.WEATHER_BASE_URL)

    def get_weather_data(self, city: str):
        params = {
            "q": city,
            "appid": config.WEATHER_API_KEY,
            "units": "metric",
            "lang": "en"
        }
        return self.make_request("weather", params=params)