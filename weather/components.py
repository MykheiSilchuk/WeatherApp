import threading
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import ttk
from core.logger import app_logger

class WeatherDisplay(ttk.Frame):
    def __init__(self, parent, weather_service):
        super().__init__(parent)
        # Store reference to the service layer
        self.weather_service = weather_service
        self.setup_ui()

    def setup_ui(self):
        """Initialize UI components for weather display."""
        self.icon_label = ttk.Label(self)
        self.icon_label.pack(pady=5)

        self.temp_label = ttk.Label(self, font=("Segoe UI", 32, "bold"))
        self.temp_label.pack()

        self.desc_label = ttk.Label(self, font=("Segoe UI", 14, "italic"))
        self.desc_label.pack()

        self.details_label = ttk.Label(self, font=("Segoe UI", 10), justify="center")
        self.details_label.pack(pady=10)

    def update_weather(self, data: dict) -> dict:
        """Update text labels and trigger background icon loading."""
        self.temp_label.config(text=f"{data['temperature']}°C")
        self.desc_label.config(text=data['description'].capitalize())
        self.details_label.config(
            text=f"Feels like: {data['feels_like']}°C\n"
                 f"Humidity: {data['humidity']}% | Pressure: {data['pressure']} hPa"
        )
        
        # Start a background thread to fetch the icon without blocking the UI
        threading.Thread(
            target=self.load_icon, 
            args=(data['icon'],), 
            daemon=True
        ).start()

    def load_icon(self, icon_code: str) -> dict:
        """Fetch icon bytes from service and convert to PhotoImage."""
        try:
            # Get raw image content via service
            content = self.weather_service.icon_service.get_icon(icon_code)
            
            # Process image using Pillow
            image = Image.open(BytesIO(content))
            photo = ImageTk.PhotoImage(image)
            
            # Use .after() to update UI from the main thread
            self.after(0, self.set_icon, photo)
        except Exception as e:
            app_logger.error(f"Error loading icon '{icon_code}': {e}")

    def set_icon(self, photo):
        """Apply the loaded image to the label and keep a reference."""
        self.icon_label.config(image=photo)
        self.icon_label.image = photo