import os
import requests

# --- CONFIGURATION ---
# Make sure these are set in your environment secrets
GEMINI_API_KEY = os.environ.get('API_KEY')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
REST_API_URL = os.environ.get('REST_API_URL', "https://restcountries.com/v3.1")


# --- 1. FUNCTION: Get List of Cities (CountriesNow API) ---
def get_cities_for_country(country_name):
    """Fetches a list of cities for the given country to help the user."""
    print(f"\n🔍 Searching for major cities in {country_name}...")
    url = "https://countriesnow.space/api/v0.1/countries/cities"
    payload = {"country": country_name}

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if not data.get('error') and data.get('data'):
            return data['data']
        else:
            print(
                f"   (No specific city list found for {country_name}. You'll need to type it manually.)"
            )
            return []

    except Exception:
        print("   (Could not fetch city list. Proceeding to manual input.)")
        return []


# --- 2. FUNCTION: Get Country Metadata (GitHub Raw JSON, No API Key) ---
def get_and_display_country_info(country_name):
    """Fetch country info from a free GitHub JSON dataset (no API key)."""

    url = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"

    try:
        response = requests.get(url)
        data = response.json()

        # Find the matching country (case-insensitive)
        match = None
        for c in data:
            if c["name"]["common"].lower() == country_name.lower():
                match = c
                break

        if not match:
            print(f"❌ Country '{country_name}' not found.")
            return "Country data not found.", None

        # Extract details
        name = match["name"]["common"]
        official_name = match["name"]["official"]
        capital = match.get("capital", ["N/A"])[0]
        population = match.get("population", 0)
        region = match.get("region", "N/A")
        subregion = match.get("subregion", "N/A")

        # Currencies
        currencies = match.get("currencies", {})
        if currencies:
            cur_code = list(currencies.keys())[0]
            cur_name = currencies[cur_code]["name"]
            currency_str = f"{cur_name} ({cur_code})"
        else:
            cur_code = "N/A"
            currency_str = "N/A"

        # Languages
        languages = ", ".join(match.get("languages", {}).values())

        # AI summary string
        ai_summary = (
            f"Official Name: {name}, Capital: {capital}, "
            f"Region: {region} ({subregion}), "
            f"Currency: {currency_str}, Languages: {languages}, "
            f"Population: {population:,}"
        )

        # Print to CLI
        print(f"\n--- 🌏 REPORT FOR: {name.upper()} ---")
        print(f"Official Name: {official_name}")
        print(f"Capital:       {capital}")
        print(f"Region:        {region} ({subregion})")
        print(f"Population:    {population:,}")
        print(f"Currency:      {currency_str}")
        print(f"Languages:     {languages}")
        print("--------------------------------")

        return ai_summary, cur_code

    except Exception as e:
        print(f"Error fetching country info: {e}")
        return f"Could not fetch country data: {e}", None


