import os
import requests

# 1. Get inputs
# Make sure your secret is exactly named 'WEATHER_API_KEY'
api_key = os.environ.get('WEATHER_API_KEY')

if not api_key:
    print("Error: WEATHER_API_KEY not found in Secrets.")
    exit()

city = input("City: ")
days = int(input("Days (1-5): "))

# 2. Fetch data
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
data = response.json()

# --- ERROR HANDLING ADDED HERE ---
# The API returns a string "200" in the 'cod' field if successful
if data.get("cod") != "200":
    print(f"\nError from API: {data.get('message')}")
    # Stop the program here so it doesn't crash below
    exit()

print(f"\n--- Weather for {city.title()}: Next {days} Days ---")

# 3. Filter for distinct days
seen_dates = set()
count = 0
print(data)
# Now it is safe to access ['list']
for item in data['list']:
    dt_txt = item['dt_txt']
    date_part = dt_txt.split(" ")[0]

    if date_part not in seen_dates:
        temp = item['main']['temp']
        desc = item['weather'][0]['description']

        print(f"Date: {date_part} | Temp: {temp}°C | {desc}")

        seen_dates.add(date_part)
        count += 1

    if count == days:
        break
