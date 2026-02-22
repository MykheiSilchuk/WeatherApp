import pytest
from weather.service import WeatherService
from core.errors import WeatherError, NetworkError, CityNotFoundError


class FakeWeatherAPI:
    def __init__(self, temp=20, desc="clear sky"):
        self.temp = temp
        self.desc = desc

    def get_weather_data(self, city: str): 
        return {
            "name": city,
            "main": {
                "temp": self.temp,
                "feels_like": self.temp - 1,
                "humidity": 60,
                "pressure": 1013,
            },
            "weather": [{"description": self.desc, "icon": "01d"}],
        }


class FailingWeatherAPI:
    def __init__(self, error):
        self.error = error

    def get_weather_data(self, city: str):
        raise self.error


def test_get_weather_returns_parsed_data():
    api = FakeWeatherAPI(temp=25, desc="sunny")
    service = WeatherService(api)

    data = service.get_weather("Kyiv")

    assert data["temperature"] == 25  
    assert data["description"] == "sunny"
    assert data["city"] == "Kyiv"


def test_get_weather_calls_api_with_correct_city():
    called = {}

    class SpyAPI(FakeWeatherAPI):
        def get_weather_data(self, city: str):
            called["city"] = city
            return super().get_weather_data(city)

    service = WeatherService(SpyAPI())
    service.get_weather("Lviv")

    assert called["city"] == "Lviv"


def test_get_weather_raises_city_not_found():
    api = FailingWeatherAPI(CityNotFoundError("Atlantis"))
    service = WeatherService(api)

    with pytest.raises(CityNotFoundError):
        service.get_weather("Atlantis")


def test_get_weather_raises_network_error():
    api = FailingWeatherAPI(NetworkError())
    service = WeatherService(api)

    with pytest.raises(NetworkError):
        service.get_weather("Kyiv")