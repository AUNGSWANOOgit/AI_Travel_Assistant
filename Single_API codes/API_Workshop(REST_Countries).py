import os
import requests

# 1. Get Configuration from Environment (Replit Style)
base_url = os.environ['REST_API_URL']

def get_country_info(country_name):
    # 2. Construct the endpoint (Search by Name)
    endpoint = f"{base_url}/name/{country_name}"

    try:
        response = requests.get(endpoint)

        # Check if country was found
        if response.status_code == 404:
            print(f"Error: '{country_name}' not found. Check spelling.")
            return

        response.raise_for_status()
        data = response.json()

        # The API returns a LIST of matches. We'll take the first one.
        country = data[0] 

        # 3. Extract Data (Handling complex fields)
        name = country['name']['common']
        official = country['name']['official']
        region = country.get('region', 'N/A')
        population = country.get('population', 0)

        # Handle Capital (It's a list, catch if empty)
        capital = country['capital'][0] if 'capital' in country else "No Capital"

        # Handle Currencies (Key is dynamic, e.g., "SGD", "USD")
        # We grab the first value found in the dictionary
        currency_data = country.get('currencies', {})
        if currency_data:
            first_currency_code = list(currency_data.keys())[0]
            currency_name = currency_data[first_currency_code]['name']
            currency_str = f"{currency_name} ({first_currency_code})"
        else:
            currency_str = "N/A"

        # Handle Languages (Dynamic keys like 'eng', 'zho')
        languages = country.get('languages', {})
        language_list = ", ".join(languages.values())

        # 4. Display
        print(f"\n--- Report for: {name} ---")
        print(f"Official Name: {official}")
        print(f"Capital:       {capital}")
        print(f"Region:        {region}")
        print(f"Population:    {population:,}") # commas for thousands
        print(f"Currency:      {currency_str}")
        print(f"Languages:     {language_list}")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- USAGE ---
user_input = input("Enter a country name: ")
get_country_info(user_input)