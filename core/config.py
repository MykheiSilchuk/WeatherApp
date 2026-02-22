import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # Weather API settings
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/"
    
    # CountryRegionCity API settings for location selection
    LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")
    LOCATION_BASE_URL = "https://api.countrystatecity.in/v1/"
    
    # Asset settings
    ICON_BASE_URL = "https://openweathermap.org/img/wn/"
    TIMEOUT = 10

config = Config()