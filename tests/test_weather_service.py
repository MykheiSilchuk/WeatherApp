import pytest
from weather.service import WeatherService
from core.errors import NetworkError, CityNotFoundError

# --- Fakes and Mocks ---

class FakeIconService:
    """Mock for the icon loading service."""
    def get_icon(self, icon_code: str):
        # Return a dummy path for testing
        return f"path/to/{icon_code}.png"

class FakeWeatherAPI:
    """Mock for the weather API returning successful data."""
    def __init__(self, temp=20, desc="clear sky"):
        self.temp = temp
        self.desc = desc

    def get_weather_data(self, city: str): 
        # Simulating the OpenWeatherMap JSON structure
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
    """Mock for the weather API that raises exceptions."""
    def __init__(self, error):
        self.error = error

    def get_weather_data(self, city: str):
        raise self.error

# --- Tests ---

def test_get_weather_returns_parsed_data():
    api = FakeWeatherAPI(temp=25, desc="sunny")
    icons = FakeIconService()
    service = WeatherService(api, icons) # Correctly passing both arguments

    data = service.get_weather("Kyiv")

    # Ensure these keys match what your REAL WeatherService returns
    assert data["temperature"] == 25  
    assert data["description"] == "sunny"
    assert data["city"] == "Kyiv"

def test_get_weather_calls_api_with_correct_city():
    called = {}
    icons = FakeIconService()

    class SpyAPI(FakeWeatherAPI):
        def get_weather_data(self, city: str):
            called["city"] = city
            return super().get_weather_data(city)

    service = WeatherService(SpyAPI(), icons) # Added 'icons' argument
    service.get_weather("Lviv")

    assert called["city"] == "Lviv"

def test_get_weather_raises_city_not_found():
    api = FailingWeatherAPI(CityNotFoundError("Atlantis"))
    icons = FakeIconService()
    service = WeatherService(api, icons) # Added 'icons' argument

    with pytest.raises(CityNotFoundError):
        service.get_weather("Atlantis")

def test_get_weather_raises_network_error():
    api = FailingWeatherAPI(NetworkError())
    icons = FakeIconService()
    service = WeatherService(api, icons) # Added 'icons' argument

    with pytest.raises(NetworkError):
        service.get_weather("Kyiv")

def test_get_weather_is_case_insensitive():
    api = FakeWeatherAPI()
    icons = FakeIconService()
    service = WeatherService(api, icons) # Added 'icons' argument
    
    # Check if 'kyiv' (lower) works as well as 'Kyiv'
    try:
        service.get_weather("kyiv")
    except CityNotFoundError:
        pytest.fail("Service is case-sensitive!")