from core.logger import app_logger
from core.errors import WeatherError
from weather.api import WeatherAPI
from weather.icon_service import WeatherIconService

class WeatherService:
    def __init__(
        self, 
        api: WeatherAPI,
        icon_service: WeatherIconService
    ):
        # Initialize weather API and icon service
        self.api = api
        self.icon_service = icon_service
    
    def get_weather(self, city: str) -> dict:
        """Fetch weather data for a specific city and return parsed result."""
        raw_data = self.api.get_weather_data(city)
        return self.parse_weather_data(raw_data)

    def parse_weather_data(self, data: dict) -> dict:
        """Extract and format necessary fields from the API response."""
        try:
            return {
                "city": data["name"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        except (KeyError, IndexError) as e:
            app_logger.error(f"Data parsing failed: {e}")
            raise WeatherError("Failed to process weather data from server.")