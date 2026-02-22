import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # Weather API settings
        self.WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
        self.WEATHER_BASE_URL: str | None = os.getenv("WEATHER_BASE_URL")
        
        # CountryRegionCity API settings for location selection
        self.LOCATION_API_KEY: str | None = os.getenv("LOCATION_API_KEY")
        self.LOCATION_BASE_URL: str | None = os.getenv("LOCATION_BASE_URL")
        
        # Asset settings
        self.ICON_BASE_URL: str | None = os.getenv("ICON_BASE_URL")
        self.TIMEOUT: int | None = int(os.getenv("TIMEOUT", 10)) 

        self.validation()

    def validation(self) -> None:
        if not self.WEATHER_API_KEY:
            raise RuntimeError(
                "WEATHER_API_KEY is not set in .env"
            )


config = Config()