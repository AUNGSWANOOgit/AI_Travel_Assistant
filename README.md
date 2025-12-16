# AI Travel Assistant

A Python CLI application that helps users plan personalized trips using multiple APIs. It fetches country and city information, 5-day weather forecasts, currency exchange rates, and generates detailed itineraries via Google's Gemini AI. Users input their destination, travel dates, budget, and requirements to receive a day-by-day plan.

---

## Features

* **Country & City Info:** Fetch country details (capital, population, currency, languages) and major cities using GitHub JSON datasets and CountriesNow API.
* **Weather Forecast:** 5-day forecasts for any city using OpenWeather API.
* **Currency Conversion:** Convert between home and destination currencies via Frankfurter API.
* **AI Trip Planner:** Generate detailed day-by-day itineraries tailored to budget and preferences using Gemini API.
* **CLI Friendly:** Step-by-step prompts for an easy user experience.

---

## Files Overview

| File                              | Description                                         |
| --------------------------------- | --------------------------------------------------- |
| `main.py`                         | Main CLI program integrating all features and APIs. |
| `currency_converter.py`           | Standalone Frankfurter API currency conversion.     |
| `API_Workshop(GEMINI).py`         | Gemini AI text generation example.                  |
| `API_Workshop(OpenWeather).py`    | Weather forecasts example.                          |
| `API_Workshop(REST_Countries).py` | Country information example.                        |
| `run_apis.py`                     | Menu-based launcher for all API scripts.            |

---

## Setup

1. Install Python 3.11+ and `requests` library:

```bash
pip install requests
```

2. Obtain API keys:

   * **Gemini AI:** `API_KEY` from [Google AI Studio](https://aistudio.google.com/apikey)
   * **OpenWeather:** `WEATHER_API_KEY` from [OpenWeather](https://openweathermap.org/api)
   * **REST Countries:** No key required
   * **Frankfurter:** No key required
3. Set environment variables or Replit Secrets:

```bash
export API_KEY="YOUR_GEMINI_KEY"
export WEATHER_API_KEY="YOUR_OPENWEATHER_KEY"
```

---

## How to Run

### Run Main Travel Assistant

```bash
python main.py
```

Follow CLI prompts to:

1. Enter country and select city
2. Input home currency
3. Enter trip start date, duration, budget, and special requirements
4. Receive a personalized AI-generated itinerary

### Run Individual API Scripts

```bash
python "API_Workshop(GEMINI).py"
python "API_Workshop(OpenWeather).py"
python "API_Workshop(REST_Countries).py"
python "currency_converter.py"
```

### Run Menu

```bash
python run_apis.py
```

---

## Requirements

* Python 3.11+
* `requests` library

---

## Notes

* Ensure your API keys are set correctly; missing keys will prevent functionality.
* This project demonstrates full integration of multiple APIs into a single AI-assisted CLI application.
* All scripts are independently implemented and maintained by the author.