# --- 3. FUNCTION: Get Weather Forecast (OpenWeather API) ---
def get_and_display_weather(city):
    """Fetches the 5-day forecast."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            print(f"❌ Weather error: {data.get('message')}")
            return f"Weather data error: {data.get('message')}"

        print(f"\n--- ☁️ CURRENT 5-DAY FORECAST FOR: {city.upper()} ---")

        report = []
        seen_dates = set()

        # The API returns 3-hour chunks; we filter for one summary per day
        for item in data.get('list', []):
            dt_txt = item.get('dt_txt', "")
            if " " not in dt_txt:
                continue

            date_part = dt_txt.split(" ")[0]

            if date_part not in seen_dates:
                main = item.get('main', {})
                weather = item.get('weather', [{}])[0]

                temp = main.get('temp', "N/A")
                desc = weather.get('description', "N/A")

                # Format
                line = f"• {date_part}: {temp}°C, {desc}"
                print(line)
                report.append(line)
                seen_dates.add(date_part)

        print("---------------------------------------")
        return "\n".join(report)

    except Exception as e:
        print(f"Error fetching weather: {e}")
        return f"Could not fetch weather: {e}"


# --- 4. FUNCTION: Currency Converter (Frankfurter API) ---
def get_exchange_rate(home_currency, target_currency):
    """Calculates the exchange rate between home and destination currency."""
    if not target_currency or target_currency == "N/A":
        return "Currency conversion unavailable."

    if home_currency == target_currency:
        return f"1 {home_currency} = 1 {target_currency} (Same Currency)"

    print(f"\n💰 Checking Exchange Rate: {home_currency} -> {target_currency}...")
    url = f"https://api.frankfurter.dev/v1/latest?base={home_currency}&symbols={target_currency}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if target_currency in data.get('rates', {}):
                rate = data['rates'][target_currency]
                result_str = f"1 {home_currency} = {rate} {target_currency}"
                print(f"   ↳ {result_str}")
                return result_str

        return "Live exchange rate unavailable."

    except Exception:
        return "Live exchange rate unavailable."


# --- 5. FUNCTION: The Gemini Planner ---
def plan_trip(city, country, home_currency, budget, days, start_date, requirements):

    # FIXED: Get country info FIRST
    country_info_text, target_currency_code = get_and_display_country_info(country)

    # Weather and exchange rate
    weather_data = get_and_display_weather(city)
    exchange_rate_info = get_exchange_rate(home_currency, target_currency_code)

    print("\n🤖 AI is thinking... generating your itinerary...")

    # Construct AI prompt
    prompt = f"""
    Act as an expert travel agent. Plan a detailed trip to {city}, {country}.

    --- TRIP DETAILS ---
    • Start Date: {start_date}
    • Duration: {days} days
    • Budget: {budget} ({home_currency})
    • Special Requirements: {requirements}

    --- REAL-TIME CONTEXT ---
    1. COUNTRY INFO: {country_info_text}
    2. EXCHANGE RATE: {exchange_rate_info}
    3. CURRENT WEATHER FORECAST:
    {weather_data}

    --- FORMATTING INSTRUCTIONS (STRICT) ---
    - Output must be CLEAN PLAIN TEXT suitable for a CLI.
    - Do NOT use Markdown bolding or headers.
    - Use UPPERCASE for section titles.
    - Use simple dashes or asterisks for bullet points.
    - Use spacing to separate sections clearly.

    --- PLANNING INSTRUCTIONS ---
    - Create a day-by-day itinerary.
    - Suggest dining and sightseeing fitting the budget.
    - USE THE EXCHANGE RATE when estimating costs.
    - If rain is predicted, suggest indoor activities.
    """

    # Gemini API call
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        answer = result['candidates'][0]['content']['parts'][0]['text']

        print("\n" + "=" * 40)
        print(f"   ✈️  YOUR PERSONALIZED TRIP TO {city.upper()}   ")
        print("=" * 40)
        print(answer)
        print("=" * 40)

    except Exception as e:
        print(f"AI Error: {e}")
        if 'response' in locals():
            print(response.text)


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    if not GEMINI_API_KEY or not WEATHER_API_KEY:
        print("CRITICAL: Missing API Keys in Environment Secrets.")
    else:
        print("--- 🌍 WELCOME TO YOUR AI TRAVEL AGENT 🌍 ---")

        # 1. Ask for Country FIRST
        user_country = input("Enter Country (e.g., France): ").strip()

        # 2. Get & Show Cities
        available_cities = get_cities_for_country(user_country)

        user_city = ""

        if available_cities:
            print(f"\n--- Found {len(available_cities)} cities in {user_country} ---")
            for i, city in enumerate(available_cities[:10], 1):
                print(f"{i}. {city}")
            if len(available_cities) > 10:
                print(f"... and {len(available_cities)-10} more.")

            print("------------------------------------------------")
            choice = input("Type a city name from above OR enter your own: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= 10:
                user_city = available_cities[int(choice) - 1]
                print(f"✅ Selected: {user_city}")
            else:
                user_city = choice
        else:
            user_city = input(f"Enter City in {user_country}: ").strip()

        # 3. Collect Home Currency
        user_home_currency = input("\nYour Home Currency (e.g., USD, EUR): ").upper()

        # 4. Collect Trip Specifics
        user_start_date = input("Start Date (e.g., 2024-12-25): ")
        user_days = input("Trip Duration (Number of days): ")
        user_budget = input("Budget (e.g., Low, High, or $2000): ")
        user_reqs = input("Special Requirements (e.g., Vegetarian, Kids): ")

        # 5. Launch Planner
        if user_city:
            plan_trip(user_city, user_country, user_home_currency, user_budget,
                      user_days, user_start_date, user_reqs)
        else:
            print("❌ Error: No city selected. Exiting.")
