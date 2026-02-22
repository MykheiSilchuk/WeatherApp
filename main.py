import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk 

from weather.service import WeatherService
from weather.components import WeatherDisplay
from location.components import LocationSelector
from core.logger import app_logger
from weather.api import WeatherAPI
from weather.icon_service import WeatherIconService


class WeatherApp(tk.Tk):
    def __init__(self, weather_service: WeatherService):
        super().__init__()
        self.weather_service = weather_service
        
        self.title("SkyCast Weather")
        self.geometry("450x550")
        
        self.build_ui()
        
        # Apply modern dark theme if available
        try:
            sv_ttk.set_theme("dark")
        except ImportError:
            app_logger.warning("sv-ttk not installed. Using default theme.")

    def build_ui(self):
        """Create and pack the main UI components."""
        # Location selection component - passes selected city to fetch_weather
        self.selector = LocationSelector(self, on_location_selected=self.fetch_weather)
        self.selector.pack(pady=20, padx=20, fill="x")

        # Visual separator between selector and display
        ttk.Separator(self).pack(fill="x", padx=40)

        # Main weather display component - now receives the service instance
        self.display = WeatherDisplay(self, self.weather_service.icon_service)
        self.display.pack(pady=20, fill="both", expand=True)

    def fetch_weather(self, city_name: str) -> dict:
        """
        Event handler triggered when a city is selected.
        Fetches data from API and updates the display component.
        """
        try:
            # Retrieve weather data through the service layer
            data = self.weather_service.get_weather(city_name)
            # Update the UI labels and trigger icon download
            self.display.update_weather(data)
        except Exception as e:
            app_logger.error(f"UI update error: {e}")
            messagebox.showerror("Weather Error", str(e))


def main():
    weather_api = WeatherAPI()
    icon_service = WeatherIconService()
    weather_service = WeatherService(
        weather_api,
        icon_service
    )

    app = WeatherApp(weather_service)
    
    app.mainloop()

if __name__ == "__main__":
    # Application entry point
    main()



