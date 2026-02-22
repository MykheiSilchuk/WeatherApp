import tkinter as tk
from tkinter import ttk
from core.logger import app_logger
from location.service import LocationService

class LocationSelector(tk.Frame):
    def __init__(self, parent, on_location_selected):
        super().__init__(parent)
        self.service = LocationService()
        self.on_location_selected = on_location_selected
        
        self.selected_country_code = None
        self.selected_region_code = None
        self.countries_data = []
        self.regions_data = []

        self.build_ui()
        self.load_countries()

    def build_ui(self):
        # Налаштування колонок для вирівнювання
        self.columnconfigure(1, weight=1)

        # Country selection
        ttk.Label(self, text="Select Country:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.country_cb = ttk.Combobox(self, state="readonly", width=30)
        self.country_cb.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.country_cb.bind("<<ComboboxSelected>>", self.country_change)

        # Region selection
        ttk.Label(self, text="Select Region:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.region_cb = ttk.Combobox(self, state="disabled", width=30) # Спочатку вимкнено
        self.region_cb.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.region_cb.bind("<<ComboboxSelected>>", self.region_change)

        # City selection
        ttk.Label(self, text="Select City:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.city_cb = ttk.Combobox(self, state="disabled", width=30) # Спочатку вимкнено
        self.city_cb.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.city_cb.bind("<<ComboboxSelected>>", self.city_change)

    def load_countries(self):
        try:
            list_of_countries = self.service.get_countries_for_ui()
            self.countries_data = list_of_countries
            self.country_cb['values'] = [c['name'] for c in list_of_countries]
        except Exception as e:
            app_logger.error(f"UI Error loading countries: {e}")

    def country_change(self, event):
        name = self.country_cb.get()

        self.selected_country_code = next((c['code'] for c in self.countries_data if c['name'] == name), None)
        
        if not self.selected_country_code:
            return

        list_of_regions = self.service.get_regions_for_ui(self.selected_country_code)
        self.regions_data = list_of_regions


        self.region_cb.configure(state="readonly")
        self.region_cb['values'] = [r['name'] for r in list_of_regions]
        self.region_cb.set('')
        
        self.city_cb.set('')
        self.city_cb.configure(state="disabled")

    def region_change(self, event):
        name = self.region_cb.get()
        self.selected_region_code = next((s['code'] for s in self.regions_data if s['name'] == name), None)
        
        if not self.selected_region_code:
            return
        
        list_of_cities = self.service.get_cities_for_ui(self.selected_country_code, self.selected_region_code)
        self.city_cb.configure(state="readonly")
        self.city_cb['values'] = list_of_cities
        self.city_cb.set('')

    def city_change(self, event):
        city_name = self.city_cb.get()
        if city_name:
            self.on_location_selected(city_name)