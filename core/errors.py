class WeatherError(Exception):
    """Base class for all application-specific exceptions."""
    pass

class NetworkError(WeatherError):
    """Raised when there is a connection issue."""
    def __str__(self):
        return "Network error occurred. Please check your internet connection."

class CityNotFoundError(WeatherError):
    """Raised when the weather API cannot find the specified city."""
    def __init__(self, city):
        self.city = city
    def __str__(self):
        return f"City '{self.city}' not found on the service."

class APIError(WeatherError):
    """Raised for general API or server-side issues."""
    def __init__(self, message="API Error"):
        super().__init__(message)