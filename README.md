# SkyCast Weather 🌤️

A desktop weather application built with Python and Tkinter that provides real-time weather data for cities worldwide.

## Screenshots

| Ukraine – Smila | United Kingdom – Seafield | Japan – Kimitsu |
|---|---|---|
| ![Smila](screenshots/smila.png) | ![Seafield](screenshots/seafield.png) | ![Kimitsu](screenshots/kimitsu.png) |

## Features

- Browse cities by Country → Region → City
- Real-time weather data via OpenWeatherMap API
- Temperature, feels like, humidity, pressure
- Weather icons loaded asynchronously
- Local SQLite cache for location data (faster repeated use)
- Dark theme UI via `sv-ttk`

## Tech Stack

- **Python 3.10+**
- **Tkinter + sv-ttk** — GUI
- **OpenWeatherMap API** — weather data
- **CountryStateCity API** — location hierarchy
- **SQLite** — local location cache
- **Pillow** — icon rendering
- **pytest** — unit tests

## Project Structure

```
weather_app/
├── core/           # Shared infrastructure (config, DB, logger, HTTP client, errors)
├── location/       # Country/Region/City selection (API, service, UI component)
├── weather/        # Weather data (API, service, icon service, UI component)
├── tests/          # Unit tests with fakes and mocks
└── main.py         # Entry point
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/MykheiSilchuk/WeatherApp.git
cd WeatherApp
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

```dotenv
WEATHER_API_KEY=your_openweathermap_api_key
WEATHER_BASE_URL=http://api.openweathermap.org/data/2.5/

LOCATION_API_KEY=your_countrystatecity_api_key
LOCATION_BASE_URL=https://api.countrystatecity.in/v1/

ICON_BASE_URL=https://openweathermap.org/img/wn/
TIMEOUT=10

URL_SETTINGS_UNITS=metric
URL_SETTINGS_LANG=uk
```

**Get API keys:**
- OpenWeatherMap: https://openweathermap.org/api (free tier is enough)
- CountryStateCity: https://countrystatecity.in (free)

### 5. Run the app
```bash
python main.py
```

## Running Tests

```bash
python -m pytest tests/
```

## Architecture Notes

The app follows a layered architecture:

```
API layer → Service layer → UI components → Main window
```

Each layer depends only on the layer directly below it. UI components receive only what they need — for example, `WeatherDisplay` receives `icon_service` directly rather than the full `WeatherService`.

HTTP logic is centralized in `BaseAPIClient`, keeping `WeatherAPI` and `LocationAPI` clean and focused. Location data is cached in SQLite and RAM, with background threads syncing updates from the API without blocking the UI.
