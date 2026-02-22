import threading
from location.api import LocationAPI
from core.database import LocationDB
from core.logger import app_logger

class LocationService:
    def __init__(self):
        self.api = LocationAPI()
        self.db = LocationDB()
        self.cache = {'countries': None, 'regions': {}, 'cities': {}}
        self.lock = threading.Lock()
        app_logger.info("LocationService initialized with Thread-Locking.")

    def get_countries_for_ui(self):
        # 1. Check local data sources (RAM cache and SQLite DB)
        local_data = self.cache['countries']
        if not local_data:
            app_logger.debug("Countries not found in cache, requesting from DB")
            local_data = self.db.get_countries()
            self.cache['countries'] = local_data

        # 2. Start background synchronization with API to keep data fresh
        threading.Thread(target=self.sync_countries, args=(local_data,), daemon=True).start()

        if not local_data:
            app_logger.warning("No country data in DB, performing initial API fetch")
            return self.sync_countries(None, return_data=True)
            
        return local_data

    def sync_countries(self, local_data, return_data=False):
        try:
            app_logger.info("Syncing country list from API.")
            api_data = self.api.get_countries()
            formatted = [{"name": c["name"], "code": c["iso2"]} for c in api_data]

            # Update DB and cache only if data has changed
            if formatted != local_data:
                with self.lock:
                    self.db.save_countries(formatted)
                    self.cache['countries'] = formatted
                    app_logger.info("Country list successfully updated in local storage")
            else:
                app_logger.debug("Country list is already up-to-date")
            
            if return_data: return formatted
        except Exception as e:
            app_logger.error("Critical error during country synchronization", exc_info=True)
            return local_data if return_data else None

    def get_regions_for_ui(self, country_code):
        app_logger.info(f"Fetching regions for country: {country_code}")
        local_data = self.cache['regions'].get(country_code) or self.db.get_regions(country_code)
        
        threading.Thread(
            target=self.sync_regions, 
            args=(country_code, local_data), 
            daemon=True
        ).start()

        if not local_data:
            return self.sync_regions(country_code, None, return_data=True)
        return local_data

    def sync_regions(self, country_code, local_data, return_data=False):
        try:
            api_data = self.api.get_regions(country_code)
            formatted = [{"name": s["name"], "code": s["iso2"]} for s in api_data]
            
            if formatted != local_data:
                with self.lock:
                    self.db.save_regions(country_code, formatted)
                    self.cache['regions'][country_code] = formatted
                    app_logger.info(f"regions for {country_code} synchronized successfully.")
            
            if return_data: return formatted
        except Exception as e:
            app_logger.error(f"Failed to fetch regions for country: {country_code}", exc_info=True)
            return local_data if return_data else None

    def get_cities_for_ui(self, country_code, region_code):
        cache_key = (country_code, region_code)
        app_logger.info(f"Fetching cities for: {country_code}, {region_code}")
        
        local_data = self.cache['cities'].get(cache_key) or self.db.get_cities(country_code, region_code)
        
        threading.Thread(
            target=self.sync_cities, 
            args=(country_code, region_code, local_data), 
            daemon=True
        ).start()

        if not local_data:
            return self.sync_cities(country_code, region_code, None, return_data=True)
        return local_data

    def sync_cities(self, country_code, region_code, local_data, return_data=False):
        try:
            api_data = self.api.get_cities(country_code, region_code)
            formatted = [c["name"] for c in api_data]
            
            if formatted != local_data:
                with self.lock:
                    self.db.save_cities(country_code, region_code, formatted)
                    self.cache['cities'][(country_code, region_code)] = formatted
                    app_logger.info(f"Cities for {region_code} ({country_code}) updated successfully.")
            
            if return_data: return formatted
        except Exception as e:
            app_logger.error(f"Error synchronizing cities for region: {region_code}", exc_info=True)
            return local_data if return_data else None