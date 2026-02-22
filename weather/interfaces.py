from abc import ABC, abstractmethod


class IWeatherAPI(ABC):

    @abstractmethod
    def get_weather_data(self, city: str) -> dict:
        pass