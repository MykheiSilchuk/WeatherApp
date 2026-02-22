from weather.icon_api import WeatherIconAPI


class WeatherIconService:
    def __init__(self, api=None):
        self.api = api or WeatherIconAPI()
        self.cache = {} 

    def get_icon(self, icon_code: str) -> dict:
        if icon_code not in self.cache:
            self.cache[icon_code] = self.api.get_icon(icon_code)
        return self.cache[icon_code]