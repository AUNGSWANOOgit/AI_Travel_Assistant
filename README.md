# AI Travel Assistant

A collection of Python scripts demonstrating how to work with different APIs to make an AI Travel Assistant using simple requests.

## Available APIs (Under Single_API codes)

### 1. Gemini API - AI Text Generation
**File:** `API_Workshop(GEMINI).py`

Uses Google's Gemini AI to generate explanations. The you can type in your prompt to Gemini via CLI.

**Required Secret:**
- `API_KEY` - Your Google AI API key from https://aistudio.google.com/apikey

### 2. OpenWeather API - Weather Forecasts
**File:** `API_Workshop(OpenWeather).py`

Fetches weather forecasts for any city for up to 5 days.

**Required Secret:**
- `WEATHER_API_KEY` - Your OpenWeather API key from https://openweathermap.org/api

**How it works:**
- Prompts you for a city name
- Asks how many days of forecast you want (1-5)
- Shows temperature and weather description for each day

### 3. REST Countries API - Country Information
**File:** `API_Workshop(REST_Countries).py`

Gets detailed information about any country in the world.

**Required Secret:**
- `REST_API_URL` - Set to `https://restcountries.com/v3.1`

**How it works:**
- Prompts you for a country name
- Shows capital, region, population, currency, and languages

## How to Run

### Run Individual Files
In the Shell, run any file directly:
```bash
python "API_Workshop(GEMINI).py"
python "API_Workshop(OpenWeather).py"
python "API_Workshop(REST_Countries).py"
```

### Run with Menu
Use the menu system to choose which API to run:
```bash
python run_apis.py
```

## Setup

1. Get your API keys from the respective services
2. Add them to Replit Secrets (click the lock icon 🔒 in the Tools panel)
3. Run any of the Python files

## Requirements

- Python 3.11+
- requests library (already installed)
