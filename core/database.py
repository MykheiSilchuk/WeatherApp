import sqlite3

class LocationDB:
    def __init__(self, db_path="locations.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Countries table
            cursor.execute('''CREATE TABLE IF NOT EXISTS countries 
                             (code TEXT PRIMARY KEY, name TEXT)''')

            # regions table
            cursor.execute('''CREATE TABLE IF NOT EXISTS regions 
                             (code TEXT, name TEXT, country_code TEXT,
                              PRIMARY KEY (code, country_code))''')
            
            # Cities table
            cursor.execute('''CREATE TABLE IF NOT EXISTS cities 
                         (name TEXT, region_code TEXT, country_code TEXT,
                          UNIQUE(name, region_code, country_code))''')
            
            conn.commit()
    def save_countries(self, countries):
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("INSERT OR REPLACE INTO countries VALUES (?, ?)", 
                            [(c['code'], c['name']) for c in countries])
    
    def get_countries(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name, code FROM countries")
            return [{"name": row[0], "code": row[1]} for row in cursor.fetchall()]
    
    def save_regions(self, country_code, regions):
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("INSERT OR REPLACE INTO regions (code, name, country_code) VALUES (?, ?, ?)", 
                            [(s['code'], s['name'], country_code) for s in regions])
    
    def get_regions(self, country_code):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name, code FROM regions WHERE country_code = ?", (country_code,))
            return [{"name": row[0], "code": row[1]} for row in cursor.fetchall()]
    
    def save_cities(self, country_code, region_code, cities):
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("INSERT OR IGNORE INTO cities (name, region_code, country_code) VALUES (?, ?, ?)", 
                            [(name, region_code, country_code) for name in cities])
    
    def get_cities(self, country_code, region_code):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name FROM cities WHERE country_code = ? AND region_code = ?", (country_code, region_code))
            return [row[0] for row in cursor.fetchall()]
    
