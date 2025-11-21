import os
import requests

# 1. Setup
# Ensure your Secret key in Replit is named 'API_KEY'
api_key = os.environ.get('API_KEY')

if not api_key:
    print("Error: 'API_KEY' not found in Secrets.")
    exit()

# 2. User Input
user_prompt = input("\nWhat do you want to ask Gemini? \n> ")

# 3. Prepare Request
# Using gemini-1.5-flash as it is the current standard fast model
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}

payload = {"contents": [{"parts": [{"text": user_prompt}]}]}

# 4. Send & Process
print("\nThinking...")

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status(
    )  # Stop if API returns an error (like 400 or 500)

    data = response.json()

    # 5. Extract Text (The Clean Output)
    # The text is nested inside: candidates -> index 0 -> content -> parts -> index 0 -> text
    try:
        answer = data['candidates'][0]['content']['parts'][0]['text']

        print("\n--- Gemini Response ---")
        print(answer)
        print("-----------------------")

    except (KeyError, IndexError):
        print(
            "\nError: The AI blocked the response (likely safety filters) or the format changed."
        )

except requests.exceptions.RequestException as e:
    print(f"\nConnection Error: {e}")
    # Print the actual error message from Google if available
    if 'response' in locals():
        print("Details:", response.text)
