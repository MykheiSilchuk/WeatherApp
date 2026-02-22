import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk 

from weather.service import WeatherService
from weather.components import WeatherDisplay
from location.components import LocationSelector
from core.logger import app_logger

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkyCast Weather")
        self.geometry("450x550")
        
        # Initialize the shared weather service
        self.weather_service = WeatherService()
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
        self.display = WeatherDisplay(self, self.weather_service)
        self.display.pack(pady=20, fill="both", expand=True)

    def fetch_weather(self, city_name):
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

if __name__ == "__main__":
    # Application entry point
    app = WeatherApp()
    app.mainloop()